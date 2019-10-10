def get_cam_detections(observation):
    """
    returns all squares seen by the camera in a list
    from left to right
    :param observation:
    :return:
    """
    obs_dir_list=[]
    if observation.left is not None:
        obs_dir_list.append(observation.left)
    if observation.forwardleft is not None:
        obs_dir_list.append(observation.forwardleft)
    if observation.forward is not None:
        obs_dir_list.append(observation.forward)

    if observation.forwardright is not None:
        obs_dir_list.append(observation.forwardright)


def get_agents(observation):
    """
    Gets all agents in the observation
    returns a list
    :param observation:
    :return:
    """

    if observation.right:
        pass

    if observation.forwardright:
        pass
