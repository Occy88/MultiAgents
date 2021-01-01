import vacuumworld
from vacuumworld.vwc import action, direction
import math
from agent_util import GridState
from agent_util import get_closest_agent
import random
import json


class Follower:
    """
    Follows the closest agent as long as there is no:
    white, same colour agent that is closer.
    if a distance to a white agent is one then following is dropped
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
        print("==================FOLLOWING===============")
        agent_list, user_list = self.get_users()
        chosen_pairs = self.choose_followers(user_list, agent_list)
        self.check_present(chosen_pairs)

    def check_present(self, chosen_pairs):
        for pair in chosen_pairs:
            agent = pair[0]
            print(self.name)
            print(agent[0][0])
            if agent[0][0] == self.name:
                self.target_position = pair[1][1]

    def choose_followers(self, user_list, agent_list):
        chosen_pairs = []
        for user in user_list:
            if len(agent_list) == 0:
                break
            chosen_agent = get_closest_agent(agent_list, user[1])
            agent_list.remove(chosen_agent)
            chosen_pairs.append((chosen_agent, user))

        return chosen_pairs

    def get_users(self):
        """
        gets the location of any dirt
        that has the color of the current agent
        :return:
        """

        user_list = []
        agent_list = []
        for y, li in enumerate(self.grid_state.locations):
            for x, p in enumerate(li):
                print(p.agent)
                if p.agent is not None and (p.agent[0] == 'user'):
                    user_list.append((p.agent, (x, y)))

                if p.agent is not None and not (p.agent[0] == 'user'):
                    agent_list.append((p.agent, (x, y)))
        print(agent_list)
        print(user_list)
        return user_list, agent_list
