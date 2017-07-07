
def cmdparse(raw_string, player, scope):

    """
    This parses player input, and returns a dict containg at minumum:
        {"action": <action_obj>, "split_string": <split string of player text>}

    This dict can also contain:
        {"target": <target object of action>}
            ex: 
                in "move testexit" the object identified by "testexit" is
                the target

        {"object": <object object>}
            "object": in the grammatical sense
            ex:
                "take sword from spider"
                    sword = object, 
                    spider = target

        Note!
            targets/objects have strict hierarchy!

            targets contain objects / objects can only be accessed via targets

        {"other_text": <string of other text>}

            when an action takes a string as input, this is where it goes

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
    matched_action = find_action(action_name, player)
    p_output = {"action": matched_action, "split_string": split_string}

    return p_output


def find_action(action_name, player):
    for action in player.get_action_objs():
        if action_name in action.get_identifiers():
            return action


def find_target(target_name, scope):
    for g_obj in scope:
        if target_name in g_obj.get_identifiers():
            return g_obj


def find_object(object_name, target):
    for g_obj in target.get_children():
        if object_name in g_obj.get_identifiers():
            return g_obj
