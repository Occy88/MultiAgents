import vacuumworld
from vacuumworld.vwc import action, direction
import tkinter

class GroupAgents:
    def __init__(self):
        self.grid_size = -1


    # if no agents around pick a random direction a go there
    # if an agent around then idle
    def detect_agent(self):
        pass
    def decide(self):
        print(self.observation.left)
        if self.observation.left is not None:
            print(self.observation.left.agent)
            print(self.observation.left.dirt)
            print(self.observation.left[0])
        return action.idle()

    def revise(self, observation, messages):
        self.observation = observation


vacuumworld.run(MyMind())
