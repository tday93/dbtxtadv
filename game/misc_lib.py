# from tinydb import Query


def check_conditions(actorset, testset):
    return all(item in actorset for item in testset)


def get_in_scope(actor):
    """
        in scope means children of the actors parent,
        the actors children,
        and usable actions
    """

    a_loc_obj = actor.get_loc_obj()
    actions = [action for id, action in actor.game.actions.items()
               if action.i_name in actor.actions]
    a_children = actor.get_children()
    l_children = a_loc_obj.get_children()

    return [a_loc_obj] + actions + a_children + l_children


def get_from_name(actor, obj_name):

        obj_in_scope = get_in_scope(actor)
        o_matching = []
        for obj in obj_in_scope:
            if (obj_name == "all" or obj_name in obj.get_identifiers()):
                o_matching.append(obj)
        return o_matching
