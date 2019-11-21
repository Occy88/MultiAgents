from enum import Enum
from vacuumworld.vwc import action, direction

import math


# RESOLVED AS SINGLE CHARACTERS TO SAVE COMMUNICATION BANDWIDTH
class AgentPercepts(Enum):
    LEFT = '1'
    RIGHT = '2'
    TOP = '3'
    FRONT_LEFT = '4'
    FRONT_RIGHT = '5'


class AgentActions(Enum):
    TURN_LEFT = '6'
    TURN_RIGHT = '7'
    FORWARD = '8'


class CommunicationKeys(Enum):
    GRID_SIZE = 'a'
    POSITION = 'b'
    NEXT_ACTION = 'c'
    OBSERVATIONS = 'd'


class GridDirections(Enum):
    """
    Cannot be modified, (used to find orientation)
    """
    TOP = 'north'
    RIGHT = 'east'
    LEFT = 'west'
    BOTTOM = 'south'


class GridLocation:
    def __init__(self):
        self.dirt = None
        self.agent = None
        self.currently_observed = False
        self.age = 0

    def encode(self):
        agent_details_to_send = self.agent
        dirt_details_to_send = self.dirt
        if self.agent is not None:
            agent_details_to_send = [self.agent[0].split('-')[1], self.agent[1]]
        if self.dirt is not None:
            dirt_details_to_send = [self.dirt[0].split('-')[1], self.dirt[1]]
        return [agent_details_to_send, dirt_details_to_send]

    def decode(self, observation):
        self.agent = observation[1]
        self.dirt = observation[2]
        if observation[1] is not None:
            self.agent = ['A-' + str(observation[1][0]), observation[1][1]]
        if observation[2] is not None:
            self.dirt = ['D-' + str(observation[2][0]), observation[2][1]]
        self.currently_observed = True
        self.age = 0

    def update(self):
        self.age += 1

    def draw(self):
        string = '|'
        if self.dirt is not None:
            string += 'D'
        else:
            string += ' '
        if self.agent is not None:
            string += self.agent[0].split('-')[1]
        else:
            string += ' '
        if self.currently_observed:
            string += 'X'
        else:
            string += ' '
        age = str(self.age)
        age = age.ljust(3)
        print(string + ' ' + age, end='')


class GridState:
    def __init__(self):
        self.size = 0
        self.locations = []

    def set_size(self, n):
        self.size = n
        self.locations = []
        for y in range(n):
            self.locations.append([])
            for x in range(n):
                self.locations[y].append(GridLocation())

    def update(self):
        for y in self.locations:
            for l in y:
                l.update()

    def decode(self, observations):
        """
        [[7, 3], ['a-1', 'orange', 'north'], None], [[6, 3], None, None], [[7, 2], ['a-2', 'orange', 'north'], None], [[6, 2], None, None]]
        :param d:
        :return:
        """

        try:
            for obs in observations:
                coords = obs[0]
                x = int(coords[0])
                y = int(coords[1])
                cell = self.locations[y][x]
                cell.decode(obs)

        except Exception as e:
            print(e)

    def encode_location(self, x, y):
        """
        returns position in the format of an observation
        :param x:
        :param y:
        :return:
        """
        l = self.locations[y][x]
        return [[x, y]] + l.encode()

    def draw(self):
        for l in self.locations:
            for location in l:
                location.draw()
            print('')


def split_grid(grid_size):
    """
    Splits grid into points that need to be explored to cover the
    whole grid.
    :param grid_size:
    :return:
    """
    points_to_explore = []
    for y in range(1, grid_size):
        points_to_explore.append([])
        for x in range(grid_size):
            points_to_explore[y].append(GridLocation())
            pass
        y += 3
    return points_to_explore


def get_cam_detections(observation):
    """
    returns all squares seen by the camera
    :param observation:
    :return:[(obs,observation.direction)]
    """
    obs_dir_list = {}

    if observation.left is not None:
        obs_dir_list[AgentPercepts.LEFT.value] = observation.left

    if observation.forwardleft is not None:
        obs_dir_list[AgentPercepts.FRONT_LEFT.value] = observation.forwardleft

    if observation.forward is not None:
        obs_dir_list[AgentPercepts.TOP.value] = observation.forward

    if observation.forwardright is not None:
        obs_dir_list[AgentPercepts.FRONT_RIGHT.value] = observation.forwardright

    if observation.right is not None:
        obs_dir_list[AgentPercepts.RIGHT.value] = observation.right

    return obs_dir_list


def get_closest_agent(agent_list, point):
    closest_distance = math.inf
    if agent_list is None or len(agent_list)<=0:
        return
    closest_agent = agent_list[0]
    for agent in agent_list:
        agent_pos = agent[1]
        distance = dist(agent_pos, point)
        if distance < closest_distance:
            closest_distance = distance
            closest_agent = agent
        if distance == closest_distance:
            if int(agent[0][0].split('-')[1]) > int(closest_agent[0][0].split('-')[1]):
                closest_agent = agent
    return closest_agent


def get_agents(observation):
    """
    Gets all agents in the observation
    returns a list
    :param observation:
    :return: [(agent,observation.direction)...]
    """
    directions = get_cam_detections(observation)
    agents = {}
    for key, val in directions.items():
        if val.agent is not None:
            agents[key] = val.agent
    return agents


def dist(p1, p2):
    summation = 0
    for i, v in enumerate(p1):
        summation += (v - p2[i]) ** 2
    return math.sqrt(summation)
