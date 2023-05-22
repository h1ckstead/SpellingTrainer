import logging
import tkinter as tk

from PIL import Image
from customtkinter import CTkImage

from core import strings
from core.gui.blocks.registration_edit_block import RegistrationEditBlock
from core.gui.elements import CTAButton, Button
from core.gui.views.base_view import BaseView
from core.gui.views.practice_view import PracticePage
from core.session import Session
from core.user import User
from util import helpers


class UserRegistrationPage(BaseView):
    def __init__(self, parent, controller, previous_page):
        super().__init__(parent, controller)
        self.parent = parent
        self.controller = controller
        self.previous_page = previous_page
        self.current_user = None

        self.registration_block = RegistrationEditBlock(self, self.controller)
        self.back_btn = Button(self, strings.BACK_BUTTON_TEXT, command=lambda: self.previous_page.tkraise())
        new_user_img = CTkImage(Image.open(helpers.get_path('assets/new_user.png')), size=(20, 20))
        self.save_btn = CTAButton(self, text=strings.CREATE_USER, state=tk.DISABLED, image=new_user_img,
                                  compound=tk.LEFT,
                                  command=lambda: [self.create_user(),
                                                   PracticePage(parent=self.parent, controller=self.controller,
                                                                current_user=self.current_user,
                                                                previous_page=self.main_page(),
                                                                session=Session()).tkraise()])

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.registration_block.grid(row=0, column=0, columnspan=3, pady=(15, 0))
        self.back_btn.grid(row=1, column=0, pady=(20, 0))
        self.save_btn.grid(row=1, column=2, columnspan=2, pady=(20, 0))
        self.report_bug_btn.grid(row=4, column=0, columnspan=3, pady=(30, 0))

    def create_user(self):
        username = self.registration_block.get_username()
        strict_spelling = self.registration_block.get_strict_spelling_value()
        avatar = self.registration_block.selected_avatar
        self.current_user = User(username, strict_spelling, avatar)
        logging.info(f"User {self.current_user} has been created")

    def main_page(self):
        from core.gui.views.main_view import MainPage
        import util.load_savefile as load_savefile

        saved_data = load_savefile.load_save()
        return MainPage(parent=self.parent, controller=self.controller, saved_data=saved_data)
