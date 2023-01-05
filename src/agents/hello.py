from pade.core.agent import Agent
from pade.misc.utility import display_message

class AgentHello(Agent):
    def __init__(self, aid):
        super(AgentHello, self).__init__(aid=aid)
        display_message(self.aid.localname, "Hello, world!")
