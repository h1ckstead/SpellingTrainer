import logging
import platform
import tkinter as tk
import webbrowser
from tkinter import messagebox

import customtkinter
from customtkinter import CTk, CTkFont, CTkFrame

from core import config
from core.gui.views.main_view import MainPage
from core.gui.views.welcome_view import WelcomePage
from util import helpers


class SpellingTrainerApp(CTk):
    def __init__(self, *args, **kwargs):
        CTk.__init__(self, *args, **kwargs)
        logging.debug("Initializing top level window")
        if platform.system() == 'Windows':
            self.iconbitmap(helpers.get_path("assets", "favicon.ico"))
        self.title(config.APP_NAME)
        self.title_font = CTkFont(family="Arial", size=config.TITLE_FONT_SIZE, weight="bold")
        self.font = CTkFont(family="Arial", size=config.FONT_SIZE)
        self.geometry(f'{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+{self.center_x()}+{self.center_y()}')
        customtkinter.set_appearance_mode("dark")

        self.create_menu()

        logging.debug("Creating mainframe")
        mainframe = CTkFrame(self)
        mainframe.pack(side="top", fill="both", expand=True)
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)

        saved_data = helpers.load_save()
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

    def create_menu(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Check for updates...")  # TODO: Add check for updates function
        file_menu.add_command(label="Report a bug", command=lambda: webbrowser.open("mailto:spellingtrainer@proton.me"))
        file_menu.add_command(label="Donate", command=self.open_donate_page)
        file_menu.add_command(label="About", command=self.show_info)
        menu_bar.add_cascade(label="Help", menu=file_menu)

        # Configure the root window to use the menu bar
        self.configure(menu=menu_bar)

    @staticmethod
    def show_info():
        messagebox.showinfo(message="Copyright (C) 2023 Victoria Lazareva.\n\n"
                                    f"Version: {config.VERSION}\n\n"
                                    "Spelling Trainer is free software\n\n"
                                    "Credits:\n"
                                    "Logo by Vecteezy\n"
                                    "Avatars by Freepik\n"
                                    "Icons by Uxwing\n"
                            )

    @staticmethod
    def open_donate_page():
        webbrowser.open('https://example.com/donate')
