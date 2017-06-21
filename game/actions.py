from objects.baseobject import BaseObject


class Action(BaseObject):

    """
        action base class

    """

    def __init__(self, game, table, id):
        super().__init__(game, table, id)

    def do_action(self, actor, **kw):
        """
            this is what is called when this
            action is performed
        """
        pass

    @staticmethod
    def get_action(game, table, id, action_dict):
        if action_dict["class"] == "TestAction":
            return TestAction(game, table, id)


class TestAction(Action):

    def __init__(self, game, table, id):
        super().__init__(game, table, id)

    def do_action(self, actor, **kw):
        actor.game.player_output(" ".join(kw["split_string"]))
