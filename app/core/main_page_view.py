from app.core.user_page_view import UserPage
from app.core.practice_page_view import PracticePage
from app.core.choose_different_user_view import ChooseDifferentUserPage
from tkinter import *
from app import config
from app.core.new_user_view import NewUserPage
import random
from PIL import ImageTk, Image


class MainPage(Frame):
    def __init__(self, parent, controller, saved_data):
        Frame.__init__(self, parent)
        self.controller = controller
        self.saved_data = saved_data
        self.last_user = saved_data['last_user']
        self.grid(row=0, column=0, sticky="nsew")

        Label(self, text=self.greeting(), font=controller.title_font, pady=10).pack()
        Label(self, text=config.DESCRIPTION_MAIN, font=controller.font, wraplength=config.WINDOW_WIDTH - 20).pack()
        Button(self, text=f'Continue as {self.last_user}',
               command=lambda: PracticePage(parent=parent, controller=self.controller,
                                            current_user=saved_data[self.last_user]).tkraise()).pack()
        Button(self, text='See complete stats', command=lambda: UserPage(parent=parent,
                                                                         controller=self.controller,
                                                                         current_user=self.saved_data[self.last_user],
                                                                         session_attempts=0,
                                                                         session_misspelled_lst=0).tkraise()).pack()
        Button(self, text='Choose a different User',
               command=lambda: ChooseDifferentUserPage(parent=parent,
                                                       controller=self.controller,
                                                       saved_data=self.saved_data).tkraise()).pack()
        Button(self, text='New User',
               command=lambda: NewUserPage(parent=parent,
                                           controller=self.controller).tkraise()).pack()
        Button(self, text='Exit', command=self.controller.destroy).pack()

    def greeting(self):
        return config.GREETING_MAIN.format(self.last_user, random.choice(config.GREETING_EMOJI))
