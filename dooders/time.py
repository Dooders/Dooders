from typing import Union
from mesa import Agent
from mesa.time import RandomActivation

class Time(RandomActivation):
    """
    Do I need a specific step function here? Because this might be broken
    """

    def __init__(self, model):
        super().__init__(model)

    def get_agent_count(self, agent_type: Union[Agent, None]=None) -> int:
        if agent_type:
            return len([agent for agent in self.agents if isinstance(agent, agent_type)])
        else:
            return len(self.agents)

    