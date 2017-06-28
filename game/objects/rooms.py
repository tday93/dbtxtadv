import misc_lib
from objects.baseobject import BaseObject


class Room(BaseObject):

    """ a room is an object without a location,
        and (probably) exits to other locations
    """

    def __init__(self, game, table, id, table_name):
        super().__init__(game, table, id, table_name)

    @staticmethod
    def get_object(game, table, id, item, table_name):
        return Room(game, table, id, table_name)

    def describe(self, actor):
        if self.is_describable(actor):
            desc_txt = []
            for description in self.descriptions:
                if misc_lib.check_conditions(actor.get_flags(),
                                             description["conditions"]):
                    desc_txt.append(description["description"])
            return (self.format_description(desc_txt)
                    + self.describe_exits(actor))
        else:
            return None

    def describe_exits(self, actor):
        for exit in self.exits:
            exit_desc_block = "  [Exit] <{}>: \n".format(exit["d_name"])
            for desc in exit["descriptions"]:
                if misc_lib.check_conditions(actor.get_flags(),
                                             desc["conditions"]):
                    exit_desc_block = (exit_desc_block
                                       + "    {}\n".format(
                                           desc["description"]))
        return exit_desc_block
