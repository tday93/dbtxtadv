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
        self.player_characters = {}
        # initialize objects
        self.rooms = self.load_rooms(self.gdb.rooms, "rooms")
        self.actors = self.load_actors(self.gdb.actors, "actors")
        self.items = self.load_items(self.gdb.items, "items")
        # load actions
        self.actions = self.load_actions(self.gdb.actions, "actions")
        # start game loop
        self.ui = None
        self.message_queue = []

    async def test_loop(self):
        while True:
            player_input = input("What do?")
            input_pkg = {"player_id": 1, "player_input": player_input}
            await self.player_input(input_pkg)

    def player_input(self, input_pkg):
        """ called when a player inputs text into game """
        player = self.player_characters[input_pkg["player_id"]]
        player_input = input_pkg["player_input"]
        player_action, split_string = cmdparser.cmdparse(player_input,
                                                         player)
        scope = misc_lib.get_in_scope(player)
        player_action.do_action(player, split_string=split_string,
                                raw_text=player_input, scope=scope)
        self.player_ouput("TEST MESSAGE PLEASE IGNORE")
        reply = self.message_queue
        self.message_queue = []
        return reply

    def player_ouput(self, output_text):
        # adds a message to the queue to be sent to the player
        self.message_queue.append(output_text)

    def register_player(self, player_obj):
        self.player_characters[player_obj.id] = player_obj

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
