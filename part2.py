import vacuumworld
from vacuumworld.vwc import action, direction, size
from agent_util import get_cam_detections, get_agents
from agent_util import AgentPercepts
from agent_util import GridDirections
from vacuumworld.vwagent import vwagent
from vacuumworld.vwenvironment import GridAmbient
from MappingMind import MappingMind
import random
import json
import zlib
from FindGridSizeMind import FindGridSizeMind
from GreedyExplore import GreedyExplore
from Follower import Follower
from GoToPosition import GoToPosition
from Cleaner import Cleaner
import base64
import struct
from Plunger import Plunger
# position attributes
POSITION_KEY = '3'

# action.speak()
key_dict = {
    'A': 'user',
    'B': 'orange',
    'C': 'white',
    'D': 'green',
    'E': 'dirt',
    'F': 'agent',
    'G': 'colour',
    'H': 'name',
    'I': 'north',
    'J': 'west',
    'K': 'east',
    'L': 'south',
    'M': 'west',
    '"N"': 'null',
    '"O"': 'None',
    'N': 'None',
    'O': 'None'
}


class TestMind(FindGridSizeMind, MappingMind, GreedyExplore, GoToPosition, Cleaner,Plunger):
    """

    """

    def __init__(self):
        self.grid_size = -1
        self.message = {}
        self.action = action.idle()
        self.observation = []
        self.position = (-1, -1)
        self.colour = 'none'
        self.orientation = 'none'
        self.dirt = 'none'
        self.name = 'none'
        # MESSAGES
        # LOAD THE MESSAGES
        self.messages = []

        FindGridSizeMind.__init__(self)
        # MAPPING MAP MAX BANDWIDTH OF 80
        MappingMind.__init__(self)
        GreedyExplore.__init__(self)
        Cleaner.__init__(self)
        GoToPosition.__init__(self)
        Plunger.__init__(self)

    def decide(self):
        # default messge to broadcast in case anything is required?
        print('------------', 'AGENT: ', self.name, '---------------')
        self.message = {}
        self.action = action.idle()
        # Conditions to Find Grid Size
        if self.grid_size < 0:
            FindGridSizeMind.run(self)
        if self.grid_size > 0:
            # order by inverse precedence (most important last (for any classes that affect actions)
            # keeps the current state of the map and the
            # age (number fo cycles since update)
            MappingMind.run(self)
            # Places a value on each cell by how long ago it was explored and cubes it (older exponentially more expensive)
            # and if there are other agents that are closer there is a penalty.
            # sums each cell to the value of it's surrounding cells (how much does the robot wanna go there)
            # Robot targets the closest most expensive cell
            GreedyExplore.run(self)
            # If there is a cell to clean, checks if there are other bots
            # closer that are able to clean it, if there are then abandons cleaning
            Cleaner.run(self)
            # Resolves a face to face argument, forces the next to moves to be a turn and
            # forward to the right if possible.
            # Follower.run(self
            Plunger.run(self)
            # goes to the specified self.target_position, viea the fewest
            # possible moves, prioritises x first then y.
            GoToPosition.run(self)

        return self.validate_actions()

    def validate_actions(self):
        """
        update message with default parameters (position, action) (this is for this mind only)
        Check length of message,
        any other checks,
        :param action_func: action to execute
        :param message_dict:  message dictionary to broadcast
        :return: action.movement, action.speak
        """
        error = ['error', 'error message too long']
        try:
            m = json.dumps(self.message, separators=(',', ':'))
            # CASE IS NOT PRESERVED IN ORDER TO PREVENT CLASH WITH KEY DICT
            # print("--------MESSAGE SENT: --------")

            m = m.lower()
            for key, val in key_dict.items():
                if val is None:
                    continue
                m = m.replace(val, key)
            lists = []
            m = json.loads(m)
            for key, val in m.items():
                lists.append([key, val])
            s = json.dumps(lists)
            s = s.replace(' ', '')
            code_bytes = zlib.compress(s.encode('utf-8'))
            code_lat1 = code_bytes.decode('latin-1')

            m = code_lat1
            print(size(m))
        except Exception as e:
            print(e)
            m = error

        if m.__len__() > 100:
            print("\n=======================LONG MESSAGE:=================\n ", m)
            m = error

        return self.action, action.speak(m)

    def load_message(self, message):
        try:
            # print("===============LOADED+========================")
            content = message.content
            code_bytes_compressed = content.encode('latin-1')
            content_str = zlib.decompress(code_bytes_compressed)
            content = content_str.decode('utf-8')
            for key, val in key_dict.items():
                content = content.replace(key, val)
            lists = json.loads(content)
            m = {}
            for l in lists:
                m.update({l[0]: l[1]})
            return m
        except Exception as e:
            print(e)
            return {}

    def revise(self, observation, messages):
        self.observation = observation
        self.position = observation.center.coordinate
        self.colour = observation.center.agent.colour
        self.orientation = observation.center.agent.orientation
        self.dirt = observation.center.dirt
        self.name = observation.center.agent.name
        self.messages = messages
        # print("MESSAGES: ")
        # print(self.messages)


# more belief revision
vacuumworld.run(TestMind())
