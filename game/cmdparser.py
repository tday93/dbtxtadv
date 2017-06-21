

def cmdparse(raw_string, player):

    """
    This parses player input

    Args:
        raw_string = stripped text entered by the player
        player = the player object of the player who entered this command

    Notes:

        commands are expected to be space separated alphanums

        command format is as follows:

            cmdname [args]
    """
    split_string = raw_string.split(" ")
    action_name = split_string[0]
    possible_actions = get_possible_actions(player)
    matched_action = match_actions(possible_actions, action_name)
    return matched_action, split_string


def match_actions(p_actions, action_name):
    for action in p_actions:
        if any(action.i_name == action_name, action.d_name == action_name,
               action_name in action.aliases):
            return action


def get_possible_actions(player):
    p_actions = []
    for action_name in player.actions:
        for action in player.game.actions:
            if action.i_name == action_name and action.is_usable(player):
                p_actions.append(action)
    return p_actions
