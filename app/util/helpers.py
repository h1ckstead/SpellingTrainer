import os
import sys
import pickle
from core import config
import logging
from core import constants


def load_save():
    savefile_path = get_savefile_path()
    logging.info(savefile_path)
    try:
        with open(savefile_path, 'rb') as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        return None


def get_savefile_path():
    if os.name == 'posix':  # macOS or Linux
        app_support_dir = os.path.expanduser(os.path.join('~', 'Library', 'Application Support', config.APP_NAME))
        os.makedirs(app_support_dir, exist_ok=True)
        savefile_path = os.path.join(app_support_dir, 'savefile')
    elif os.name == 'nt':  # Windows
        appdata_dir = os.path.expanduser(os.path.join('~', 'AppData', 'Roaming', config.APP_NAME))
        os.makedirs(appdata_dir, exist_ok=True)
        savefile_path = os.path.join(appdata_dir, 'savefile')
    else:
        savefile_path = 'savefile'
    return savefile_path


def get_path(*args):
    if getattr(sys, 'frozen', False):
        # Running as a bundled executable
        if hasattr(sys, '_MEIPASS'):
            # macOS and Windows
            base_path = sys._MEIPASS
        else:
            # macOS
            base_path = os.path.dirname(sys.executable)
    elif 'unittest' in sys.modules:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app'))
    else:
        # Running as a regular Python script
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    return os.path.join(base_path, *args)


def get_avatars_list():
    return os.listdir(get_path("assets/avatars"))


def load_dictionary(name):
    """
    Loads appropriate binary file containing dict of words.

    :param name: str filename
    :return: dict
    """
    with open(get_path(f'assets/{name}'), mode='rb') as document:
        return pickle.load(document)


def verify_dicts_version(saved_data):
    """
    Checks if dictionaries of existing users are outdated.

    :param saved_data: dict
    :return:
    """
    if saved_data[saved_data["last_user"]].dictionaries.high_priority_words["version"] < config.DICT_VERSION:
        users = saved_data.pop("last_user")
        update_user_dicts(users)
    else:
        logging.info("Users' dictionaries are up to date")


def update_user_dicts(users):
    """
    Updates dictionaries for all existing users.

    :param users: dict
    :return:
    """
    new_high_priority_words = load_dictionary(constants.HIGH_PRIORITY_WORDS)
    new_low_priority_words = load_dictionary(constants.LOW_PRIORITY_WORDS)
    for user in users:
        vocabulary = users[user].vocabulary
        learned_words = users[user].learned_words

        updated_high_priority_words = remove_duplicates(to_remove_from=new_high_priority_words, model=vocabulary)
        final_high_priority_words = remove_duplicates(to_remove_from=updated_high_priority_words, model=learned_words)
        
        updated_low_priority_words = remove_duplicates(to_remove_from=new_low_priority_words, model=vocabulary)
        final_low_priority_words = remove_duplicates(to_remove_from=updated_low_priority_words, model=learned_words)

        users[user].dictionaries.high_priority_words = final_high_priority_words
        users[user].dictionaries.low_priority_words = final_low_priority_words


def remove_duplicates(to_remove_from, model):
    """
    Compares two dicts and removes common values from one of them.

    :param to_remove_from: dict
    :param model: dict
    :return: dict
    """
    new_dict = {}
    for key, value in to_remove_from.items():
        if key not in model:
            new_dict[key] = value
        else:
            print(f"Removed {key} from dict")
    to_remove_from = new_dict
    return to_remove_from
