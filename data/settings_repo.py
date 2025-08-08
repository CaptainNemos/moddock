from data import config_repo

def get(key, default=None):
    return config_repo.get_setting(key, default)

def set(key, value):
    return config_repo.set_setting(key, value)
