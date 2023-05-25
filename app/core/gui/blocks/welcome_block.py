import random
import tkinter as tk

from PIL import Image
from customtkinter import CTkFrame, CTkLabel, CTkImage, CTkFont

from core import strings, config
from core.gui.elements import CTAButton
from core.gui.views.base_view import BaseFrame
from util import helpers


class WelcomeBlock(BaseFrame):
    def __init__(self, parent, controller, last_user=None, saved_data=None, next_page=None):
        BaseFrame.__init__(self, parent, controller, width=config.WINDOW_WIDTH - 100, height=config.WINDOW_HEIGHT - 250)
        self.parent = parent
        self.controller = controller
        self.last_user = last_user
        self.saved_data = saved_data
        self.next_page = next_page
        self.grid_propagate(False)

        if self.last_user:
            self.title_text = strings.MAIN_PAGE_TITLE.format(random.choice(strings.GREETING_EMOJI))
            self.title = CTkLabel(self, text=self.title_text, font=self.controller.title_font)
            self.cta_button = CTAButton(self, font=CTkFont(family="Arial", size=config.FONT_SIZE),
                                        image=self.button_image(), text=strings.CONTINUE_LEARNING,
                                        command=lambda: self.next_page.tkraise())
            self.avatar = self.load_user_avatar(self.saved_data[self.last_user])
            self.avatar_label = CTkLabel(self, text="", image=self.avatar)
            self.username = CTkLabel(self, text=self.last_user, font=CTkFont(family="Arial", weight="bold",
                                                                             size=config.HEADER_FONT_SIZE))
            body_frame = CTkFrame(self)
            tip_icon = CTkImage(Image.open(helpers.get_path('assets/idea.png')), size=(20, 20))
            block_body = CTkLabel(body_frame, text=self.tip_of_the_day(), image=tip_icon, padx=5, compound=tk.LEFT,
                                  wraplength=600, justify=tk.LEFT)
            block_body.pack(pady=10, padx=5)

            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(2, weight=1)

            self.title.grid(row=0, column=0, columnspan=3, padx=15, pady=15)
            self.avatar_label.grid(row=1, column=0, columnspan=3)
            self.username.grid(row=2, column=0, columnspan=3)
            body_frame.grid(row=3, column=0, columnspan=3, pady=(20, 0))
            self.cta_button.grid(row=4, column=0, columnspan=3, pady=(20, 0))
        else:
            self.title_text = strings.WELCOME_PAGE_TITLE
            self.title = CTkLabel(self, text=self.title_text, font=self.controller.title_font)
            self.cta_button = CTAButton(self, font=CTkFont(family="Arial", size=config.FONT_SIZE),
                                        image=self.button_image(), compound=tk.LEFT, text=strings.START_LEARNING,
                                        command=lambda: self.next_page.tkraise())
            self.block_body = CTkLabel(self, text=strings.WELCOME_PAGE_TEXT, wraplength=400, justify=tk.LEFT)

            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(2, weight=1)

            self.title.grid(row=0, column=0, columnspan=3, padx=15, pady=15)
            self.block_body.grid(row=1, column=0, columnspan=3)
            self.cta_button.grid(row=2, column=1, pady=(25, 0))

    def change_current_user(self, new_user):
        # Needed for change user feature
        self.avatar = self.load_user_avatar(new_user)
        self.username.configure(text=new_user.name)
        self.avatar_label.configure(image=self.avatar)

    @staticmethod
    def tip_of_the_day():
        return random.choice(strings.SPELLING_TIPS)

    @staticmethod
    def button_image():
        return CTkImage(Image.open(helpers.get_path('assets/learn.png')), size=(20, 20))

    def load_user_avatar(self, user):
        try:
            return CTkImage(Image.open(helpers.get_path(f'assets/avatars/{user.avatar}')), size=(100, 100))
        except FileNotFoundError:
            user.avatar = user.pick_random_avatar()
            return self.load_user_avatar(user)
