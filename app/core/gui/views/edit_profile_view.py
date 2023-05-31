from core import strings
from core.gui.blocks.registration_edit_block import RegistrationEditBlock
from core.gui.elements import CTAButton, Button
from core.gui.views.base_view import BaseView
from util import helpers


class EditProfilePage(BaseView):
    def __init__(self, parent, controller, previous_page, current_user):
        super().__init__(parent, controller)
        self.parent = parent
        self.controller = controller
        self.previous_page = previous_page
        self.current_user = current_user

        self.profile_edit_block = RegistrationEditBlock(parent=self, controller=self.controller,
                                                        current_user=self.current_user)
        self.cancel_btn = Button(self, strings.CANCEL, command=lambda: self.previous_page.tkraise())
        self.save_btn = CTAButton(self, strings.SAVE, command=lambda: [self.save_changes(),
                                                                       self.previous_page.tkraise()])

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.profile_edit_block.grid(row=0, column=0, columnspan=3, pady=(40, 30))
        self.cancel_btn.grid(row=1, column=0, pady=(20, 0))
        self.save_btn.grid(row=1, column=2, columnspan=2, pady=(20, 0))
        self.report_bug_btn.grid(row=4, column=0, columnspan=3, pady=(42, 0))

    def save_changes(self):
        new_username = self.profile_edit_block.get_username()
        self.current_user.edit_username(new_username)
        self.current_user.edit_avatar(self.profile_edit_block.selected_avatar)

        # Update existing pages
        self.previous_page.user_block.update_profile()
        self.previous_page.main_page.saved_data = helpers.load_save()
        self.previous_page.main_page.welcome_block.change_current_user(self.current_user)
