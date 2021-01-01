import vacuumworld
from vacuumworld.vwc import action, direction
import math
from agent_util import AgentPercepts
from agent_util import get_closest_agent
from agent_util import GridDirections
from agent_util import get_cam_detections
from agent_util import CommunicationKeys
from agent_util import GridState
import random
import json
# import numpy as np


class GreedyExplore:
    """
    Agent has a state of the map with
    values in each cell representing how many
    cycles ago they were explored.
    Greedy explore directs the agent towards the most expensive node
    if another agent is nearer to the node (via the tie break function)
    n e.g. 10 points are taken away from the node
    """

    def __init__(self):
        # required params
        self.message = {}
        self.messages = []
        # it's fine to redeclare just to get the functions while programming.
        self.grid_state = GridState()
        self.orientation = 'none'
        self.position = (-1, -1)
        # penalty if other agent is closer:
        self.penalty = 20
        # penalty for points on an edge

    def run(self):
        print("==================GREEDILY EXPLORING===============")
        adjusted = self.get_adjusted()
        self.choose_max(adjusted)

    def get_adjusted(self):
        price_matrix = []
        i = 0
        agents = []
        for y, li in enumerate(self.grid_state.locations):
            price_matrix.append([])
            for x, p in enumerate(li):
                price_matrix[y].append(p.age)
                if p.agent is not None:
                    agents.append((p.agent, (x, y)))

        for y, li in enumerate(price_matrix):
            for x, p in enumerate(li):
                closest_agent=get_closest_agent(agents,(x,y))
                # print(self.name,closest_agent[0])
                if self.name==closest_agent[0][0]:
                        price_matrix[y][x] -= self.penalty
        # price_matrix=np.array(price_matrix)
        # print(price_matrix)
        return price_matrix

    def choose_max(self, price_matrix):
        max = 0
        # choose a max
        for y, l in enumerate(price_matrix):
            for x, p in enumerate(l):
                if p > max:
                    max = p
                    self.target_position = (x, y)
