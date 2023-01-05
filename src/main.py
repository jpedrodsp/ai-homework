from controllers.agentmanager import get_manager
# from agents.hello import AgentHello
# from agents.echo import AgentEchoReceiver, AgentEchoSender
from agents.orchestrator import AgentOrchestrator
from agents.calculator import AgentSumCalculator, AgentSubtractionCalculator, AgentMultiplicationCalculator, AgentDivisionCalculator, AgentExponentiationCalculator, AgentSquareRootCalculator

if __name__ == '__main__':
    manager = get_manager()
    # manager.create_agent(agent_type=AgentHello)
    # manager.create_agent(agent_type=AgentEchoReceiver)
    # manager.create_agent(agent_type=AgentEchoReceiver)
    # manager.create_agent(agent_type=AgentEchoSender)
    calculators = [AgentSumCalculator, AgentSubtractionCalculator, AgentMultiplicationCalculator, AgentDivisionCalculator, AgentExponentiationCalculator, AgentSquareRootCalculator]
    for calculator in calculators:
        manager.create_agent(agent_type=calculator)
    manager.create_agent(agent_type=AgentOrchestrator)
    manager.start_loop()