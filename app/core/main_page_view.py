import random
from tkinter import *

from PIL import Image
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkImage, CTkProgressBar

from app import config
from app.core.choose_different_user_view import ChooseDifferentUserPage
from app.core.new_user_view import NewUserPage
from app.core.practice_page_view import PracticePage
from app.core.user_page_view import UserPage


class MainPage(CTkFrame):
    def __init__(self, parent, controller, saved_data):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.saved_data = saved_data
        self.last_user = saved_data['last_user']
        self.grid(row=0, column=0, sticky="nsew")

        self.greeting().grid(row=0, column=1, pady=10)
        self.description().grid(row=1, column=0, pady=20, columnspan=3)
        self.continue_btn().grid(row=2, column=0, padx=5)
        self.see_stats_btn().grid(row=2, column=1, padx=5, sticky='w')
        self.horizontal_line().grid(row=3, column=0, columnspan=3, pady=20, padx=10)
        self.choose_diff_usr_btn().grid(row=4, column=0)
        self.new_user_btn().grid(row=4, column=1, sticky='w')
        self.grid_rowconfigure(5, weight=1)
        self.exit_btn().grid(row=6, column=2, sticky='e', padx=10, pady=(0, 10))

    def greeting(self):
        text = config.GREETING_MAIN.format(self.last_user, random.choice(config.GREETING_EMOJI))
        return CTkLabel(self, text=text, font=self.controller.title_font)

    def description(self):
        return CTkLabel(self, text=config.DESCRIPTION_MAIN, font=self.controller.font,
                        wraplength=config.WINDOW_WIDTH - 20)

    def continue_btn(self):
        #  TODO: Fix avatars path
        avatar_image = CTkImage(Image.open(f'assets/avatars/{self.saved_data[self.last_user].avatar}'))
        return CTkButton(self, text='Continue', image=avatar_image, compound='left', width=160, height=35,
                         command=lambda: PracticePage(parent=self.parent, controller=self.controller,
                                                      current_user=self.saved_data[self.last_user]).tkraise())

    def see_stats_btn(self):
        return CTkButton(self, text='See complete stats', width=160, height=35,
                         command=lambda: UserPage(parent=self.parent, controller=self.controller,
                                                  current_user=self.saved_data[self.last_user],
                                                  session_attempts_correct=0, session_attempts_incorrect=0).tkraise())

    def horizontal_line(self):
        progressbar = CTkProgressBar(self, width=config.WINDOW_WIDTH - 20)
        progressbar.set(1)
        return progressbar

    def choose_diff_usr_btn(self):
        return CTkButton(self, text='Choose a different User', width=160, height=35,
                         command=lambda: ChooseDifferentUserPage(parent=self.parent,
                                                                 controller=self.controller,
                                                                 saved_data=self.saved_data).tkraise())

    def new_user_btn(self):
        return CTkButton(self, text='New User', width=160, height=35,
                         command=lambda: NewUserPage(parent=self.parent,
                                                     controller=self.controller,
                                                     saved_data=self.saved_data).tkraise())

    def exit_btn(self):
        return CTkButton(self, text='Exit', width=160, height=35, command=self.controller.destroy)
