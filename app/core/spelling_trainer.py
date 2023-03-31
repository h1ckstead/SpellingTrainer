from tkinter import *
from tkinter import font

from app import config
from app.core import user
from app.core.new_user_view import NewUserPage
from app.core.main_page_view import MainPage


class SpellingTrainerApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title(config.APP_NAME)
        self.title_font = font.Font(family=config.MAC_FONT, size=config.TITLE_FONT_SIZE, weight="bold")
        self.font = font.Font(family=config.MAC_FONT, size=config.FONT_SIZE)
        self.geometry(f'{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+{self.center_x()}+{self.center_y()}')

        mainframe = Frame(self)
        mainframe.pack(side="top", fill="both", expand=True)
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)

        saved_data = user.User.load_save()
        if saved_data is None:
            NewUserPage(parent=mainframe, controller=self).tkraise()
        else:
            MainPage(parent=mainframe, controller=self, saved_data=saved_data).tkraise()

    def center_x(self):
        user_screen_width = self.winfo_screenwidth()
        return int(user_screen_width / 2 - config.WINDOW_WIDTH / 2)

    def center_y(self):
        user_screen_height = self.winfo_screenheight()
        return int(user_screen_height / 2 - config.WINDOW_HEIGHT / 2)
