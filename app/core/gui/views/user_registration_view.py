import logging
import tkinter as tk
from tkinter import messagebox

from PIL import Image
from customtkinter import CTkImage

from core import strings
from core.gui.blocks.registration_edit_block import RegistrationEditBlock
from core.gui.elements import CTAButton, Button
from core.gui.views.base_view import BaseView
from core.session import Session
from core.user import User
from util import helpers


class UserRegistrationPage(BaseView):
    def __init__(self, parent, controller, previous_page):
        super().__init__(parent, controller)
        self.parent = parent
        self.controller = controller
        self.previous_page = previous_page  # Main/Welcome page
        self.current_user = None

        self.registration_block = RegistrationEditBlock(self, self.controller)
        self.back_btn = Button(self, strings.BACK_BUTTON_TEXT, command=lambda: self.previous_page.tkraise())
        new_user_img = CTkImage(Image.open(helpers.get_path('assets/new_user.png')), size=(20, 20))
        self.save_btn = CTAButton(self, text=strings.CREATE_USER, state=tk.DISABLED, image=new_user_img,
                                  compound=tk.LEFT, command=self.create_user)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.registration_block.grid(row=0, column=0, columnspan=3, pady=(15, 0))
        self.back_btn.grid(row=2, column=0, pady=(20, 0))
        self.save_btn.grid(row=2, column=2, columnspan=2, pady=(20, 0))
        self.report_bug_btn.grid(row=5, column=0, columnspan=3, pady=(0, 5))

    def create_user(self):
        username = self.registration_block.get_username()
        if hasattr(self.previous_page, 'saved_data') and username in self.previous_page.saved_data["users"]:
            messagebox.showerror(message=f"User {username} already exists")
        else:
            strict_spelling = self.registration_block.get_strict_spelling_value()
            avatar = self.registration_block.selected_avatar
            self.current_user = User(username, strict_spelling, avatar)
            self.session = Session()
            logging.info(f"User {self.current_user} has been created")
            main_page = self.main_page()
            main_page.welcome_block.next_page.tkraise()

    def main_page(self):
        from core.gui.views.main_view import MainPage

        if self.previous_page:
            self.previous_page.destroy()

        saved_data = helpers.load_save()
        return MainPage(parent=self.parent, controller=self.controller, current_user=self.current_user,
                        saved_data=saved_data, session=self.session)
