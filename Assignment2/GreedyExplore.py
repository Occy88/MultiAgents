import vacuumworld
from vacuumworld.vwc import action, direction
import math
from agent_util import AgentPercepts
from agent_util import get_closest_agent
from agent_util import GridDirections
from agent_util import get_cam_detections
from agent_util import CommunicationKeys
from agent_util import GridState
from agent_util import dist
import random
import json


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
        for x, li in enumerate(self.grid_state.locations):
            price_matrix.append([])
            for y, p in enumerate(li):
                price_matrix[x].append(p.age)
                if p.agent is not None:
                    agents.append((p.agent, (x, y)))

        for x, li in enumerate(price_matrix):
            for y, p in enumerate(li):
                closest_agent = get_closest_agent(agents, (x, y))
                # print(self.name,closest_agent[0])
                # distance=dist(self.position,(x,y))
                # price_matrix[y][x] += int(distance)
                price_matrix[x][y] **= 3
                if self.name == closest_agent[0][0]:
                    price_matrix[x][y] *= self.penalty
                else:
                    price_matrix[x][y] -= self.penalty

        # convert each node as the sum of it's surrounding nodes
        neighbours = [(-1, -1), (-1, 0), (0, -1), (0, 0), (0, 1), (1, 1), (1, 0)]
        new_m = price_matrix.copy()
        for x, li in enumerate(price_matrix):
            for y, p in enumerate(li):
                for n in neighbours:
                    n_p = (x + n[0], y + n[1])
                    if 0 <= n_p[0] < self.grid_size and 0 <= n_p[1] < self.grid_size:
                        new_m[x][y] += price_matrix[x][y]

        print(self.colour)
        return new_m
    def transpose(self,matrix):
        return zip(*matrix)

    def choose_max(self, price_matrix):
        max = -math.inf
        # choose a max
        price_matrix=self.transpose(price_matrix)
        for x, l in enumerate(price_matrix):
            for y, p in enumerate(l):
                if p > max:
                    max = p
                    max_list = [(dist(self.position, (x, y)), max, (x, y))]
                elif p == max:
                    max_list.append((dist(self.position, (x, y)), max, (x, y)))
        max_list.sort()
        if len(max_list) == 0:
            self.target_position = (int(self.grid_size / 2), int(self.grid_size / 2))
        else:
            self.target_position = max_list[0][2]
        print(self.target_position)
