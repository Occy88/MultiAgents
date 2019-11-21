from enum import Enum
from vacuumworld.vwc import action, direction


class AgentPercepts(Enum):
    LEFT = 'l'
    RIGHT = 'r'
    TOP = 't'
    FRONT_LEFT = 'tl'
    FRONT_RIGHT = 'tr'


class AgentActions(Enum):
    TURN_LEFT = 'l'
    TURN_RIGHT = 'r'
    FORWARD = 'f'


class GridDirections(Enum):
    TOP = 'north'
    RIGHT = 'east'
    LEFT = 'west'
    BOTTOM = 'south'


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


def tie_break(agent_list,current_agent):
    """
    Given a list of agents the one
    with the highest
    number is chosen (for now)

    :param agent_list: [agent_name,agent_name...]
    :return:
    """
    current_choice = -1
    chosen_agent = None
    
    for agent in agent_list:
        agent_number = int(agent.split("-")[1])
        if agent_number > current_choice:
            chosen_agent = agent
            current_choice = agent_number
    if current_agent==chosen_agent:
        return True
    return False
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


def get_next_action(start, orientation_start, destination, orientation_destination):
    actions = []
    from vacuumworld.vwc import action, direction

    pass
