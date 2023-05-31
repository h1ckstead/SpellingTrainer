import os
import sys
import pickle
from core import config
import logging
from core import constants
from core.constants import HIGH_PRIORITY_WORDS, LOW_PRIORITY_WORDS


def load_save():
    savefile_path = get_savefile_path()
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
    updated = False
    last_user = saved_data["last_user"]
    if saved_data[last_user].dictionaries.high_priority_words["version"] < config.HIGH_PRIORITY_DICT_VERSION:
        logging.info(f"{HIGH_PRIORITY_WORDS} is stale. Updating from "
                     f"{saved_data[last_user].dictionaries.high_priority_words['version']} to "
                     f"{config.HIGH_PRIORITY_DICT_VERSION}.")
        saved_data.pop("last_user")
        users = saved_data
        update_user_dict(users, to_update=HIGH_PRIORITY_WORDS)
        users["last_user"] = last_user
        updated = True
    if saved_data[last_user].dictionaries.low_priority_words["version"] < config.LOW_PRIORITY_DICT_VERSION:
        logging.info(f"{LOW_PRIORITY_WORDS} is stale. Updating from "
                     f"{saved_data[last_user].dictionaries.low_priority_words['version']} to "
                     f"{config.LOW_PRIORITY_DICT_VERSION}.")
        saved_data.pop("last_user")
        users = saved_data
        update_user_dict(users, to_update=LOW_PRIORITY_WORDS)
        users["last_user"] = last_user
        updated = True
    else:
        logging.info("Users' dictionaries are up to date")
    return updated


def update_user_dict(users, to_update):
    """
    Updates dictionaries for all existing users.

    :param users: dict
    :param to_update str name of the dictionary
    :return:
    """
    for user in users.values():
        existing_data = []
        if len(user.dictionaries.vocabulary) == 0 and len(user.dictionaries.learned_words) == 0:
            if to_update == HIGH_PRIORITY_WORDS:
                user.dictionaries.high_priority_words = load_dictionary(constants.HIGH_PRIORITY_WORDS)
                return
            elif to_update == LOW_PRIORITY_WORDS:
                user.dictionaries.low_priority_words = load_dictionary(constants.LOW_PRIORITY_WORDS)
                return
        elif len(user.dictionaries.vocabulary) == 0:
            existing_data = [user.dictionaries.learned_words]
        elif len(user.dictionaries.learned_words) == 0:
            existing_data = [user.dictionaries.vocabulary]
        else:
            existing_data = [user.dictionaries.vocabulary, user.dictionaries.learned_words]

        if to_update == HIGH_PRIORITY_WORDS:
            new_high_priority_words = load_dictionary(constants.HIGH_PRIORITY_WORDS)["data"]
            for data in existing_data:
                updated_high_priority_words = remove_duplicates(to_remove_from=new_high_priority_words, model=data)
                user.dictionaries.high_priority_words["data"] = updated_high_priority_words
                user.dictionaries.high_priority_words["version"] = config.HIGH_PRIORITY_DICT_VERSION
        elif to_update == LOW_PRIORITY_WORDS:
            new_low_priority_words = load_dictionary(constants.LOW_PRIORITY_WORDS)["data"]
            for data in existing_data:
                updated_low_priority_words = remove_duplicates(to_remove_from=new_low_priority_words, model=data)
                user.dictionaries.low_priority_words["data"] = updated_low_priority_words
                user.dictionaries.low_priority_words["version"] = config.LOW_PRIORITY_DICT_VERSION
        user.save_progress()


def remove_duplicates(to_remove_from, model):
    """
    Compares two dicts and removes common values from one of them
    Updates changed values.

    :param to_remove_from: dict
    :param model: dict
    :return: dict
    """
    keys_to_remove = []
    for key, value in to_remove_from.items():
        if key in model and constants.AmE in model[key] and constants.AmE not in value:
            del model[key][constants.AmE]
            logging.info(f"Removed 'AmE' value for word {key}")
        if key in model and constants.AmE in value:
            model[key][constants.AmE] = value[constants.AmE]
            logging.info(f"Added/Updated 'AmE' value for word {key}")
        if key in model and value[constants.DEFINITIONS] == model[key]:
            keys_to_remove.append(key)
        elif key in model:
            model[key][constants.DEFINITIONS] = value[constants.DEFINITIONS]
            keys_to_remove.append(key)
            logging.info(f"Updated value of word {key}")
    for key in keys_to_remove:
        del to_remove_from[key]
        logging.info(f"Removed {key} from dict")
    return to_remove_from
