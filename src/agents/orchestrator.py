import time
from pade.core.agent import Agent
from pade.misc.utility import display_message
from pade.behaviours.protocols import TimedBehaviour
from pade.misc.common import ACLMessage
from controllers.agentmanager import get_manager
from agents.calculator import AgentSumCalculator, AgentSubtractionCalculator, AgentMultiplicationCalculator, AgentDivisionCalculator, AgentSquareRootCalculator, AgentExponentiationCalculator
from lib.mathAst import *
from antlr4 import *
import threading
from pade.misc.utility import call_later

class AgentOrchestrator(Agent):
    waitingtable = {}
    waitingmutex = threading.Lock()
    waitingerror = False

    def __init__(self, aid):
        super(AgentOrchestrator, self).__init__(aid=aid, debug=False)

    def on_start(self):
        super(AgentOrchestrator, self).on_start()
        display_message(self.aid.localname, f'Starting orchestrator agent --- {id(self)} ...')
        
        expression: str = "23 + 10 * 2 - 5 / 2 ^ 2"
        # call_later(5, self.calculate, expression)
        self.calculate(expression)

    def react(self, message):
        super().react(message)
        origin_aid = message.sender
        if message.performative == ACLMessage.ACCEPT_PROPOSAL:
            value = float(message.content)
            self.waitingmutex.acquire()
            self.waitingtable[origin_aid] = value
            self.waitingmutex.release()
        elif message.performative == ACLMessage.REJECT_PROPOSAL:
            self.waitingerror = True

    def calculate_sum(self, value1, value2):
        # Send to Calculator Sum Agent
        display_message(self.aid.localname, f'Calculating sum of {value1} and {value2} ...')
        manager = get_manager()
        targets = manager.retrieve_agent_type(AgentSumCalculator)
        if len(targets) == 0:
            display_message(self.aid.localname, f'No Sum Calculator Agent found ...')
            return
        target = targets[0]
        message = ACLMessage(ACLMessage.REQUEST)
        # message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_content(f'{value1};{value2}')
        message.add_receiver(aid=target.aid)

        # Wait for response from Calculator Sum Agent
        self.waitingmutex.acquire()
        self.waitingtable[target.aid] = None
        self.waitingmutex.release()
        self.send(message)
        while self.waitingtable[target.aid] is None or self.waitingerror == False:
            time.sleep(1.0)
        if self.waitingerror:
            raise Exception('Error calculating sum')
        display_message(self.aid.localname, f'Calculated sum of {value1} and {value2} = {self.waitingtable[target.aid]}')
        return self.waitingtable[target.aid]

    def calculate_sub(self, value1, value2):
        # Send to Calculator Sub Agent
        display_message(self.aid.localname, f'Calculating sub of {value1} and {value2} ...')
        manager = get_manager()
        targets = manager.retrieve_agent_type(AgentSubtractionCalculator)
        if len(targets) == 0:
            display_message(self.aid.localname, f'No Sub Calculator Agent found ...')
            return
        target = targets[0]
        message = ACLMessage(ACLMessage.REQUEST)
        # message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_content(f'{value1};{value2}')
        message.add_receiver(aid=target.aid)

        # Wait for response from Calculator Sub Agent
        self.waitingmutex.acquire()
        self.waitingtable[target.aid] = None
        self.waitingmutex.release()
        self.send(message)
        while self.waitingtable[target.aid] is None or self.waitingerror == False:
            time.sleep(1.0)
        if self.waitingerror:
            raise Exception('Error calculating sub')
        display_message(self.aid.localname, f'Calculated sub of {value1} and {value2} = {self.waitingtable[target.aid]}')
        return self.waitingtable[target.aid]

    def calculate_mul(self, value1, value2):
        # Send to Calculator Mul Agent
        display_message(self.aid.localname, f'Calculating mul of {value1} and {value2} ...')
        manager = get_manager()
        targets = manager.retrieve_agent_type(AgentMultiplicationCalculator)
        if len(targets) == 0:
            display_message(self.aid.localname, f'No Mul Calculator Agent found ...')
            return
        target = targets[0]
        message = ACLMessage(ACLMessage.REQUEST)
        # message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_content(f'{value1};{value2}')
        message.add_receiver(aid=target.aid)

        # Wait for response from Calculator Mul Agent
        display_message(self.aid.localname, f'Acquiring lock ...')
        self.waitingmutex.acquire()
        self.waitingtable[target.aid] = None
        self.waitingmutex.release()
        display_message(self.aid.localname, f'Lock acquired ...')
        self.send(message)

        display_message(self.aid.localname, f'Waiting for response ...')
        while self.waitingtable[target.aid] is None or self.waitingerror == False:
            time.sleep(1.0)
        if self.waitingerror:
            raise Exception('Error calculating mul')
            
        display_message(self.aid.localname, f'Calculated mul of {value1} and {value2} = {self.waitingtable[target.aid]}')
        return self.waitingtable[target.aid]
    
    def calculate_div(self, value1, value2):
        # Send to Calculator Div Agent
        display_message(self.aid.localname, f'Calculating div of {value1} and {value2} ...')
        manager = get_manager()
        targets = manager.retrieve_agent_type(AgentDivisionCalculator)
        if len(targets) == 0:
            display_message(self.aid.localname, f'No Div Calculator Agent found ...')
            return
        target = targets[0]
        message = ACLMessage(ACLMessage.REQUEST)
        # message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_content(f'{value1};{value2}')
        message.add_receiver(aid=target.aid)

        # Wait for response from Calculator Div Agent
        self.waitingmutex.acquire()
        self.waitingtable[target.aid] = None
        self.waitingmutex.release()
        self.send(message)
        while self.waitingtable[target.aid] is None or self.waitingerror == False:
            time.sleep(1.0)
        if self.waitingerror:
            raise Exception('Error calculating div')
        display_message(self.aid.localname, f'Calculated div of {value1} and {value2} = {self.waitingtable[target.aid]}')
        return self.waitingtable[target.aid]

    def calculate_pow(self, value1, value2):
        # Send to Calculator Pow Agent
        display_message(self.aid.localname, f'Calculating pow of {value1} and {value2} ...')
        manager = get_manager()
        targets = manager.retrieve_agent_type(AgentExponentiationCalculator)
        if len(targets) == 0:
            display_message(self.aid.localname, f'No Pow Calculator Agent found ...')
            return
        target = targets[0]
        message = ACLMessage(ACLMessage.REQUEST)
        # message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_content(f'{value1};{value2}')
        message.add_receiver(aid=target.aid)

        # Wait for response from Calculator Pow Agent
        self.waitingmutex.acquire()
        self.waitingtable[target.aid] = None
        self.waitingmutex.release()
        self.send(message)
        while self.waitingtable[target.aid] is None or self.waitingerror == False:
            time.sleep(1.0)
        if self.waitingerror:
            raise Exception('Error calculating pow')
        display_message(self.aid.localname, f'Calculated pow of {value1} and {value2} = {self.waitingtable[target.aid]}')
        return self.waitingtable[target.aid]

    def calculate_squareroot(self, value1, value2):
        # Send to Calculator Pow Agent
        display_message(self.aid.localname, f'Calculating squareroot of {value1} and {value2} ...')
        manager = get_manager()
        targets = manager.retrieve_agent_type(AgentSquareRootCalculator)
        if len(targets) == 0:
            display_message(self.aid.localname, f'No SquareRootPow Calculator Agent found ...')
            return
        target = targets[0]
        message = ACLMessage(ACLMessage.REQUEST)
        # message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_content(f'{value1};{value2}')
        message.add_receiver(aid=target.aid)

        # Wait for response from Calculator Pow Agent
        self.waitingmutex.acquire()
        self.waitingtable[target.aid] = None
        self.waitingmutex.release()
        self.send(message)
        while self.waitingtable[target.aid] is None or self.waitingerror == False:
            time.sleep(1.0)
        if self.waitingerror:
            raise Exception('Error calculating pow')
        display_message(self.aid.localname, f'Calculated pow of {value1} and {value2} = {self.waitingtable[target.aid]}')
        return self.waitingtable[target.aid]

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
        display_message(self.aid.localname, f'INPUT: {text}')
        lexer = MathLexer.mathparserLexer(text)
        tokenstream = CommonTokenStream(lexer)        
        parser = MathParser.mathparserParser(tokenstream)   
        display_message(self.aid.localname, f'PARSER: {parser.literalNames}')
        tree = parser.compileUnit()
        display_message(self.aid.localname, f'TREE: {tree.toStringTree(recog=parser)}')
        ast = MathVisitor.customMathParserVisitor().visitCompileUnit(tree)
        display_message(self.aid.localname, f'AST: {ast}')
        value = self.visit(ast)
        display_message(self.aid.localname, f'Value: {value}')
        return value