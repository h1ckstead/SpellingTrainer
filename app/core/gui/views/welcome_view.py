from core.gui.blocks.welcome_block import WelcomeBlock
from core.gui.views.base_view import BaseView
from core.gui.views.user_registration_view import UserRegistrationPage


class WelcomePage(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.parent = parent
        self.controller = controller

        self.welcome_block = WelcomeBlock(self, self.controller,
                                          next_page=UserRegistrationPage(self.parent, self.controller, self))

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.welcome_block.grid(row=0, column=0, columnspan=3, pady=50)
        self.horizontal_line.grid(row=1, column=0, columnspan=3, sticky="s", pady=(0, 3))
        self.pencil_icon.grid(row=1, column=2, sticky="e", padx=(0, 80))
        self.close_button.grid(row=2, column=2, sticky="e", padx=(0, 100), pady=(20, 0))
        self.report_bug_btn.grid(row=3, column=0, columnspan=3, pady=(45, 0))
