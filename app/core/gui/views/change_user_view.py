import tkinter as tk
from tkinter import StringVar, Label

from PIL import Image
from customtkinter import CTkFrame, CTkComboBox, CTkFont, CTkImage

from core import config, strings
from core.gui.elements import Button, CTAButton, GreyLine
from core.gui.views.base_view import BaseView
from core.gui.views.practice_view import PracticePage
from core.gui.views.user_registration_view import UserRegistrationPage
from core.session import Session
from util import helpers


class ChangeUserPage(BaseView):
    def __init__(self, parent, controller, previous_page, saved_data):
        super().__init__(parent, controller)
        self.parent = parent
        self.controller = controller
        self.previous_page = previous_page
        self.saved_data = saved_data
        self.current_user = self.get_current_user()

        # Practice page is initialized here and not in the content block to avoid hover bug on Entry field
        self.practice_page = PracticePage(parent=self.parent, controller=self.controller,
                                          current_user=self.current_user, previous_page=self.previous_page,
                                          session=Session())
        self.content_block = ContentBlock(self, controller=self.controller, saved_data=self.saved_data,
                                          practice_page=self.practice_page)
        self.back_btn = Button(self, strings.BACK_TO_MAIN_BTN_TEXT, command=lambda: previous_page.tkraise())

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.content_block.grid(row=1, column=1, columnspan=2, sticky=tk.NSEW, pady=(0, 55))
        self.horizontal_line.grid(row=3, column=1, columnspan=2, pady=30)
        self.back_btn.grid(row=4, column=1, sticky=tk.W)
        self.close_button.grid(row=4, column=2, sticky=tk.E)
        self.report_bug_btn.grid(row=6, column=0, columnspan=4, sticky=tk.S, pady=(0, 5))

    def get_current_user(self):
        last_user = self.saved_data["last_user"]
        return self.saved_data[last_user]


class ContentBlock(CTkFrame):
    def __init__(self, parent, controller, saved_data, practice_page):
        CTkFrame.__init__(self, parent, width=config.WINDOW_WIDTH - 380, height=config.WINDOW_HEIGHT - 250)
        self.parent = parent
        self.controller = controller
        self.saved_data = saved_data
        self.practice_page = practice_page
        self.grid_propagate(False)

        users = [k for k in self.saved_data.keys() if k != 'last_user']
        default_value = StringVar(value=saved_data["last_user"])
        self.title_text = Label(self, text=strings.CHANGE_USER_TITLE, font=self.controller.title_font,
                                background="#2b2b2b", foreground="#FFFFFF")
        self.dropdown = CTkComboBox(self, state="readonly", cursor="arrow", values=users, variable=default_value,
                                    width=175)
        self.dropdown.focus_set()  # To avoid bug where default_value appears only on hover
        self.continue_learning_btn = CTAButton(self, text=strings.CONTINUE_LEARNING, image=self.button_image(),
                                               font=CTkFont(family="Arial", size=config.FONT_SIZE),
                                               command=lambda: [self.update_pages(), self.practice_page.tkraise(),
                                                                self.saved_data[self.dropdown.get()].save_progress()
                                                                ])
        self.horizontal_line = GreyLine(self, height=3, width=config.WINDOW_WIDTH - 450)
        self.create_new_user_btn = Button(self, text=strings.CREATE_NEW,
                                          command=lambda: UserRegistrationPage(self.parent.master, self.controller,
                                                                               self.parent).tkraise())

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.title_text.grid(row=0, column=1)
        self.dropdown.grid(row=1, column=1, pady=(25, 15))
        self.continue_learning_btn.grid(row=2, column=1)
        self.horizontal_line.grid(row=3, column=1, pady=(120, 15))
        self.create_new_user_btn.grid(row=4, column=1)

    def update_pages(self):
        user = self.saved_data[self.dropdown.get()]
        self.parent.previous_page.welcome_block.change_current_user(user)
        self.practice_page.change_current_user(user)

    @staticmethod
    def button_image():
        return CTkImage(Image.open(helpers.get_path('assets/learn.png')), size=(20, 20))
