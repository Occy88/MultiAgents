import vacuumworld
from vacuumworld.vwc import action, direction,size
import math
from agent_util import AgentPercepts
from agent_util import GridDirections
from agent_util import get_cam_detections
from agent_util import GridState
from agent_util import CommunicationKeys
from vacuumworld.vwagent import vwagent
from vacuumworld.vwenvironment import GridAmbient
import random
import json


class MappingMind:
    """
    Sends all observed squares at each cycle,
    updates all received observations at each cycle
    """

    def __init__(self):
        # required params
        self.message = {}
        self.grid_state = []
        self.messages = []
        self.orientation = 'none'
        self.observation = []
        self.position = (-1, -1)
        self.grid_state = GridState()
        self.observations_to_send = {}

    def run(self):
        # cannot map if grid size is less than zero

        if self.grid_size <= 0:
            return
        if not self.grid_state.size == self.grid_size:
            self.init_grid_state()
        self.update_map()
        self.grid_state.update()
        self.send_observations()
        # self.send_messages()
        # self.perform_actions()

    def init_grid_state(self):
        self.grid_state.set_size(self.grid_size)

    def send_observations(self):
        self.message.update({CommunicationKeys.OBSERVATIONS.value: self.observations_to_send})

    def update_map(self):
        """
        From own observation and messages
        map state is updated.
        :return:
        """
        self.observations_to_send = []
        # set all currently observed to false:
        # and remove all agents, as locations are non-static
        for y in self.grid_state.locations:
            for x in y:
                x.currently_observed = False
                x.agent=None
        for o in self.observation:
            coord = o[0]
            x = coord[0]
            y = coord[1]
            location = self.grid_state.locations[y][x]
            location.agent = o[1]
            location.dirt = o[2]
            location.age=0
            location.currently_observed = True
            self.observations_to_send.append(self.grid_state.encode_location(x, y))
        for m in self.messages:
            message = self.load_message(m)
            observations = message.get(CommunicationKeys.OBSERVATIONS.value)
            if observations is None:
                break
            self.grid_state.decode(observations)
        # self.grid_state.draw()
        pass
