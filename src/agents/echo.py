from pade.core.agent import Agent
from pade.misc.utility import display_message
from pade.behaviours.protocols import TimedBehaviour
from pade.misc.common import ACLMessage, AID
from controllers.agentmanager import get_manager

class AgentEchoReceiver(Agent):
    def __init__(self, aid):
        super(AgentEchoReceiver, self).__init__(aid=aid, debug=False)
        display_message(self.aid.localname, f'Starting receiver agent {id(self)} ...')

    def react(self, message: ACLMessage):
        super(AgentEchoReceiver, self).react(message)
        display_message(self.aid.localname, f'Message received from {message.sender.name}')

class BehaviorEchoSender(TimedBehaviour):
    def __init__(self, agent, time):
        super(BehaviorEchoSender, self).__init__(agent, time)
    
    def on_time(self):
        super(BehaviorEchoSender, self).on_time()
        self.echo(self.agent, self.message)
        
    def set_message(self, message):
        self.message = message
    
    def set_aid(self, aid):
        self.aid = aid

    def set_agent(self, agent):
        self.agent = agent

    def echo(self, agent: Agent, message: ACLMessage):
        """
        This function sends a message to the agent that sent the message.
        """
        manager = get_manager()
        targets = manager.retrieve_agent_type(AgentEchoReceiver)
        aid = agent.aid
        for target in targets:
            message.add_receiver(aid=target.aid)
            display_message(aid.localname, f'Echoing message to {target.aid.getName()} ::: {id(target)} ...')
        display_message(aid.localname, f'Echoing message to {len(targets)} agents ...')
        agent.send(message)


class AgentEchoSender(Agent):
    def __init__(self, aid):
        super(AgentEchoSender, self).__init__(aid=aid, debug=False)
    
    def on_start(self):
        super(AgentEchoSender, self).on_start()
        display_message(self.aid.localname, f'Starting sender agent {id(self)} ...')
        
        # Add TimedBehavior to echo messages every 10 seconds
        message = ACLMessage(ACLMessage.INFORM)
        message.set_content('Hello, world!')

        behavior = BehaviorEchoSender(self, 10)
        behavior.set_message(message)
        behavior.set_agent(self)
        self.behaviours.append(behavior)

        display_message(self.aid.localname, 'Echoing messages every 10 seconds ...')