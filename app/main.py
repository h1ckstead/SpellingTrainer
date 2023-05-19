import getpass
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from core.spelling_trainer import SpellingTrainerApp

if __name__ == '__main__':
    log_file = "SpellingTrainer.log"

    if os.name == 'posix':  # macOS or Linux
        username = getpass.getuser()
        log_dir = os.path.join(f'/Users/{username}/Library/Logs/')
        log_path = os.path.join(log_dir, log_file)
    elif os.name == 'nt':  # Windows
        log_dir = os.path.join(os.getenv('APPDATA'), 'SpellingTrainer')
        log_path = os.path.join(log_dir, log_file)
    else:
        log_path = log_file

    # Create the log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Create the log file if it doesn't exist
    if not os.path.exists(log_path):
        open(log_path, 'w').close()

    if getattr(sys, 'frozen', False):
        # If running in a bundled executable
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(sys.executable)
    else:
        # If running as a regular Python script
        base_path = os.path.dirname(os.path.abspath(__file__))

    # create a rotating file handler with a max size of 10 MB
    handler = RotatingFileHandler(filename=log_path, maxBytes=10 * 1024 * 1024, backupCount=5)

    # configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: [%(levelname)s] %(message)s',
                        handlers=[handler, logging.StreamHandler()])

    # create an instance of the SpellingTrainerApp class
    logging.info('Starting application')
    logging.debug('Creating SpellingTrainerApp instance')
    spelling_trainer = SpellingTrainerApp()

    # start the tkinter event loop
    logging.debug('Starting tkinter event loop')
    spelling_trainer.mainloop()
