import logging
import os
import pickle
import platform
import sys
import urllib
import webbrowser
import requests
from bs4 import BeautifulSoup
from tkinter import messagebox


from core import config
from core import constants
from core.constants import HIGH_PRIORITY_WORDS, LOW_PRIORITY_WORDS


def load_save():
    savefile_path = get_savefile_path()
    try:
        with open(savefile_path, 'rb') as file:
            data = pickle.load(file)
            logging.debug(f"Loaded savefile: {data}")
        return data
    except FileNotFoundError:
        logging.error(f"Save file not found in: {savefile_path}")
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
        if hasattr(sys, '_MEIPASS'):  # Running as a bundled executable
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(sys.executable)
    elif 'unittest' in sys.modules:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app'))
    else:  # Running as a regular Python script
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, *args)


def get_avatars_list():
    return os.listdir(get_path("assets/avatars"))


def report_bug():
    email_address = "spellingtrainer@proton.me"
    subject = "[Bug Report] for Spelling Trainer"
    current_platform = platform.system()
    newline = '\n'  # Default newline character
    if current_platform == 'Windows':
        newline = '\r\n'  # Use Windows newline character sequence

    body = f"Hello,{newline}{newline}" \
           f"I wanted to provide feedback for the Spelling Trainer {config.VERSION}.{newline}{newline}" \
           f"[Your feedback here, include any relevant information, steps to reproduce, screenshots]"

    if current_platform == 'Windows':
        encoded_body = urllib.parse.quote(body)
        mailto_url = f"mailto:{email_address}?subject={subject}&body={encoded_body}"
    else:
        mailto_url = f"mailto:{email_address}?subject={subject}&body={body}"
    webbrowser.open(mailto_url)


def load_dictionary(name):
    """
    Loads appropriate binary file containing dict of words.

    :param name: str filename
    :return: dict
    """
    with open(get_path(f'assets/{name}'), mode='rb') as document:
        return pickle.load(document)


def verify_dicts_version(users, last_user):
    """
    Checks if dictionaries of existing users are outdated.

    :param users: dict containing usernames and their respective User objects
    :param last_user User object
    :return:
    """
    updated = False
    if last_user.dictionaries.high_priority_words["version"] < config.HIGH_PRIORITY_DICT_VERSION:
        logging.info(f"{HIGH_PRIORITY_WORDS} is stale. Updating from "
                     f"{last_user.dictionaries.high_priority_words['version']} to "
                     f"{config.HIGH_PRIORITY_DICT_VERSION}.")
        update_user_dict(users, to_update=HIGH_PRIORITY_WORDS)
        updated = True
    if last_user.dictionaries.low_priority_words["version"] < config.LOW_PRIORITY_DICT_VERSION:
        logging.info(f"{LOW_PRIORITY_WORDS} is stale. Updating from "
                     f"{last_user.dictionaries.low_priority_words['version']} to "
                     f"{config.LOW_PRIORITY_DICT_VERSION}.")
        update_user_dict(users, to_update=LOW_PRIORITY_WORDS)
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
        if not user.dictionaries.vocabulary and not user.dictionaries.learned_words:
            if to_update == HIGH_PRIORITY_WORDS:
                user.dictionaries.high_priority_words = load_dictionary(constants.HIGH_PRIORITY_WORDS)
            elif to_update == LOW_PRIORITY_WORDS:
                user.dictionaries.low_priority_words = load_dictionary(constants.LOW_PRIORITY_WORDS)
        elif not user.dictionaries.vocabulary:
            existing_data = [user.dictionaries.learned_words]
        elif not user.dictionaries.learned_words:
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
            logging.debug(f"Removed 'AmE' value for word {key}")
        if key in model and constants.AmE in value:
            model[key][constants.AmE] = value[constants.AmE]
            logging.debug(f"Added/Updated 'AmE' value for word {key}")
        if key in model and value[constants.DEFINITIONS] == model[key]:
            keys_to_remove.append(key)
        elif key in model:
            model[key][constants.DEFINITIONS] = value[constants.DEFINITIONS]
            keys_to_remove.append(key)
            logging.debug(f"Updated value of word {key}")
    for key in keys_to_remove:
        del to_remove_from[key]
        logging.debug(f"Removed {key} from dict")
    return to_remove_from


def check_for_updates():
    page_url = 'https://spellingtrainer.wixsite.com/download'

    response = requests.get(page_url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    footer = soup.find("footer", {"class": "SITE_FOOTER_WRAPPER"})
    version_element = footer.find('p', text=lambda text: text and 'Version: ' in text).string
    version = version_element.replace('Version: ', '')

    if version != config.VERSION:
        message = 'New version is available: {}\n\nDo you want to go to the website and download the update?'.format(
            version)
        result = messagebox.askquestion('Update Available', message, icon='question')
        if result == 'yes':
            webbrowser.open(page_url)
    else:
        messagebox.showinfo('Up to Date', 'Already up to date', icon='info')
