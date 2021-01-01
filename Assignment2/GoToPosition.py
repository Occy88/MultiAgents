import vacuumworld
from vacuumworld.vwc import action, direction
import math
from agent_util import AgentPercepts
from agent_util import GridDirections, GridState
from agent_util import get_cam_detections
from agent_util import CommunicationKeys
from vacuumworld.vwagent import vwagent
from vacuumworld.vwenvironment import GridAmbient
import random
import json


class GoToPosition:
    """
    Goes to a specified position,
    If at any stage the Agent is able to clean, then it does so.
    """

    def __init__(self):
        # required params
        self.message = {}
        self.messages = []
        self.orientation = 'none'
        self.position = (-1, -1)
        self.target_position = (-1, -1)
        self.target_orientation = GridDirections.RIGHT

    def run(self):
        if self.target_position[0] < 0 or self.target_position[1] < 0:
            return
        self.goto_pos()
        self.check_clean()

    def check_clean(self):
        print(self.dirt)
        if self.dirt is not None and (self.dirt[1] == self.colour or self.colour=='white'):
            self.action = action.clean()

    def goto_pos(self):
        try:
            vector = self.target_position[0] - self.position[0], self.target_position[1] - self.position[1]
            # prioritize right direction
            if self.orientation in [GridDirections.TOP.value]:
                if vector[0] > 0:
                    self.action = action.turn(direction.right)
                    return
                if vector[0] < 0:
                    self.action = action.turn(direction.left)
                    return
                if vector[0] == 0 and vector[1] > 0:
                    self.action = action.turn(direction.right)
                    return
            if self.orientation in [GridDirections.BOTTOM.value]:
                if vector[0] > 0:
                    self.action = action.turn(direction.left)
                    return
                if vector[0] < 0:
                    self.action = action.turn(direction.right)
                    return
                if vector[0] == 0 and vector[1] < 0:
                    self.action = action.turn(direction.right)
                    return
            if self.orientation in [GridDirections.LEFT.value]:
                if vector[0] > 0:
                    self.action = action.turn(direction.right)
                    return
                if vector[0] == 0 and vector[1] < 0:
                    self.action = action.turn(direction.right)
                    return
                if vector[0] == 0 and vector[1] > 0:
                    self.action = action.turn(direction.left)
                    return
            if self.orientation in [GridDirections.RIGHT.value]:
                if vector[0] < 0:
                    self.action = action.turn(direction.right)
                    return
                if vector[0] == 0 and vector[1] < 0:
                    self.action = action.turn(direction.left)
                    return
                if vector[0] == 0 and vector[1] > 0:
                    self.action = action.turn(direction.right)
                    return
            if not vector[0] == 0 or not vector[1] == 0:
                self.action = action.move()
                return

        except Exception as e:
            print(e)
            print("____-_-_-_-_-_-_---_-_-_-_-____")
