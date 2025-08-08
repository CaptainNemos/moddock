from data import config_repo

def load():
    return config_repo.get_mods()

def save(mods):
    return config_repo.set_mods(mods)
