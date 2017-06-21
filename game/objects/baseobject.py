import misc_lib


class BaseObject(object):

    """

        base class for all ingame objects

        handles connection to tinydb and exposes
        convenience methods

    """

    def __init__(self, game, table, id):
        self.game = game
        self.table = table
        self.id = id
        self.load_values()

        """
        fields:
            i_name
            d_name
            Class
            descriptions
            flags
            location = {"table": tablename, "id": id}
        """

    @staticmethod
    def get_object(game, table, id, item):
        return BaseObject(game, table, id)

    def save_values(self):

        """ save all non function attributes of this object
            to the database """

        for name, value in self.__dict__.items():
            if name != "table" and name != "id" and name != "game":
                self.save_value(name)

    def save_value(self, name):

        """ save a given attribute to the database """

        value = getattr(self, name)
        self.table.update({name: value}, eids=[self.id])

    def load_values(self):

        """ load all values from the database and attach as attributes """

        values = self.table.get(eid=self.id)
        for name, value in values.items():
            setattr(self, name, value)

    # convenience methods for checking things, all return booleans

    def is_describable(self, actor):
        return hasattr(self, "descriptions")

    def is_attackable(self, actor):
        return all(hasattr(self, "stats"), "hp" in self.stats,
                   "def" in self.stats)

    def has_exits(self, actor):
        return hasattr(self, "exits")

    def is_usable(self, actor):
        """ whether or not this can be passed to 'use_action'
            on an actor
        """
        return hasattr(self, "do_action")

        # other helper methods
    def describe(self, actorflags):
        if self.is_describable():
            desc_out = []
            for description in self.descriptions:
                if misc_lib.check_conditions(self.get_flags(),
                                             description["conditions"]):
                    desc_out.append(description["description"])
            return desc_out
        else:
            return None

    def get_flags(self):
        if hasattr(self, "location"):
            loc_obj = getattr(self.game,
                              self.location["table"])[self.location["id"]]
            loc_flags = loc_obj.get_flags()
            return self.flags + loc_flags
        else:
            return self.flags
