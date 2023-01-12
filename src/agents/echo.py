from pade.core.agent import Agent
from pade.misc.utility import display_message
from pade.behaviours.protocols import FipaRequestProtocol, TimedBehaviour
from pade.misc.common import ACLMessage, AID
from controllers.agentmanager import get_manager

class FipaRequestEchoReceiver(FipaRequestProtocol):
    def __init__(self, agent):
        super(FipaRequestEchoReceiver, self).__init__(agent=agent,message=None,is_initiator=False)
    def handle_request(self, message: ACLMessage):
        super(FipaRequestEchoReceiver, self).handle_request(message)
        display_message(self.agent.aid.localname, f"received request: {message.content}")
        reply = message.create_reply()
        reply.set_performative(ACLMessage.INFORM)
        reply.set_content(f"REPLY FROM {self.agent.aid.localname}")
        self.agent.send(reply)

"""
This agent should receive a message from the sender.
It will send a message back to the sender when it happens.
"""
class AgentEchoReceiver(Agent):
    def __init__(self, aid):
        super(AgentEchoReceiver, self).__init__(aid=aid, debug=False)
        display_message(self.aid.localname, f'Starting receiver agent {id(self)} ...')
        self.comportrequest = FipaRequestEchoReceiver(self)
        self.behaviours.append(self.comportrequest)

class FipaRequestEchoSender(FipaRequestProtocol):
    def __init__(self, agent, message=None, is_initiator=True):
        super(FipaRequestEchoSender, self).__init__(
            agent=agent,
            message=message,
            is_initiator=is_initiator
        )
    
    def handle_inform(self, message):
        super(FipaRequestEchoSender, self).handle_request(message)
        display_message(self.agent.aid.localname, f"got echo reply: {message.content}")

class WaitBeforeStartBehavior(TimedBehaviour):
    def __init__(self, agent, time, message):
        super(WaitBeforeStartBehavior, self).__init__(agent, time)
        self.message = message
        
    def on_time(self):
        super(WaitBeforeStartBehavior, self).on_time()
        self.agent.send(self.message)

"""
This agent will initiate sending a echo request from the receiver.
It will wait for a message from the receiver.
"""
class AgentEchoSender(Agent):
    def __init__(self, aid):
        super(AgentEchoSender, self).__init__(aid=aid, debug=False)
    
    def on_start(self):
        super(AgentEchoSender, self).on_start()
        display_message(self.aid.localname, f'Starting sender agent {id(self)} ...')

        # Send message to receiver
        if len(get_manager().retrieve_agent_type(AgentEchoReceiver)) == 0:
            display_message(self.aid.localname, f'No receiver agent found ...')
            return
        message = ACLMessage(ACLMessage.REQUEST)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_content("ECHO SEND")
        for receiver in get_manager().retrieve_agent_type(AgentEchoReceiver):
            message.add_receiver(AID(receiver.aid.getName()))
        self.comportrequest = FipaRequestEchoSender(self, message=message)
        self.timed_behaviour = WaitBeforeStartBehavior(self, 2, message)
        self.behaviours.append(self.comportrequest)
        self.behaviours.append(self.timed_behaviour)