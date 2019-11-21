import vacuumworld
from vacuumworld.vwc import action, direction
import math
from agent_util import GridState
from agent_util import get_closest_agent
import random
import json


def dist(p1, p2):
    summation = 0
    for i, v in enumerate(p1):
        summation += (v - p2[i]) ** 2
    return math.sqrt(summation)


class Cleaner:
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
        self.penalty = 10
        # penalty for points on an edge

    def run(self):
        print("==================CLEANING===============")
        dirt_list, agent_list = self.get_dirt()
        chosen_pairs = self.choose_dirt(dirt_list, agent_list)
        self.check_present(chosen_pairs)

    def check_present(self, chosen_pairs):
        for pair in chosen_pairs:
            agent = pair[0]
            if agent[0][0] == self.name:
                self.target_position = pair[1][1]

    def choose_dirt(self, dirt_list, agent_list):
        chosen_pairs = []
        for dirt in dirt_list:
            if len(agent_list) == 0:
                break
            chosen_agent = get_closest_agent(agent_list, dirt[1])
            agent_list.remove(chosen_agent)
            chosen_pairs.append((chosen_agent, dirt))

        return chosen_pairs

    def get_dirt(self):
        """
        gets the location of any dirt
        that has the color of the current agent
        :return:
        """

        dirt_list = []
        agent_list = []
        for y, li in enumerate(self.grid_state.locations):
            for x, p in enumerate(li):

                if p.dirt is not None and (p.dirt[1] == self.colour or self.colour=='white'):
                    dirt_list.append((p.dirt, (x, y)))

                if p.agent is not None and (p.agent[1] == self.colour or self.colour=='white'):
                    agent_list.append((p.agent, (x, y)))
        return dirt_list, agent_list
