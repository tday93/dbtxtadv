from objects.baseobject import BaseObject


class Actor(BaseObject):

    """ base class for all actors in game
        actors can use actions
    """

    def __init__(self, game, table, id):
        super().__init__(game, table, id)

    def use_action(self, action, **kw):
        if action.is_usable():
            action.do_action(self, **kw)

    @staticmethod
    def get_object(game, table, id, item):
        if "class" not in item:
            return Actor(game, table, id)
        elif item["class"] == "Player":
            return Player(game, table, id)
        elif item["class"] == "AutoActor":
            return AutoActor(game, table, id)
        else:
            return Actor(game, table, id)


class Player(Actor):

    """ player actor class """

    def __init__(self, game, table, id):
        super().__init__(game, table, id)
        self.game.register_player(self)


class AutoActor(Actor):

    """ actors with AI """

    def __init__(self, game, table, id):
        super().__init__(game, table, id)

    def choose_action(self):
        pass
