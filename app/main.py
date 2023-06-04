import getpass
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
import platform

from core.spelling_trainer import SpellingTrainerApp
#
# if __name__ == '__main__':
#     log_file = "SpellingTrainer.log"
#     log_dir = ""
#
#     if os.name == 'posix':  # macOS or Linux
#         username = getpass.getuser()
#         log_dir = os.path.join(f'/Users/{username}/Library/Logs/')
#         log_path = os.path.join(log_dir, log_file)
#     elif os.name == 'nt':  # Windows
#         log_dir = os.path.join(os.getenv('APPDATA'), 'SpellingTrainer')
#         log_path = os.path.join(log_dir, log_file)
#     else:
#         log_path = log_file
#
#     # Create the log directory if it doesn't exist
#     os.makedirs(log_dir, exist_ok=True)
#
#     # Create the log file if it doesn't exist
#     if not os.path.exists(log_path):
#         open(log_path, 'w').close()
#
#     if getattr(sys, 'frozen', False):
#         # If running in a bundled executable
#         if hasattr(sys, '_MEIPASS'):
#             base_path = sys._MEIPASS
#         else:
#             base_path = os.path.dirname(sys.executable)
#     else:
#         # If running as a regular Python script
#         base_path = os.path.dirname(os.path.abspath(__file__))
#
#     # create a rotating file handler with a max size of 10 MB
#     handler = RotatingFileHandler(filename=log_path, maxBytes=10 * 1024 * 1024, backupCount=5)
#
#     # configure logging
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s: [%(levelname)s] %(message)s',
#                         handlers=[handler, logging.StreamHandler()])
#
#     logging.info('Starting application')
#     spelling_trainer = SpellingTrainerApp()
#
#     logging.debug('Starting tkinter event loop')
#     spelling_trainer.mainloop()

# ------------------
# import fcntl


def configure_paths_and_loggers():
    log_file = "SpellingTrainer.log"
    log_dir = ""

    if os.name == 'posix':  # macOS or Linux
        username = getpass.getuser()
        log_dir = os.path.join(f'/Users/{username}/Library/Logs/')
        log_path = os.path.join(log_dir, log_file)
        lock_file_path = os.path.join('/tmp', 'spelling_trainer.lock')
    elif os.name == 'nt':  # Windows
        log_dir = os.path.join(os.getenv('APPDATA'), 'Spelling Trainer')
        log_path = os.path.join(log_dir, log_file)
        lock_file_path = os.path.join(log_dir, 'spelling_trainer.lock')
    else:
        log_path = log_file
        lock_file_path = os.path.join(os.getcwd(), 'spelling_trainer.lock')

    # Create the log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Create the log file if it doesn't exist
    if not os.path.exists(log_path):
        open(log_path, 'w').close()

    # if getattr(sys, 'frozen', False):
    #     # If running in a bundled executable
    #     if hasattr(sys, '_MEIPASS'):
    #         base_path = sys._MEIPASS
    #     else:
    #         base_path = os.path.dirname(sys.executable)
    # else:
    #     # If running as a regular Python script
    #     base_path = os.path.dirname(os.path.abspath(__file__))

    handler = RotatingFileHandler(filename=log_path, maxBytes=10 * 1024 * 1024, backupCount=5)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: [%(levelname)s] %(message)s',
                        handlers=[handler, logging.StreamHandler()])
    # Get the logger for PIL or Pillow
    pil_logger = logging.getLogger('PIL')
    pil_logger.setLevel(logging.WARNING)
    return lock_file_path


def start_mainloop():
    logging.info('Starting application')
    spelling_trainer = SpellingTrainerApp()
    spelling_trainer.mainloop()


def run_program():
    # lock_file_path = configure_paths_and_loggers()
    # lock_file = open(lock_file_path, 'w')
    #
    # try:
    #     fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    #     start_mainloop()
    # except (OSError, IOError):
    #     logging.error("Another instance of the program is already running.")
    #     sys.exit(1)
    # finally:
    #     fcntl.lockf(lock_file, fcntl.LOCK_UN)
    #     lock_file.close()
    #     os.remove(lock_file_path)
    current_platform = platform.system()
    lock_file_path = configure_paths_and_loggers()
    if current_platform == 'Windows':
        import msvcrt
        lock_file = open(lock_file_path, 'w')
        try:
            # lock_file = open(lock_file_path, 'w')
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
            start_mainloop()
        except IOError:
            logging.error("Another instance of the program is already running.")
            sys.exit(1)
        finally:
            lock_file.close()
            os.remove(lock_file_path)

    elif current_platform == 'Darwin':
        import fcntl
        lock_file = open(lock_file_path, 'w')
        try:
            fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            start_mainloop()
        except (OSError, IOError):
            logging.error("Another instance of the program is already running.")
            sys.exit(1)
        finally:
            fcntl.lockf(lock_file, fcntl.LOCK_UN)
            lock_file.close()
            os.remove(lock_file_path)
    else:
        logging.error(f"Unsupported operating system: {current_platform}")
        sys.exit(1)


if __name__ == '__main__':
    run_program()
