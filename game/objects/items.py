from objects.baseobject import BaseObject


class Item(BaseObject):
    """
        Items are objects that can present actions to the player,
        and hold a state of their own.

        Subclassing this could be use to override the "get_actions()"
        method, to only present actions under certain conditions.

    """
    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)
        self.category = "Item"

    @staticmethod
    def get_object(game, table, id, item_dict, table_name):
        return Item(game, table, id, table_name)
