from objects.baseobject import BaseObject


class Actor(BaseObject):

    """ base class for all actors in game
        actors can use actions
    """

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)

    def use_action(self, action, **kw):
        if action.is_usable():
            action.do_action(self, **kw)

    @staticmethod
    def get_object(game, table, id, item, table_name):
        if "class" not in item:
            return Actor(game, table, id, table_name)
        elif item["class"] == "Player":
            return Player(game, table, id, table_name)
        elif item["class"] == "AutoActor":
            return AutoActor(game, table, id, table_name)
        else:
            return Actor(game, table, id, table_name)


class Player(Actor):

    """ player actor class """

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)
        self.game.register_player(self)


class AutoActor(Actor):

    """ actors with AI """

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)

    def choose_action(self):
        pass
