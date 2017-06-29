# from tinydb import TinyDB, Query
from objects.baseobject import BaseObject
from objects.actors import Actor
from objects.rooms import Room
from objects.items import Item
from actions import Action
from data.gamedb import GameDB
import misc_lib
import cmdparser


class Game(object):

    def __init__(self, dbpath, logger):
        # initialize database
        self.logger = logger
        self.gdb = GameDB(dbpath)
        # initialize objects
        self.rooms = self.load_rooms(self.gdb.rooms, "rooms")
        self.actors = self.load_actors(self.gdb.actors, "actors")
        self.items = self.load_items(self.gdb.items, "items")
        # load actions
        self.actions = self.load_actions(self.gdb.actions, "actions")
        # initialize player
        # start game loop
        self.ui = None

    async def test_loop(self):
        while True:
            player_input = input("What do?")
            await self.player_input(player_input)

    async def player_input(self, player_input):
        """ called when a player inputs text into game """
        player_action, split_string = cmdparser.cmdparse(player_input,
                                                         self.pc)
        scope = misc_lib.get_in_scope(self.pc)
        player_action.do_action(self.pc, split_string=split_string,
                                raw_text=player_input, scope=scope)

    def player_output(self, player_output_list):
        """ outputs text to the player """
        for item in player_output_list:
            print(item)

    def register_player(self, player_obj):
        self.pc = player_obj

    def load_objects(self, table, obj_class, table_name):
        built_objects = {}
        for item in table.all():
            new_object = obj_class.get_object(self, table, item.eid,
                                              item, table_name)
            self.logger.debug(
                "obj = {} type ={}".format(
                    new_object.i_name, new_object.__class__.__name__))
            built_objects[item.eid] = new_object
        return built_objects

    def load_simple(self, table, table_name):
        return self.load_objects(table, BaseObject, table_name)

    def load_rooms(self, table, table_name):
        return self.load_objects(table, Room, table_name)

    def load_actors(self, table, table_name):
        return self.load_objects(table, Actor, table_name)

    def load_items(self, table, table_name):
        return self.load_objects(table, Item, table_name)

    def load_actions(self, table, table_name):
        built_actions = {}
        for item in table.all():
            new_object = Action.get_action(self, table,
                                           item.eid, item, table_name)
            built_actions[item.eid] = new_object
        return built_actions

    def get_game_object(self, id_dict):
        return getattr(self, id_dict["table"])[id_dict["id"]]


if __name__ == "__main__":
    g = Game("data/db.json")
