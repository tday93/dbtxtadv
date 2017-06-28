""" transforms are functions that alter a game object in some manner """


def damage(game_obj, dmg):
    if game_obj.is_damageable():
        game_obj.stats["hp"] = game_obj.stats["hp"] - dmg
        game_obj.save_values()


def move(game_obj, loc_dict):
    game_obj.location = loc_dict
    game_obj.save_values()


