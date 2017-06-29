# from tinydb import Query


def check_conditions(actorset, testset):
    return all(item in actorset for item in testset)


def get_in_scope(actor):
    """
        in scope means the same location as the actor,
        or with the actor as the location, and the room
        the actor is in
    """
    a_loc = actor.location
    items = actor.game.items
    actors = actor.game.actors
    actions = actor.game.actions
    a_as_loc = {"table": actor.table_name, "id": actor.id}

    container = actor.get_loc_obj()

    obj_in_scope = [container]
    for i_id, item in items.items():
        if (item.has_location() and (item.location == a_loc
                                     or item.location == a_as_loc)):
            obj_in_scope.append(item)
    for a_id, other_actor in actors.items():
        if (other_actor.has_location()
                and (other_actor.location == a_loc
                     or actor.location == a_as_loc)):
            obj_in_scope.append(other_actor)
    for ac_id, action in actions.items():
        if action.i_name in actor.actions:
            obj_in_scope.append(action)
    return obj_in_scope


def get_from_name(actor, obj_name):

        obj_in_scope = get_in_scope(actor)
        o_matching = []
        for obj in obj_in_scope:
            if (obj_name == "all" or obj_name in obj.get_identifiers()):
                o_matching.append(obj)
        return o_matching
