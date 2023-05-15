import logging

import customtkinter
from customtkinter import CTk, CTkFont, CTkFrame

import util.load_savefile as load_savefile
from core import config
from core.gui.views.main_view import MainPage
from core.gui.views.welcome_view import WelcomePage


class SpellingTrainerApp(CTk):
    def __init__(self, *args, **kwargs):
        CTk.__init__(self, *args, **kwargs)
        # self.iconbitmap("path_to_your_icon.ico") <-- Icon
        logging.debug("Initializing top level window")
        self.title(config.APP_NAME)
        self.title_font = CTkFont(family="Arial", size=config.TITLE_FONT_SIZE, weight="bold")
        self.font = CTkFont(family="Arial", size=config.FONT_SIZE)
        self.geometry(f'{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+{self.center_x()}+{self.center_y()}')
        self.resizable(False, False)
        customtkinter.set_appearance_mode("dark")

        logging.debug("Creating mainframe")
        mainframe = CTkFrame(self)
        mainframe.pack(side="top", fill="both", expand=True)
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)

        saved_data = load_savefile.load_save()
        logging.debug(f"Loaded savefile: {saved_data}")
        if saved_data is None:
            WelcomePage(parent=mainframe, controller=self).tkraise()
        else:
            MainPage(parent=mainframe, controller=self, saved_data=saved_data).tkraise()

    def center_x(self):
        user_screen_width = self.winfo_screenwidth()
        return int(user_screen_width / 2 - config.WINDOW_WIDTH / 2)

    def center_y(self):
        user_screen_height = self.winfo_screenheight()
        return int(user_screen_height / 2 - config.WINDOW_HEIGHT / 2)
