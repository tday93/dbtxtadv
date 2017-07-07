from objects.baseobject import BaseObject
import transforms
from misc_lib import get_from_name, check_conditions


class Action(BaseObject):

    """
        action base class

    """

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)
        self.category = "Action"

    def do_action(self, actor, **kw):
        response = []
        pre = self.pre_action(actor, **kw)
        act = self.run_action(actor, **kw)
        post = self.post_action(actor, **kw)
        if pre:
            response = response + pre
        if act:
            response = response + act
        if post:
            response = response + post
        self.game.player_ouput(response)

    def pre_action(self, actor, **kw):
        """ called before the action is performed"""
        pass

    def run_action(self, actor, **kw):
        """ the actual action"""
        pass

    def post_action(self, actor, **kw):
        """ called after the action is performed """
        pass

    @staticmethod
    def get_action(game, table, id, action_dict, table_name):
        if action_dict["class"] == "TestAction":
            return TestAction(game, table, id, table_name)
        elif action_dict["class"] == "Examine":
            return Examine(game, table, id, table_name)
        elif action_dict["class"] == "Move":
            return Move(game, table, id, table_name)
        elif action_dict["class"] == "Attack":
            return Attack(game, table, id, table_name)
        elif action_dict["class"] == "Get":
            return Get(game, table, id, table_name)
        elif action_dict["class"] == "Take":
            return Take(game, table, id, table_name)
        elif action_dict["class"] == "Inspect":
            return Inspect(game, table, id, table_name)


class TestAction(Action):

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)

    def run_action(self, actor, **kw):
        return " ".join(kw["split_string"])


class Examine(Action):

    """ calls an objects Describe method and returns results """

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)

    def run_action(self, actor, **kw):
        obj_name = kw["split_string"][1]
        # get other objects in scope
        matching_obj_in_scope = get_from_name(actor, obj_name)
        descriptions = []
        for obj in matching_obj_in_scope:
            if obj.is_describable(actor):
                descriptions.append(obj.describe(actor))
        return descriptions


class Inspect(Action):

    """
        returns descriptions of a targets child objects

    """

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)

    def run_action(self, actor, **kw):
        t_name = kw["split_string"][1]
        target = get_from_name(actor, t_name)[0]
        if not target.is_inspectable(actor):
            return ["You cannot inspect that"]
        descriptions = []
        for obj in target.get_children():
            descriptions.append(obj.describe(actor))
        return descriptions


class Move(Action):

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)

    def run_action(self, actor, **kw):
        t_e_name = kw["split_string"][1]
        exits = actor.get_loc_obj().get_exits()
        for exit in exits:
            if (t_e_name == exit["i_name"] or t_e_name == exit["d_name"]
                    or t_e_name in exit["aliases"]):
                if check_conditions(actor.get_flags(), exit["usable"]):
                    transforms.move(
                        actor, self.game.get_game_object(exit["leads_to"]))

    def post_action(self, actor, **kw):
        new_room = actor.get_loc_obj()
        room_desc = new_room.describe(actor)
        return [room_desc]


class Attack(Action):

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)

    def run_action(self, actor, **kw):
        target_name = kw["split_string"][1]
        t_obj = get_from_name(actor, target_name)[0]
        if t_obj.is_attackable(actor):
            return [self.do_combat(actor, t_obj)]

    def do_combat(self, actor, target):
        a_atk = actor.stats["atk"]
        t_def = target.stats["def"]
        dmg = a_atk - t_def
        transforms.damage(target, dmg)
        msg = "\n {} did {} damage to the {}!".format(actor.d_name,
                                                      dmg, target.d_name)
        return msg

    def post_action(self, actor, **kw):
        target = get_from_name(actor, kw["split_string"][1])[0]
        if target.is_attackable(actor):
            if target.stats["hp"] <= 0:
                target.flags.append("lootable")
                target.flags.append("dead")
                target.save_values()
                return ["\n You killed the {}".format(target.d_name)]


class Get(Action):

    """ moves an item in the room into the actors inventory
        what this means functionally is changing its location
        field to the actor

    """

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)

    def do_action(self, actor, **kw):

        item_name = kw["split_string"][1]
        item_obj = get_from_name(actor, item_name)[0]
        response = []
        pre = self.pre_action(actor, item_obj, **kw)
        act = self.run_action(actor, item_obj, **kw)
        post = self.post_action(actor, item_obj, **kw)
        if pre:
            response = response + pre
        if act:
            response = response + act
        if post:
            response = response + post
        self.game.player_ouput(response)

    def pre_action(self, actor, item_obj, **kw):
        # does anything need to happen here??
        pass

    def run_action(self, actor, item_obj, **kw):
        # move the item into the actors inventory
        if not item_obj.is_gettable(actor):
            return ["You cannot get that"]
        transforms.move(item_obj, actor)
        return ["You got {}".format(item_obj.d_name)]

    def post_action(self, actor, item_obj, **kw):
        # report success maybe? might not be needed
        pass


class Take(Action):

    """
        takes an item from some other game object and gives it to
        the taking actor

    """

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)

    def run_action(self, actor, **kw):
        item_name = kw["split_string"][1]
        target_name = kw["split_string"][3]
        t_obj = get_from_name(actor, target_name)[0]
        if not t_obj.is_lootable(actor):
            return ["You cannot take from this {}".format(t_obj.d_name)]
        for child in t_obj.get_children():
            if item_name in child.get_identifiers():
                transforms.move(child, actor)
                return ["You took the {} from the {}".format(child.d_name,
                                                             t_obj.d_name)]
