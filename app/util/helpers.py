import os
import sys
import pickle
from core import config
import logging


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
