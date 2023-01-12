# Relatório de Inteligência Artificial

# Grupo

- JOAO PEDRO DOS SANTOS PATROCINIO
- GABRIEL RODRIGUES DE SOUSA
- ANTONIO GERALDO REGO JUNIOR
- PEDRO MARQUES DA SILVA JUNIOR

# Introdução

Este relatório visa apresentar os resultados obtidos da atividade na disciplina de Inteligência Artificial, ministrada pelo professor Vinicius Ponte Machado no período letivo de 2022.2.

A atividade propôs que o grupo elaborasse um sistema de cálculo de expressões numéricas utilizando a framework JADE - Java Agent Development Framework.

Utilizamos a framework PADE - Python Agent Development Framework, que é uma implementação da framework JADE em Python.

Escolhemos Python como linguagem de desenvolvimento devido a sua flexibilidade e facilidade de uso.
Entretanto, a framework PADE não é tão bem documentada quanto o JADE. Durante as considerações, entraremos em mais detalhes sobre as consequências de tal escolha.

Neste documento iremos apresentar a metodologia utilizada para a elaboração do sistema, os resultados obtidos e as dificuldades encontradas durante o desenvolvimento da atividade.

# Metodologia

## Expressões e suas precedência

Uma expressão numérica é composto por um conjunto de operações e números. As operações são realizadas de acordo com a precedência de operadores, ou seja, primeiro são realizadas as operações de maior precedência, depois as de menor precedência e por fim as de menor precedência.

A precedência de operadores é definida da seguinte forma:

| Symbol | Name | Precedence                |
|--------|------|---------------------------|
| ()     | Parentheses                  | 1 |
| ^      | Exponent                     | 2 |
| * /    | Multiplication / Division    | 3 |
| + -    | Addition / Subtraction       | 4 |

A resolução de expressões numéricas de maneira correta depende da ordem das operações.
Uma operação com maior precedência deve ser executada antes de outra com menor precedência.

Por exemplo, a expressão `2 + 3 * 4` deve ser resolvida da seguinte forma:

```
- Resolve-se 3 * 4 = 12
- Resolve-se 2 + 12 = 14
- Resultado final: 14
```

Subexpressões entre parênteses devem ser resolvidas primeiro, por exemplo em `(2 + 3) * 4`. Observe:

```
- Resolve-se 2 + 3 = 5
- Resolve-se 5 * 4 = 20
- Resultado final: 20
```

Então, precisamos de um algoritmo que resolva expressões numéricas de maneira correta, levando em consideração a precedência de operadores.

## Reconhecimento das expressões numéricas

Para construir uma estrutura capaz de decidir e ordenar a ordem de precedência de expressões numéricas, utilizamos o framework `antlr` para criar uma AST (Abstract Syntax Tree) a partir de uma expressão numérica.

Definimos uma linguagem no arquivo `src/lib/mathparser.g4` capaz de decodificar expressões numéricas. A linguagem é definida da seguinte forma:

```antlr
grammar mathparser;
compileUnit
    :   expr
    ;
expr
   :   '(' expr ')'                         # parensExpr
   |   left=expr op='^' right=expr          # infixExpr
   |   left=expr op=('*'|'/') right=expr    # infixExpr
   |   left=expr op=('+'|'-') right=expr    # infixExpr
   |   value=NUM                            # numberExpr
   ;

OP_ADD: '+';
OP_SUB: '-';
OP_MUL: '*';
OP_DIV: '/';
OP_POW: '^';

NUM :   [0-9]+ ('.' [0-9][eE][+-]?[0-9]+)? ;
WS  :   [ \t\r\n] -> channel(HIDDEN);
```

Observe que a linguagem é capaz de decodificar expressões numéricas com parênteses, operações de soma, subtração, multiplicação, divisão e potência.

Cada uma das operações é definida como uma regra da linguagem, por exemplo:

```antlr
expr
   :   '(' expr ')'                         # parensExpr
   |   left=expr op='^' right=expr          # infixExpr
   |   left=expr op=('*'|'/') right=expr    # infixExpr
   |   left=expr op=('+'|'-') right=expr    # infixExpr
   |   value=NUM                            # numberExpr
   ;
```

A regra `expr` é a regra principal da linguagem, ela é capaz de decodificar expressões numéricas. A regra `expr` é subdefinida em regras alternativas como: `parensExpr`, `infixExpr`, e `numberExpr`.

Cada uma dessas regras alternativas possui um comportamento definido em código para criar uma estrutura em árvore de sintaxe abstrata (AST).

A regra `parensExpr` é capaz de decodificar expressões numéricas entre parênteses, por exemplo `(2 + 3) * 4`. A regra `infixExpr` é capaz de decodificar expressões numéricas com operações de soma, subtração, multiplicação, divisão e potência. A regra `numberExpr` é capaz de decodificar expressões numéricas com apenas números.

Escolhemos gerar o `parser`, `visitor` e `listener` do `antlr` em Python3, para que possamos integrar tais estruturas com a framework PADE.

Criamos estruturas auxiliares para facilitar a manipulação da AST gerada pelo `antlr`. Essas estruturas são funções e classes que sabem lidar com o código gerado pelo `antlr`, visitando cada nó da AST e criando uma estrutura de dados que possa ser manipulada com mais facilidade. Tais estruturas estão definidas no arquivo `lib/mathAst.py`.

```python
import lib.mathparserParser as MathParser
import lib.mathparserLexer as MathLexer
import lib.custommathparserVisitor as MathVisitor
from pade.misc.utility import display_message

class NumberNode():    
    def __init__(self, value=None):        
        self.value = value

def visitNumberExpr(self, ctx:MathParser.mathparserParser.NumberExprContext):
    value = int(str(ctx.NUM()))
    nn = NumberNode(value=value)
    return nn

class InfixExpressionNode():    
    def __init__(self, left=None, right=None, value=None):            
        self.value = value
        self.left = left
        self.right = right

def visitInfixExpr(self, ctx:MathParser.mathparserParser.InfixExprContext):
    node = InfixExpressionNode()        
    if ctx.OP_ADD():            
        node.value = '+'        
    elif ctx.OP_SUB():            
        node.value = '-'
    elif ctx.OP_MUL():            
        node.value = '*'        
    elif ctx.OP_DIV():            
        node.value = '/'        
    elif ctx.OP_POW():
        node.value = '^'
    node.left = self.visit(ctx.left)        
    node.right = self.visit(ctx.right)        
    return node
```

Após alguns testes, verificamos que a linguagem reconhecida pelo `antlr` estava pronta para ser integrada com a nossa aplicação.
Em seguida, focamos em implementar o programa inicial, que se utilizaria da framework PADE para criar um agente que seria capaz de resolver expressões numéricas.

## Implementação do programa: Tipos de Agente

Para a implementação do sistema de resolução de expressões numéricas baseada em agentes, fizemos uso da framework PADE. A framework PADE é uma framework de desenvolvimento de agentes baseada em Python3. A framework PADE é capaz de criar agentes que se comunicam entre si utilizando o protocolo `FIPA-ACL` e que podem ser executados em ambientes distribuídos.

Criamos um agente orquestrador de cálculo denominado `AgentOrchestrator` que é capaz de requisitar resultados de operações de cálculo para agentes especializados em tais operações, ou seja, cada agente de cálculo é capaz de resolver um determinado tipo de operação.

Existem seis tipos de operações de cálculo que podem ser realizadas pelo sistema: soma, subtração, multiplicação, divisão, potência e raiz quadrada. Cada um desses tipos de operação é representado por um agente especializado, como mostrado na tabela a seguir:

| Tipo de Agente | Operação | O que ele faz |
| :--- | :--- | :--- |
| AgentSumCalculator | Soma | Realiza a soma de dois números |
| AgentSubtractionCalculator | Subtração | Realiza a subtração de dois números |
| AgentMultiplicationCalculator | Multiplicação | Realiza a multiplicação de dois números |
| AgentDivisionCalculator | Divisão | Realiza a divisão de dois números |
| AgentExponentiationCalculator | Potência | Realiza a potência de um número, exceto a potência de raiz quadrada |
| AgentSquareRootCalculator | Raiz quadrada | Realiza a potência de raiz quadrada de um número |

## Implementação do Programa: Gerenciador de Agentes

Para lidar com os diferentes tipos de agentes, criamos uma classe denominada `AgentManager` que é capaz de gerenciar a criação, destruição e listagem de agentes. A classe `AgentManager` é responsável por criar os agentes orquestrador e especializados, bem como por gerenciar o ciclo de vida dos mesmos. A classe `AgentManager` é definida no arquivo `src/controllers/agentmanager.py`.

O AgentManager é um `singleton`, ou seja, apenas uma instância dele pode existir em um determinado momento. Para garantir que apenas uma instância do AgentManager exista, definimos uma função `get_manager()` que retorna a instância do AgentManager. Caso a instância do AgentManager não exista, a função `get_manager()` cria uma instância do AgentManager e a retorna. Tal referência fica armazenada na variável global `manager`.

A porta padrão para criação de agentes inicia-se na porta `50000`. Para cada agente criado, a porta é incrementada em 1. A classe `AgentManager` é definida a seguir:

```python
from pade.core.agent import Agent
from pade.misc.utility import display_message, start_loop as _start_loop
from pade.acl.aid import AID
from typing import List

manager = None
DEFAULT_MANAGER_PORT = 50000

def get_manager() -> 'AgentManager':
    """
    This function returns the global agent manager.
    """
    global manager
    if not manager:
        manager = AgentManager(DEFAULT_MANAGER_PORT)
    return manager

class AgentManager():
    def __init__(self, initial_port: int) -> None:
        self.agents: List[Agent] = []
        self.initial_port: int = initial_port
        global manager
        if not manager:
            manager = self
    def create_agent(self, agent_type: Agent, agent_id_str: str = None, agent_id_host: str = None, agent_id_port: int = None) -> Agent:
        """
        This function instantes a agent inside our internal management structure.
        It configures the agent id (host, port and name) and insert it onto our list of created agents.
        It returns the created agent.
        """
        if not agent_id_host:
            agent_id_host = "localhost"
        if not agent_id_port:
            agent_id_port = self.initial_port + len(self.agents)
        if not agent_id_str:
            agent_id_str = f'agent-{len(self.agents)}@{agent_id_host}:{agent_id_port}'
        agent_id = AID(name=agent_id_str)
        agent = agent_type(aid=agent_id)
        self.agents.append(agent)
        return agent
    def retrieve_agent_type(self, agent_type: Agent) -> List[Agent]:
        """
        This function retrieves all agents of a given type.
        """
        return [agent for agent in self.agents if isinstance(agent, agent_type)]
    def start_loop(self):
        """
        This function activates the internal agent loop of PADE, preventing the application from quitting.
        """
        _start_loop(self.agents)
```

## Implementação do Programa: Protocolo de Comunicação entre os Agentes de Cálculo e Orquestrador

O protocolo de comunicação entre os agentes de cálculo e orquestrador é definido nos arquivos de suas próprias classes, sendo eles os arquivos `src/agents/orchestrator.py` e `src/agents/calculator.py`.

Foi pensado em um protocolo ping-pong para resolução desses cálculos. Neste protocolo, seria criado uma sequência de requisições do tipo FipaProtocol para os agentes de cálculo partindo do agente orquestrador. O agente orquestrador aguardaria a resposta do agente de cálculo e, após receber a resposta, retornaria a resposta para o agente orquestrador. O agente orquestrador, com a solução em mãos, retornaria a resposta para o agente que solicitou o cálculo.

Entretanto, houve alguns problemas para a criação desse protocolo. O PADE possui problemas para utilização da função `time.sleep(seconds: float)`.
Ao utilizar essa função, o PADE não consegue receber mensagens de outros agentes, já que a função `time.sleep(seconds: float)` trava a thread principal do programa.

Tivemos que adaptar o programa para que os agentes orquestradores não utilizassem a função `time.sleep(seconds: float)` para esperar a resposta dos agentes de cálculo.

Então, optamos por utilizar um sistema de tabela/árvore para armazenar as requisições e respostas dos agentes. A tabela/árvore é definida na classe `Orchestrator` do arquivo `src/agents/orchestrator.py` através de uma variável armazenando um mapa e um mutex para garantir a segurança de acesso à variável.

## Implementação do Programa: Descrição dos Agentes

| Agente | Arquivo | Descrição |
| --- | --- | --- |
| Agente Orquestrador | `src/agents/orchestrator.py` | Responsável por realizar a primeira requisição de cálculo para os agentes de cálculo. |
| Agente de Cálculo de Soma | `src/agents/calculator.py` | Responsável por realizar quaisquer operações de soma vindo do orquestrador. |
| Agente de Cálculo de Subtração | `src/agents/calculator.py` | Responsável por realizar quaisquer operações de subtração vindo do orquestrador. |
| Agente de Cálculo de Multiplicação | `src/agents/calculator.py` | Responsável por realizar quaisquer operações de multiplicação vindo do orquestrador. |
| Agente de Cálculo de Divisão | `src/agents/calculator.py` | Responsável por realizar quaisquer operações de divisão vindo do orquestrador. |
| Agente de Cálculo de Potenciação | `src/agents/calculator.py` | Responsável por realizar quaisquer operações de potenciação vindo do orquestrador, exceto pela de raíz quadrada (ex.: x ^ 0.5) |
| Agente de Cálculo de Raíz Quadrada | `src/agents/calculator.py` | Responsável por realizar quaisquer operações de raíz quadrada vindo do orquestrador. |

## Implementação do Programa: Comportamento de Protocolo FIPA para o Agente Orquestrador

Como mencionado anteriormente, o orquestrador é responsável por iniciar e controlar as requisições de cálculo para os agentes de cálculo. Para isso, ele utiliza o sistema de comportamentos do PADE, que permite os agentes a tomarem decisões baseadas em eventos.

O evento que o agente orquestrador recebe é o evento `INFORM` do protocolo FIPA. Os agentes de cálculo, após o envio da requisição de cálculo durante o processo de visita da AST, enviam uma mensagem de informação para o agente orquestrador. O agente orquestrador, então, recebe a mensagem e realiza o tratamento da mensagem, que consiste em:

- Analisar a mensagem recebida e verificar se a mensagem é uma resposta de um agente de cálculo;
- Se a mensagem for uma resposta de um agente de cálculo, então o agente orquestrador deve verificar se a resposta é a resposta final do cálculo;
- Se a resposta for a resposta final do cálculo, então o agente orquestrador deve imprimrir uma mensagem de final de cálculo.

## Implementação do Programa: Comportamento de Protocolo FIPA para o Agente de Cálculo

Os agentes de cálculo também possuem uma classe de comportamento de protocolo FIPA. Essa classe de comportamento é responsável por receber as requisições de cálculo e realizar o cálculo. Após o cálculo, o agente de cálculo envia uma mensagem de informação para o agente orquestrador.

A única implementação de agente que talvez não tenha ficado muito clara é o agente de cálculo de potenciação. O agente de cálculo de potenciação é responsável por realizar qualquer operação de potenciação, exceto pela de raíz quadrada. A raíz quadrada é realizada pelo agente de cálculo de raíz quadrada.

# Conclusão e Considerações Finais

## Resultados

O planejamento e a conceituação do trabalho ocorreram de forma planejada. Decompor expressões numéricas e tentar realizar o cálculo com agentes específicos parecia uma tarefa simples com as estruturas de sistemas operacionais mais comuns, tais como processos e threads.

Com isso, **desenvolvemos parcialmente** as funcionalidades do programa. O contratempo de ter que reverter as estruturas dos agentes quando descobriu-se que o PADE não suporta a função `time.sleep(seconds: float)` foi um problema que não estava previsto no planejamento. Porém, o problema foi resolvido conceitualmente com a implementação de uma tabela/árvore para armazenar as requisições e respostas dos agentes.

Para podermos finalizar este trabalho, precisariamos finalizar a parte de gerenciamento das mensagens por parte do orquestrador. No tempo do trabalho, não foi possível entregar tal funcionalidade.

Teoricamente, consiste em implementar o protocolo ping-pong do trabalho para que seja possível adicionar um comportamento para cada mensagem dos agentes de cálculo, onde ao final da mesma ela seja removida. Com o valor do cálculo armazenado, o processo de visita da árvore pode ser finalizado e o resultado final pode ser impresso.

# Referências

Referencias aqui