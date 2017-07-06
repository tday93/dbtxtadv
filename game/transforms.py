""" transforms are functions that alter a game object in some manner """


def damage(game_obj, dmg):
    if game_obj.is_damageable():
        game_obj.stats["hp"] = game_obj.stats["hp"] - dmg
        game_obj.save_values()


def move(game_obj, loc_obj):
    # 1. get current obj loc
    # 2. remove obj from current loc
    # 3. add obj to new loc
    # 4. set obj loc to new loc
    obj_ref_dict = game_obj.get_ref_dict()
    old_loc = game_obj.get_loc_obj()
    old_loc.children.remove(obj_ref_dict)
    loc_obj.children.append(obj_ref_dict)
    game_obj.location = loc_obj.get_ref_dict()

    # write everything to table
    old_loc.save_values()
    loc_obj.save_values()
    game_obj.save_values()
