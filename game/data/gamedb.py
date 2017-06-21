from tinydb import TinyDB


class GameDB(object):

    def __init__(self, dbpath):
        self.db = TinyDB(dbpath, indent=4, sort_keys=True,
                         separators=(',', ':'))
        self.rooms = self.db.table("rooms")
        self.actors = self.db.table("actors")
        self.items = self.db.table("items")
        self.actions = self.db.table("actions")
