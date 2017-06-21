

def check_conditions(actorset, testset):
    return all(item in actorset for item in testset)
