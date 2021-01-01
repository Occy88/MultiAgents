import vacuumworld
from vacuumworld.vwc import action, direction
import math
from agent_util import AgentPercepts
from agent_util import GridDirections
from agent_util import get_cam_detections
from agent_util import CommunicationKeys
from vacuumworld.vwagent import vwagent
from vacuumworld.vwenvironment import GridAmbient
import random
import json


class FindGridSizeMind:
    """

    """

    def __init__(self):
        # required params
        self.message = {}
        self.messages = []
        self.orientation = 'none'
        self.observation = []
        self.position = (-1, -1)

    def run(self):
        if self.check_grid_size_recieved():
            return
        self.perform_actions()

    def perform_actions(self):
        cam_results = get_cam_detections(self.observation)

        # default message to send,
        # ============ CONDITIONS FOR MAX EDGE BEING FOUND ===============
        # conditions either of top corners of the agent detecting the maximal edge (y max, x max)
        if (AgentPercepts.RIGHT.value not in cam_results and self.orientation in [GridDirections.TOP.value,
                                                                            GridDirections.RIGHT.value]) \
                or (AgentPercepts.LEFT.value not in cam_results and self.orientation in [GridDirections.LEFT.value,
                                                                                   GridDirections.BOTTOM.value]) \
                or (AgentPercepts.TOP.value not in cam_results and self.orientation in [GridDirections.BOTTOM.value,
                                                                                  GridDirections.RIGHT.value]):
            self.max_edge_found()
            return
        # ============ CONDITIONS FOR AGENT TO TURN ================
        # if max coord is x and not facing x_positive: turn towards x_positive
        if self.position[0] > self.position[1] and self.orientation != GridDirections.RIGHT.value:
            d = direction.left
            if self.orientation == GridDirections.TOP.value:
                d = direction.right
            self.action = action.turn(d)
            return
        # if max coord is y and not facing y_positive: turn towards y_positive
        elif self.position[1] > self.position[0] and self.orientation != GridDirections.BOTTOM.value:
            d = direction.right
            if self.orientation == GridDirections.LEFT.value:
                d = direction.left
            self.action = action.turn(d)
            return
        elif self.position[0] == self.position[1] and self.orientation not in [GridDirections.RIGHT.value,
                                                                               GridDirections.BOTTOM.value]:
            if self.orientation == GridDirections.TOP.value:
                self.action = action.turn(direction.right)
            else:
                self.action = action.turn(direction.left)

            return
        if AgentPercepts.TOP.value in cam_results:
            self.action = action.move()

    def check_grid_size_recieved(self):
        for m in self.messages:
            m = self.load_message(m)
            if CommunicationKeys.GRID_SIZE.value in m and m[CommunicationKeys.GRID_SIZE.value] != self.grid_size:
                self.grid_size = m[CommunicationKeys.GRID_SIZE.value]
                return True

        return False




    def max_edge_found(self):
        """
        Max edge has been found,
        set the max edge,
        deactivate

        :return: action (idle, broadcast grid size)
        """
        self.grid_size = max(self.position) + 1
        self.message.update({CommunicationKeys.GRID_SIZE.value: self.grid_size})
