# from tinydb import TinyDB, Query
from objects.baseobject import BaseObject
from objects.actors import Actor
from actions import Action
from data.gamedb import GameDB
import cmdparser


class Game(object):

    def __init__(self, dbpath):
        # initialize database
        self.gdb = GameDB(dbpath)
        # initialize objects
        self.rooms = self.load_simple(self.gdb.rooms)
        self.actors = self.load_actors(self.gdb.actors)
        self.items = self.load_simple(self.gdb.items)
        # load actions
        self.actions = self.load_actions(self.gdb.actions)
        # initialize player
        # start game loop
        self.ui = None

    def player_input(self, player_input):
        """ called when a player inputs text into game """
        player_action, split_string = cmdparser.cmdparse(player_input, self.pc)
        player_action.do_action(self.pc, split_string=split_string)

    def player_output(self, player_output):
        """ outputs text to the player """
        print(player_output)

    def register_player(self, player_obj):
        self.pc = player_obj

    def load_objects(self, table, obj_class):
        built_objects = {}
        for item in table.all():
            new_object = obj_class.get_object(self, table, item.eid, item)
            built_objects[item.eid] = new_object
        return built_objects

    def load_simple(self, table):
        return self.load_objects(table, BaseObject)

    def load_actors(self, table):
        return self.load_objects(table, Actor)

    def load_actions(self, table):
        built_actions = {}
        for item in table.all():
            new_object = Action.get_action(self, table, item.eid, item)
            built_actions[item.eid] = new_object
        return built_actions


def main(options):
    g = Game("data/db.json")
    return g


if __name__ == "__main__":
    g = Game("data/db.json")
    print(type(g.actors[1]))
