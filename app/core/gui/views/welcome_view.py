from core.gui.blocks.welcome_block import WelcomeBlock
from core.gui.views.base_view import BaseView
from core.gui.views.user_registration_view import UserRegistrationPage
import tkinter as tk


class WelcomePage(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.parent = parent
        self.controller = controller

        self.welcome_block = WelcomeBlock(self, self.controller,
                                          next_page=UserRegistrationPage(self.parent, self.controller, self))

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.welcome_block.grid(row=1, column=1, columnspan=2, pady=50)
        self.horizontal_line.grid(row=2, column=0, columnspan=4, pady=30)
        self.close_button.grid(row=3, column=2, sticky=tk.E)
        self.report_bug_btn.grid(row=5, column=0, columnspan=4, pady=(0, 5))
