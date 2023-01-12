from pade.core.agent import Agent
from pade.misc.utility import display_message
from pade.behaviours.protocols import TimedBehaviour
from pade.misc.common import ACLMessage, AID
from controllers.agentmanager import get_manager
# from agents.orchestrator import AgentOrchestrator

# Define agents for sum, subtraction, multiplication, division, exponentiation, and square root
# Binary operations have values separated by ';' (e.g. 10;10)

class AgentSumCalculator(Agent):
    initiator: 'AgentOrchestrator' = None
    def __init__(self, aid):
        super(AgentSumCalculator, self).__init__(aid=aid, debug=False)
        display_message(self.aid.localname, f'Starting calculator agent --- {id(self)} ...')

    def set_initiator(self, initiator: 'AgentOrchestrator'):
        self.initiator = initiator

    def react(self, message):
        super(AgentSumCalculator, self).react(message)
        display_message(self.aid.localname, f'Received message from {message.sender.getName()} ::: {id(message.sender)} --- {message.content}')
        if message.performative == ACLMessage.INFORM:
            if str(message.content).startswith("CALC:::") == False:
                display_message(self.aid.localname, f'Message is not valid. Ignoring...')
                return
            content = message.content
            display_message(self.aid.localname, f'Received message from {message.sender.getName()} ::: {id(message.sender)} --- {message.content}')
            values = content.split(';')
            value1 = float(values[0])
            value2 = float(values[1])
            result = self.apply_sum(value1, value2)

            # Prepare result message
            result_message = ACLMessage(ACLMessage.ACCEPT_PROPOSAL)
            result_message.set_content(str(result))
            result_message.add_receiver(self.initiator.aid)
            self.send(result_message)
            display_message(self.aid.localname, f'Sent message to {self.initiator.aid.getName()} ::: {id(self.initiator.aid)} --- {result_message.content}')

    def apply_sum(self, value1, value2):
        return value1 + value2

class AgentSubtractionCalculator(Agent):
    def __init__(self, aid):
        super(AgentSubtractionCalculator, self).__init__(aid=aid, debug=False)
        display_message(self.aid.localname, f'Starting calculator agent --- {id(self)} ...')
    
    def react(self, message):
        super(AgentSubtractionCalculator, self).react(message)
        if message.performative == ACLMessage.INFORM:
            display_message(self.aid.localname, f'Received message from {message.sender.getName()} ::: {id(message.sender)} --- {message.content}')
            if str(message.content).startswith("CALC:::") == False:
                display_message(self.aid.localname, f'Message is not valid. Ignoring...')
                return
            display_message(self.aid.localname, f'Message is valid. Calculating...')
            content = message.content
            values = content.split(';')
            value1 = float(values[0])
            value2 = float(values[1])
            result = self.apply_subtraction(value1, value2)

            # Prepare result message
            result_message = ACLMessage(ACLMessage.ACCEPT_PROPOSAL)
            result_message.set_content(str(result))
            result_message.add_receiver(self.initiator.aid)
            self.send(result_message)
            display_message(self.aid.localname, f'Sent message to {self.initiator.aid.getName()} ::: {id(self.initiator.aid)} --- {result_message.content}')
    
    def apply_subtraction(self, value1, value2):
        return value1 - value2

class AgentMultiplicationCalculator(Agent):
    def __init__(self, aid):
        super(AgentMultiplicationCalculator, self).__init__(aid=aid, debug=False)
        display_message(self.aid.localname, f'Starting calculator agent --- {id(self)} ...')
    
    def react(self, message):
        super(AgentMultiplicationCalculator, self).react(message)
        if message.performative == ACLMessage.INFORM:
            display_message(self.aid.localname, f'Received message from {message.sender.getName()} ::: {id(message.sender)} --- {message.content}')
            if str(message.content).startswith("CALC:::") == False:
                display_message(self.aid.localname, f'Message is not valid. Ignoring...')
                return
            display_message(self.aid.localname, f'Message is valid. Calculating...')
            content = message.content
            values = content.split(';')
            value1 = float(values[0])
            value2 = float(values[1])
            result = self.apply_multiplication(value1, value2)

            # Prepare result message
            result_message = ACLMessage(ACLMessage.ACCEPT_PROPOSAL)
            result_message.set_content(str(result))
            result_message.add_receiver(self.initiator.aid)
            self.send(result_message)
            display_message(self.aid.localname, f'Sent message to {self.initiator.aid.getName()} ::: {id(self.initiator.aid)} --- {result_message.content}')
    
    def apply_multiplication(self, value1, value2):
        return value1 * value2

class AgentDivisionCalculator(Agent):
    def __init__(self, aid):
        super(AgentDivisionCalculator, self).__init__(aid=aid, debug=False)
        display_message(self.aid.localname, f'Starting calculator agent --- {id(self)} ...')
    
    def react(self, message):
        super(AgentDivisionCalculator, self).react(message)
        if message.performative == ACLMessage.INFORM:
            display_message(self.aid.localname, f'Received message from {message.sender.getName()} ::: {id(message.sender)} --- {message.content}')
            if str(message.content).startswith("CALC:::") == False:
                display_message(self.aid.localname, f'Message is not valid. Ignoring...')
                return
            display_message(self.aid.localname, f'Message is valid. Calculating...')
            content = message.content
            values = content.split(';')
            value1 = float(values[0])
            value2 = float(values[1])
            result = self.apply_division(value1, value2)

            # Prepare result message
            result_message = ACLMessage(ACLMessage.ACCEPT_PROPOSAL)
            result_message.set_content(str(result))
            result_message.add_receiver(self.initiator.aid)
            self.send(result_message)
            display_message(self.aid.localname, f'Sent message to {self.initiator.aid.getName()} ::: {id(self.initiator.aid)} --- {result_message.content}')
    
    def apply_division(self, value1, value2):
        return value1 / value2

class AgentExponentiationCalculator(Agent):
    def __init__(self, aid):
        super(AgentExponentiationCalculator, self).__init__(aid=aid, debug=False)
        display_message(self.aid.localname, f'Starting calculator agent --- {id(self)} ...')
    
    def react(self, message):
        super(AgentExponentiationCalculator, self).react(message)
        if message.performative == ACLMessage.INFORM:
            display_message(self.aid.localname, f'Received message from {message.sender.getName()} ::: {id(message.sender)} --- {message.content}')
            if str(message.content).startswith("CALC:::") == False:
                display_message(self.aid.localname, f'Message is not valid. Ignoring...')
                return
            display_message(self.aid.localname, f'Message is valid. Calculating...')
            content = message.content
            values = content.split(';')
            value1 = float(values[0])
            value2 = float(values[1])
            result = self.apply_exponentiation(value1, value2)

            # Prepare result message
            result_message = ACLMessage(ACLMessage.ACCEPT_PROPOSAL)
            result_message.set_content(str(result))
            result_message.add_receiver(self.initiator.aid)
            self.send(result_message)
            display_message(self.aid.localname, f'Sent message to {self.initiator.aid.getName()} ::: {id(self.initiator.aid)} --- {result_message.content}')
    
    def apply_exponentiation(self, value1, value2):
        return value1 ** value2

class AgentSquareRootCalculator(Agent):
    def __init__(self, aid):
        super(AgentSquareRootCalculator, self).__init__(aid=aid, debug=False)
        display_message(self.aid.localname, f'Starting calculator agent --- {id(self)} ...')
    
    def react(self, message):
        super(AgentSquareRootCalculator, self).react(message)
        if message.performative == ACLMessage.INFORM:
            display_message(self.aid.localname, f'Received message from {message.sender.getName()} ::: {id(message.sender)} --- {message.content}')
            if str(message.content).startswith("CALC:::") == False:
                display_message(self.aid.localname, f'Message is not valid. Ignoring...')
                return
            display_message(self.aid.localname, f'Message is valid. Calculating...')
            content = message.content
            values = content.split(';')
            value1 = float(values[0])
            value2 = float(values[1])
            result = self.apply_square_root(value1, value2)

            # Prepare result message
            result_message = ACLMessage(ACLMessage.ACCEPT_PROPOSAL)
            result_message.set_content(str(result))
            result_message.add_receiver(self.initiator.aid)
            self.send(result_message)
            display_message(self.aid.localname, f'Sent message to {self.initiator.aid.getName()} ::: {id(self.initiator.aid)} --- {result_message.content}')
    
    def apply_square_root(self, value1, value2):
        return value1 ** value2