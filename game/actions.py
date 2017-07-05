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
        print(response)
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


class Move(Action):

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)

    def run_action(self, actor, **kw):
        t_e_name = kw["split_string"][1]
        exits = actor.get_loc_obj().get_exits()
        for exit in exits:
            if t_e_name == exit["i_name"] or t_e_name == exit["d_name"]:
                if check_conditions(actor.get_flags(), exit["usable"]):
                    transforms.move(actor, exit["leads_to"])

    def post_action(self, actor, **kw):
        new_room = actor.get_loc_obj()
        room_desc = new_room.describe(actor)
        return [room_desc]


class Attack(Action):

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)

    def run_action(self, actor, **kw):
        target_name = kw["split_string"][1]
        t_obj = get_from_name(actor, target_name)
        if t_obj.is_attackable():
            self.do_combat(actor, t_obj)

    def do_combat(self, actor, target):
        a_atk = actor.stats["atk"]
        t_def = target.stats["def"]
        dmg = a_atk - t_def
        transforms.damage(target, dmg)
