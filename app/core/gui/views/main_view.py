import logging

from core import strings
from core.gui.blocks.welcome_block import WelcomeBlock
from core.gui.elements import Button
from core.gui.views.base_view import BaseView
from core.gui.views.change_user_view import ChangeUserPage
from core.gui.views.practice_view import PracticePage
from core.gui.views.profile_view import ProfilePage
from core.session import Session


class MainPage(BaseView):
    def __init__(self, parent, controller, saved_data, session=None):
        super().__init__(parent, controller)
        self.parent = parent
        self.controller = controller
        self.saved_data = saved_data
        self.last_user = saved_data['last_user']
        if not session:
            logging.info(f"Creating session from Main Page for user: {self.last_user}")
            self.session = Session()
        else:
            self.session = session

        self.welcome_block = WelcomeBlock(self, self.controller, self.last_user, self.saved_data,
                                          next_page=self.practice_page())

        self.change_user_btn = Button(self, text=strings.CHANGE_USER,
                                      command=lambda: ChangeUserPage(parent=self.parent,
                                                                     controller=self.controller,
                                                                     previous_page=self,
                                                                     saved_data=self.saved_data).tkraise())
        self.user_profile_btn = Button(self, text=strings.PROFILE_BTN,
                                       command=lambda: ProfilePage(parent=self.parent, controller=self.controller,
                                                                   previous_page=self.practice_page(),
                                                                   current_user=saved_data[self.last_user],
                                                                   session=self.session, main_page=self))

        # Display widgets and content blocks on the page
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.welcome_block.grid(row=0, column=0, columnspan=3, pady=(40, 20))
        self.change_user_btn.grid(row=1, column=0, padx=(17, 0))
        self.user_profile_btn.grid(row=1, column=1, columnspan=2, padx=(0, 72))
        self.pencil_icon.grid(row=2, column=2, sticky="e", padx=(0, 80))
        self.horizontal_line.grid(row=2, column=0, columnspan=3, sticky="s", pady=(0, 3))
        self.close_button.grid(row=3, column=1, columnspan=2, padx=(0, 72), pady=(20, 0))
        self.report_bug_btn.grid(row=4, column=0, columnspan=3, pady=(50, 0))

    def practice_page(self):
        return PracticePage(parent=self.parent, controller=self.controller,
                            current_user=self.saved_data[self.last_user], previous_page=self, session=self.session)