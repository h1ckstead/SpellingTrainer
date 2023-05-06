import logging
from logging.handlers import RotatingFileHandler

from app.core.spelling_trainer import SpellingTrainerApp

if __name__ == '__main__':
    # create a rotating file handler with a max size of 10 MB
    handler = RotatingFileHandler(filename='SpellingTrainer.log', maxBytes=10 * 1024 * 1024, backupCount=5)

    # configure logging
    logging.basicConfig(filename='SpellingTrainer.log', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s', handlers=[handler])

    # create an instance of the SpellingTrainerApp class
    logging.info('Starting application')
    logging.debug('Creating SpellingTrainerApp instance')
    app = SpellingTrainerApp()

    # start the tkinter event loop
    logging.debug('Starting tkinter event loop')
    app.mainloop()
