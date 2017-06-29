import misc_lib


class BaseObject(object):

    """

        base class for all ingame objects

        handles connection to tinydb and exposes
        convenience methods

    """

    def __init__(self, game, table, id, table_name):
        self.game = game
        self.table_name = table_name
        self.table = table
        self.id = id
        self.load_values()

        """
        fields:
            MANDATORY:
            i_name
            d_name
            Class

            OPTIONAL:
            descriptions = list of dicts of form:
                {"conditions":[], "description":""}
            flags = list of strings
            location = {"table": tablename, "id": id}
            inventory = list of item table refs
            actions = list of action i_names
        """

    @staticmethod
    def get_object(game, table, id, item, table_name):
        return BaseObject(game, table, id, table_name)

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

    def is_damageable(self, actor=None):
        return (hasattr(self, "stats") and "hp" in self.stats)

    def has_location(self):
        return hasattr(self, "location")

    def has_exits(self, actor=None):
        return hasattr(self, "exits")

    def has_inventory(self):
        return hasattr(self, "inventory")

    def has_actions(self):
        return hasattr(self, "actions")

    def is_usable(self, actor):
        """ whether or not this can be passed to 'use_action'
            on an actor
        """
        return hasattr(self, "do_action")

        # other helper methods
    def describe(self, actor):
        if self.is_describable(actor):
            desc_txt = []
            for description in self.descriptions:
                if misc_lib.check_conditions(actor.get_flags(),
                                             description["conditions"]):
                    desc_txt.append(description["description"])
            return self.format_description(desc_txt)
        else:
            return None

    def format_description(self, desc_txt):
        """ gets a list of description text,
            returns this text in a readable format

            base format is as follows:
                [category] <name> :
                    lines of
                    descriptions
        """
        if hasattr(self, "category"):
            category = self.category
        else:
            category = self.table_name
        desc_block = "[{}] <{}>: \n".format(category, self.d_name)
        for line in desc_txt:
            desc_block = desc_block + "  {}\n".format(line)
        return desc_block

    def get_identifiers(self):
        ids = [self.i_name, self.d_name]
        if hasattr(self, "aliases"):
            ids = ids + self.aliases
        return ids

    def get_loc_obj(self):
        if not hasattr(self, "location"):
            return None
        loc_obj = getattr(self.game,
                          self.location["table"])[self.location["id"]]
        return loc_obj

    def get_flags(self):
        all_flags = []
        loc_obj = self.get_loc_obj()
        if hasattr(self, "flags"):
            all_flags = self.flags
        if loc_obj:
            all_flags = all_flags + loc_obj.get_flags()
        return all_flags

    def get_exits(self):
        if self.has_exits():
            return self.exits

    def get_reference_dict(self):
        return {"table": self.table_name, "id": self.id}

    def get_items(self):
        items = []
        for item in self.inventory:
            items.append(self.game.get_game_object(item))
        return items

    def get_actions(self):
        actions = self.actions
        if self.has_inventory():
            i_with_actions = [item for item in self.get_items()
                              if item.has_actions()]
            for item in i_with_actions:
                actions = actions + item.get_actions()
        return actions
