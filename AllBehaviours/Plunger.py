import vacuumworld
from vacuumworld.vwc import action, direction
import math
from agent_util import GridState
from agent_util import get_agents
from agent_util import GridDirections
from agent_util import AgentPercepts
import random
import json


def dist(p1, p2):
    summation = 0
    for i, v in enumerate(p1):
        summation += (v - p2[i]) ** 2
    return math.sqrt(summation)


class Plunger:
    """
    Plunger Behaviour serves as a separator when agents are facing each other,
    it forces the agents to turn right by priority and go down one square.
    """

    def __init__(self):
        # required params
        self.message = {}
        self.messages = []
        # it's fine to redeclare just to get the functions while programming.
        self.grid_state = GridState()
        self.orientation = 'none'
        self.position = (-1, -1)
        self.plunging=False
        # penalty if other agent is closer:
        # penalty for points on an edge
        self.coordinates_turn_right={
            GridDirections.TOP.value:(1,0),
            GridDirections.RIGHT.value:(0,1),
            GridDirections.BOTTOM.value: (-1, 0),
            GridDirections.LEFT.value: (0, -1),
        }
        self.coordinates_forward={
            GridDirections.TOP.value: (0, -1),
            GridDirections.RIGHT.value: (1, 0),
            GridDirections.BOTTOM.value: (0, 1),
            GridDirections.LEFT.value: (-1, 0),
        }
        self.opposites={
            GridDirections.TOP.value:GridDirections.BOTTOM.value,
            GridDirections.BOTTOM.value:GridDirections.TOP.value,
            GridDirections.LEFT.value:GridDirections.RIGHT.value,
            GridDirections.RIGHT.value:GridDirections.LEFT.value
        }

    def sum(self,p1,p2):
        return (p1[0]+p2[0],p1[1]+p2[1])
    def run(self):
        if self.plunging:
            target_position = self.sum(self.coordinates_forward[self.orientation], self.position)
            if 0 <= target_position[0] < self.grid_size and 0 <= target_position[1] < self.grid_size:
                self.target_position = target_position
            self.plunging=False
        agents=get_agents(self.observation)
        for key,agent in agents.items():
            if self.opposites[agent[2]]==self.orientation and key==AgentPercepts.TOP.value:
                target_position=self.sum(self.coordinates_turn_right[self.orientation],self.position)
                if 0<=target_position[0]<self.grid_size and 0<= target_position[1]<self.grid_size:
                    self.target_position=target_position
                    self.plunging=True
