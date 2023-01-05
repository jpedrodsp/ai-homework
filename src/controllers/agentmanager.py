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