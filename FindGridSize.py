import vacuumworld
from vacuumworld.vwc import action, direction
import math
action.sp

































from agent_util import AgentPercepts
from agent_util import GridDirections
from agent_util import get_cam_detections
from vacuumworld.vwagent import vwagent
from vacuumworld.vwenvironment import GridAmbient
import random
import json

# gridambient
#  agents.append(self.init_agent(location, self.get_type(location), minds))
# ===========CONSTANTS==============
# Not for use in messages
# agent facing east, x_positive being the directed line x (0->n) n being the n*n grid

# For use in messages
# could use json
# messages are only 100 characters so we encode things with constants:
# to reduce footprint of the message...

# agent action during transmission

#
#
# ACTION_KEY = '1'
ACTION_TURN = 'a'
ACTION_MOVE = 'b'
ACTION_IDLE = 'c'

# # grid attributes (for sharing the grid state)
# GRID_STATE_KEY = '2'
# CLEAN = 'd'
# GREEN_DIRT = 'e'
# WHITE_DIRT = 'f'
# ORANGE_DIRT = 'g'
# UNKNOWN = 'h'

# position attributes
POSITION_KEY = '3'


class ExploreAndClean:
    """

    """

    def __init__(self):
        self.grid_size = -1
        # each position in the grid has a structure of:
        self.grid = []
        # the agent deactivates itself if it no longer requires to move
        self.active = True
        # message to broadcast at each turn
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

    def should_clean(self):
        print(self.observation.center)

    def find_grid_size(self):
        cam_results = get_cam_detections(self.observation)

        # default message to send,
        # ============ CONDITIONS FOR MAX EDGE BEING FOUND ===============
        # conditions either of top corners of the agent detecting the maximal edge (y max, x max)
        if (AgentPercepts.RIGHT not in cam_results and self.orientation in [GridDirections.TOP.value,
                                                                            GridDirections.RIGHT.value]) \
                or (AgentPercepts.LEFT not in cam_results and self.orientation in [GridDirections.LEFT.value,
                                                                                   GridDirections.BOTTOM.value]) \
                or (AgentPercepts.TOP not in cam_results and self.orientation in [GridDirections.BOTTOM.value,
                                                                                  GridDirections.RIGHT.value]):
            self.max_edge_found()
            print('t1')
            return
        # ============ CONDITIONS FOR AGENT TO TURN ================
        # if max coord is x and not facing x_positive: turn towards x_positive
        if self.position[0] > self.position[1] and self.orientation != GridDirections.RIGHT.value:
            print(self.orientation)
            print(GridDirections.RIGHT.value)
            d = direction.left
            if self.orientation == GridDirections.TOP.value:
                d = direction.right
            self.action = action.turn(d)
            print("t2")
            return
        # if max coord is y and not facing y_positive: turn towards y_positive
        elif self.position[1] > self.position[0] and self.orientation != GridDirections.BOTTOM.value:
            d = direction.right
            if self.orientation == GridDirections.LEFT.value:
                d = direction.left
            self.action = action.turn(d)
            print("t3")

            return
        elif self.position[0] == self.position[1] and self.orientation not in [GridDirections.RIGHT.value,
                                                                               GridDirections.BOTTOM.value]:
            if self.orientation == GridDirections.TOP.value:
                self.action = action.turn(direction.right)
                print("t4")
            else:
                self.action = action.turn(direction.left)
                print("t5")

            return
        if AgentPercepts.TOP in cam_results:
            print("t6")

            self.action = action.move()

    def decide(self):
        # default messge to broadcast in case anything is required?
        self.message = {}

        if not self.active:
            self.action = action.idle()
            return self.validate_actions()
        if self.grid_size < 0:
            self.find_grid_size()

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
        error = json.dumps({'error': 'message too long'})
        try:
            # set default message:
            act_transmit = ACTION_IDLE
            turn_instance = action.turn(direction.right)
            move_instance = action.move()

            if isinstance(self.action, type(turn_instance)):
                act_transmit = ACTION_TURN
            elif isinstance(self.action, type(move_instance)):
                act_transmit = ACTION_MOVE

            self.message.update({'position': self.position, 'action': act_transmit})
            m = json.dumps(self.message)
        except Exception as e:
            print(e)
            m = error
        if m.__len__() > 100:
            print("LONG MESSAGE: ", m)
            m = error
            action.speak()
        return self.action, action.speak(m)

    def max_edge_found(self):
        """
        Max edge has been found,
        set the max edge,
        deactivate

        :return: action (idle, broadcast grid size)
        """
        self.grid_size = max(self.position) + 1
        self.active = False
        self.action = action.idle()
        self.message.update({'grid_size': self.grid_size})

    def load_message(self, message):
        try:
            return json.loads(message.content)
        except Exception as e:
            print(e)
            return {}

    def should_stay_active(self):
        """
        should deactivate if
        the current max coordinate (x or y) -1 is the greater or equal than any of the broadcasted ones
        (-1) and the agent broadcasting is moving (not turning)

        i.e. another agent is closer to the solution
        :param messages:
        :return:
        """
        # other agents in better conditions to search for relevant edge
        for m in self.messages:
            message = self.load_message(m)
            if 'position' in message:
                if max(message['position']) > max(self.position) - 1 and message['action'] == ACTION_MOVE:
                    self.active = False
                    break
        # grid size has been updated
        if self.grid_size > -1:
            self.active = False

    def set_grid_size(self):
        for m in self.messages:
            message = self.load_message(m)
            if 'grid_size' in message and message['grid_size'] != self.grid_size:
                self.grid_size = message['grid_size']

    def update_grid(self):
        """
        Each message contains all observations
        of each agent
        We update the current state of the grid
        to the state of what the agent which sent the message has seen.
        :return:
        """
        for m in self.messages:
            message = self.load_message(m)
            self.grid[message['position']]['agent'] = message['name']

    def revise(self, observation, messages):
        # OBSERVATIONS:
        # SET VARIABLES (no api provided so I need to know what there is and where.)
        # print('___________________________')
        # print(messages)
        self.observation = observation
        self.position = observation.center.coordinate
        self.colour = observation.center.agent.colour
        self.orientation = observation.center.agent.orientation
        self.dirt = observation.center.dirt
        self.name = observation.center.agent.name
        # MESSAGES
        # LOAD THE MESSAGES
        self.messages = messages
        # ANY ACTIONS WHICH DEPEND ON MESSAGES
        # self.update_grid()

        self.set_grid_size()
        self.should_stay_active()


# more belief revision
vacuumworld.run(ExploreAndClean(), skip=True)
