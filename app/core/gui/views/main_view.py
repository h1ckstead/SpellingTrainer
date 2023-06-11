import logging
import tkinter as tk

from core import strings
from core.gui.blocks.welcome_block import WelcomeBlock
from core.gui.elements import Button
from core.gui.views.base_view import BaseView
from core.gui.views.change_user_view import ChangeUserPage
from core.gui.views.practice_view import PracticePage
from core.gui.views.profile_view import ProfilePage
from core.session import Session


class MainPage(BaseView):
    def __init__(self, parent, controller, current_user, saved_data=None, session=None):
        super().__init__(parent, controller)
        self.parent = parent
        self.controller = controller
        self.saved_data = saved_data
        self.current_user = current_user
        if not session:
            logging.info(f"Creating session from Main Page for user: {self.current_user.name}")
            self.session = Session()
        else:
            self.session = session

        # Create widgets
        self.welcome_block = WelcomeBlock(parent=self, controller=self.controller, current_user=self.current_user,
                                          next_page=self.practice_page())
        self.change_user_btn = Button(self, text=strings.CHANGE_USER,
                                      command=lambda: ChangeUserPage(parent=self.parent,
                                                                     controller=self.controller,
                                                                     current_user=self.current_user,
                                                                     saved_data=self.saved_data,
                                                                     previous_page=self).tkraise())
        self.user_profile_btn = Button(self, text=strings.PROFILE_BTN,
                                       command=lambda: ProfilePage(parent=self.parent, controller=self.controller,
                                                                   previous_page=self.practice_page(),
                                                                   current_user=self.current_user,
                                                                   session=self.session, main_page=self))

        # Display widgets and content blocks on the page
        self.configure_rows_and_columns()
        self.display_widgets_on_page()

    def configure_rows_and_columns(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(6, weight=1)

    def display_widgets_on_page(self):
        self.welcome_block.grid(row=1, column=1, columnspan=2, sticky=tk.NSEW, pady=(0, 20))
        self.change_user_btn.grid(row=3, column=1, sticky=tk.W)
        self.user_profile_btn.grid(row=3, column=2, sticky=tk.E)
        self.horizontal_line.grid(row=4, column=1, columnspan=2, pady=30)
        self.close_button.grid(row=5, column=2, sticky=tk.E)
        self.report_bug_btn.grid(row=7, column=0, columnspan=4, sticky=tk.S, pady=(0, 5))

    def practice_page(self):
        return PracticePage(parent=self.parent, controller=self.controller,
                            current_user=self.current_user,
                            previous_page=self, session=self.session)
