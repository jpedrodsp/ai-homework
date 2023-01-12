from pade.core.agent import Agent
from pade.misc.utility import display_message
from pade.misc.common import ACLMessage
from controllers.agentmanager import get_manager
from agents.calculator import AgentSumCalculator, AgentSubtractionCalculator, AgentMultiplicationCalculator, AgentDivisionCalculator, AgentSquareRootCalculator, AgentExponentiationCalculator
from lib.mathAst import *
from antlr4 import *
import threading
from pade.behaviours.protocols import FipaRequestProtocol

class FipaProtocolOrchestrator(FipaRequestProtocol):
    """
    When this protocol is added, the orchestrator agent will be enabled to
    receive answers from the calculator agents.
    """
    def __init__(self, agent):
        super(FipaProtocolOrchestrator, self).__init__(agent=agent, message=None, is_initiator=False)
    
    def handle_inform(self, message):
        super().handle_inform(message)
        # TODO: translate answer from calculator agent to internal tables

class AgentOrchestrator(Agent):
    messages = {}
    message_mutex: threading.Lock = None

    def messages_next_available_id(self) -> int:
        next_slot = 0
        while True:
            if next_slot not in self.messages.keys():
                break
            next_slot += 1
        return next_slot

    def messages_add(self):
        self.message_mutex.acquire()
        message_id = self.messages_next_available_id()
        self.messages[message_id] = "wait"
        self.message_mutex.release()

    def __init__(self, aid):
        super(AgentOrchestrator, self).__init__(aid=aid, debug=False)
        self.messages = {}
        self.message_mutex = threading.Lock()

    def on_start(self):
        super(AgentOrchestrator, self).on_start()
        display_message(self.aid.localname, f'Starting orchestrator agent --- {id(self)} ...')
        
        expression: str = "23 + 10 * 2 - 5 / 2 ^ 2"
        self.calculate(expression)

    def react(self, message):
        super().react(message)
        origin_aid = message.sender
        display_message(self.aid.localname, f'Received message from {origin_aid.getName()} ::: {id(origin_aid)} --- {message.content}')

    def calculate_sum(self, value1, value2):
        # Send to Calculator Sum Agent
        display_message(self.aid.localname, f'Calculating sum of {value1} and {value2} ...')
        manager = get_manager()
        targets = manager.retrieve_agent_type(AgentSumCalculator)
        if len(targets) == 0:
            display_message(self.aid.localname, f'No Sum Calculator Agent found ...')
            return
        target = targets[0]
        message = ACLMessage(ACLMessage.INFORM)
        message.set_content(f'CALC:::{value1};{value2}')
        message.add_receiver(aid=target.aid)

        # Configure orchestrator agent to wait for response
        display_message(self.aid.localname, f'Sending message ...')
        self.messages_add()
        self.send(message)

        return

    def calculate_sub(self, value1, value2):
        # Send to Calculator Sub Agent
        display_message(self.aid.localname, f'Calculating sub of {value1} and {value2} ...')
        manager = get_manager()
        targets = manager.retrieve_agent_type(AgentSubtractionCalculator)
        if len(targets) == 0:
            display_message(self.aid.localname, f'No Sub Calculator Agent found ...')
            return
        target = targets[0]
        message = ACLMessage(ACLMessage.INFORM)
        message.set_content(f'CALC:::{value1};{value2}')
        message.add_receiver(aid=target.aid)

        # Wait for response from Calculator Sub Agent
        display_message(self.aid.localname, f'Sending message ...')
        self.messages_add()
        self.send(message)

    def calculate_mul(self, value1, value2):
        # Send to Calculator Mul Agent
        display_message(self.aid.localname, f'Calculating mul of {value1} and {value2} ...')
        manager = get_manager()
        targets = manager.retrieve_agent_type(AgentMultiplicationCalculator)
        if len(targets) == 0:
            display_message(self.aid.localname, f'No Mul Calculator Agent found ...')
            return
        target = targets[0]
        message = ACLMessage(ACLMessage.INFORM)
        message.set_content(f'CALC:::{value1};{value2}')
        message.add_receiver(aid=target.aid)

        # Wait for response from Calculator Mul Agent
        display_message(self.aid.localname, f'Sending message ...')
        self.messages_add()
        self.send(message)
    
    def calculate_div(self, value1, value2):
        # Send to Calculator Div Agent
        display_message(self.aid.localname, f'Calculating div of {value1} and {value2} ...')
        manager = get_manager()
        targets = manager.retrieve_agent_type(AgentDivisionCalculator)
        if len(targets) == 0:
            display_message(self.aid.localname, f'No Div Calculator Agent found ...')
            return
        target = targets[0]
        message = ACLMessage(ACLMessage.INFORM)
        message.set_content(f'CALC:::{value1};{value2}')
        message.add_receiver(aid=target.aid)

        # Wait for response from Calculator Div Agent
        display_message(self.aid.localname, f'Sending message ...')
        self.messages_add()
        self.send(message)

    def calculate_pow(self, value1, value2):
        # Send to Calculator Pow Agent
        display_message(self.aid.localname, f'Calculating pow of {value1} and {value2} ...')
        manager = get_manager()
        targets = manager.retrieve_agent_type(AgentExponentiationCalculator)
        if len(targets) == 0:
            display_message(self.aid.localname, f'No Pow Calculator Agent found ...')
            return
        target = targets[0]
        message = ACLMessage(ACLMessage.INFORM)
        message.set_content(f'CALC:::{value1};{value2}')
        message.add_receiver(aid=target.aid)

        # Wait for response from Calculator Pow Agent
        display_message(self.aid.localname, f'Sending message ...')
        self.messages_add()
        self.send(message)

    def calculate_squareroot(self, value1, value2):
        # Send to Calculator Pow Agent
        display_message(self.aid.localname, f'Calculating squareroot of {value1} and {value2} ...')
        manager = get_manager()
        targets = manager.retrieve_agent_type(AgentSquareRootCalculator)
        if len(targets) == 0:
            display_message(self.aid.localname, f'No SquareRootPow Calculator Agent found ...')
            return
        target = targets[0]
        message = ACLMessage(ACLMessage.INFORM)
        message.set_content(f'CALC:::{value1};{value2}')
        message.add_receiver(aid=target.aid)

        # Wait for response from Calculator Pow Agent
        display_message(self.aid.localname, f'Sending message ...')
        self.messages_add()
        self.send(message)

    def visit(self, node):
        display_message(self.aid.localname, f'Visiting node {node} --- {str(node)}')        
        if type(node) == InfixExpressionNode or type(node) == InfixExpressionNode or type(node) == NumberNode:
            display_message(self.aid.localname, f'Visiting infix expression node {node} --- {str(node)}')
            if node.value == '+':          
                lvalue = self.visit(node.left)
                rvalue = self.visit(node.right)
                display_message(self.aid.localname, f'Calculating sum of {lvalue} and {rvalue} ...')
                return self.calculate_sum(lvalue, rvalue)
            elif node.value == '-':                
                lvalue = self.visit(node.left)
                rvalue = self.visit(node.right)
                display_message(self.aid.localname, f'Calculating sub of {lvalue} and {rvalue} ...')
                return self.calculate_sub(lvalue, rvalue)
            elif node.value == '*':                
                lvalue = self.visit(node.left)
                rvalue = self.visit(node.right)
                display_message(self.aid.localname, f'Calculating mul of {lvalue} and {rvalue} ...')
                return self.calculate_mul(lvalue, rvalue)
            elif node.value == '/':                
                lvalue = self.visit(node.left)
                rvalue = self.visit(node.right)
                display_message(self.aid.localname, f'Calculating div of {lvalue} and {rvalue} ...')
                return self.calculate_div(lvalue, rvalue)
            elif node.value == '^':
                lvalue = self.visit(node.left)
                rvalue = self.visit(node.right)
                if rvalue == 0.5:
                    display_message(self.aid.localname, f'Calculating squareroot of {lvalue} and {rvalue} ...')
                    return self.calculate_squareroot(lvalue, rvalue)
                else:
                    display_message(self.aid.localname, f'Calculating pow of {lvalue} and {rvalue} ...')
                    return self.calculate_pow(lvalue, rvalue)
            else:
                display_message(self.aid.localname, f'Returning value {node.value} ...')
                return node.value

    def calculate(self, expression: str):
        display_message(self.aid.localname, f'Calculating expression {expression} ...')
        text = InputStream(expression)
        # display_message(self.aid.localname, f'INPUT: {text}')
        lexer = MathLexer.mathparserLexer(text)
        tokenstream = CommonTokenStream(lexer)        
        parser = MathParser.mathparserParser(tokenstream)   
        # display_message(self.aid.localname, f'PARSER: {parser.literalNames}')
        tree = parser.compileUnit()
        # display_message(self.aid.localname, f'TREE: {tree.toStringTree(recog=parser)}')
        ast = MathVisitor.customMathParserVisitor().visitCompileUnit(tree)
        # display_message(self.aid.localname, f'AST: {ast}')
        value = self.visit(ast)
        display_message(self.aid.localname, f'Value: {value}')
        return value