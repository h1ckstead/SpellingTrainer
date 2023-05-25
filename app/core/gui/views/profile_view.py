from tkinter import Label, BooleanVar

from PIL import Image
from customtkinter import CTkLabel, CTkImage, CTkFont

from core import config, strings
from core.gui.elements import Button, CTAButton, HintLabel, GreyLine, StrictSpellingSwitch, StaticsLabel, ThickLine, \
    CustomToolTip
from core.gui.views.base_view import BaseView, BaseFrame
from core.gui.views.vocabulary_view import VocabularyPage
from util import helpers
import tkinter as tk


class ProfilePage(BaseView):
    def __init__(self, parent, controller, current_user, main_page, previous_page, session):
        super().__init__(parent, controller)
        self.parent = parent
        self.controller = controller
        self.current_user = current_user
        self.main_page = main_page
        self.previous_page = previous_page  # Practice Page
        self.session = session

        # Create widgets and content blocks
        self.title_text = Label(self, text=strings.PROFILE_PAGE_TITLE, font=self.controller.title_font,
                                background="#333333", foreground="#FFFFFF")
        self.user_block = UserBlock(self, self.controller, self.current_user)
        self.overall_statistics_block = StatisticsBlock(self, self.controller, current_user=self.current_user)
        self.session_statistics_block = StatisticsBlock(self, self.controller, session=self.session)
        self.show_vocab_btn = CTAButton(self, text=strings.SHOW_VOCAB, width=200,
                                        command=lambda: VocabularyPage(parent=self.parent, controller=self.controller,
                                                                       previous_page=self,
                                                                       current_user=self.current_user).tkraise())
        self.back_to_main_btn = Button(self, text=strings.BACK_TO_MAIN_BTN_TEXT,
                                       command=lambda: self.main_page.tkraise())
        self.back_to_learning = CTAButton(self, text=strings.BACK_TO_LEARNING, image=self.learn_button_image,
                                          compound="left", command=self.update_previous_and_raise)
        # self.line = GreyLine(self, width=650)
        self.pencil_icon = CTkLabel(self, text="",
                                    image=CTkImage(Image.open(helpers.get_path('assets/pencil.png')), size=(30, 30)))

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(7, weight=1)

        self.title_text.grid(row=1, column=0, columnspan=6, pady=10)
        self.user_block.grid(row=2, column=1, rowspan=2, sticky=tk.N)
        self.overall_statistics_block.grid(row=2, column=2, columnspan=3, padx=10, sticky=tk.NSEW)
        self.session_statistics_block.grid(row=3, column=2, columnspan=3, padx=10, pady=(20, 0), sticky=tk.NSEW)
        self.show_vocab_btn.grid(row=3, column=1, sticky=tk.SE)
        self.horizontal_line.grid(row=5, column=0, columnspan=6, pady=30)
        self.back_to_main_btn.grid(row=6, column=1)
        self.close_button.grid(row=6, column=2, sticky=tk.W)
        self.back_to_learning.grid(row=6, column=4, sticky=tk.E)
        self.report_bug_btn.grid(row=8, column=0, columnspan=6, pady=(0, 5))

    def update_previous_and_raise(self):
        if not self.previous_page.spelling_trainer_block.is_play_btn_on and not self.current_user.only_from_vocabulary:
            self.previous_page.spelling_trainer_block.new_word()
            self.previous_page.spelling_trainer_block.turn_on_play_btn()
        self.previous_page.tkraise()


class UserBlock(BaseFrame):
    def __init__(self, parent, controller, current_user):
        BaseFrame.__init__(self, parent, controller, width=config.WINDOW_WIDTH - 500)
        self.parent = parent
        self.controller = controller
        self.current_user = current_user

        self.avatar = CTkLabel(self, text="",
                               image=CTkImage(
                                   Image.open(helpers.get_path(f"assets/avatars/{self.current_user.avatar}")),
                                   size=(60, 60)))
        self.username = CTkLabel(self, text=self.current_user.name, font=CTkFont(None, config.HEADER_FONT_SIZE,
                                                                                 weight="bold"))
        self.edit_btn = Button(self, text="Edit profile",
                               image=CTkImage(Image.open(helpers.get_path('assets/edit.png')), size=(15, 15)),
                               width=30, height=25, corner_radius=10, compound="left",
                               command=lambda: self.edit_page().tkraise())
        self.horizontal_line = GreyLine(self, width=180)
        self.strict_spelling_switch = StrictSpellingSwitch(self,
                                                           command=lambda: self.current_user.toggle_strict_spelling(
                                                               self.strict_spelling_switch.get()))
        self.configure_strict_spelling_switch()
        self.strict_spelling_hint = HintLabel(self, text=strings.STRICT_SPELLING_HINT, image=False)

        self.avatar.grid(row=0, column=0, pady=(10, 0))
        self.username.grid(row=1, column=0, pady=(0, 5))
        self.edit_btn.grid(row=2, column=0)
        self.horizontal_line.grid(row=3, column=0, pady=10)
        self.strict_spelling_switch.grid(row=4, column=0, padx=10, sticky="w")
        self.strict_spelling_hint.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="w")

    def edit_page(self):
        from core.gui.views.edit_profile_view import EditProfilePage
        return EditProfilePage(parent=self.parent.master, controller=self.controller,
                               previous_page=self.parent,
                               current_user=self.current_user)

    def configure_strict_spelling_switch(self):
        switch_var = BooleanVar(value=self.current_user.strict_spelling)
        self.strict_spelling_switch.configure(variable=switch_var)

    def update_profile(self):
        self.avatar.configure(text="",
                              image=CTkImage(Image.open(helpers.get_path(f"assets/avatars/{self.current_user.avatar}")),
                                             size=(60, 60)))
        self.username.configure(text=self.current_user.name)


class StatisticsBlock(BaseFrame):
    def __init__(self, parent, controller, current_user=None, session=None):
        BaseFrame.__init__(self, parent, controller)
        self.parent = parent
        self.controller = controller
        self.current_user = current_user
        self.session = session
        # self.grid_propagate(False)

        if current_user:
            self.header_text = CTkLabel(self, text=strings.OVERALL_STATISTICS,
                                        font=CTkFont(None, config.STATISTICS_FONT_SIZE))
            self.attempts = StaticsLabel(self, text=self.current_user.total_attempts)
            self.attempts_tip = CustomToolTip(self.attempts, msg="Overall number of times\n you've spelled words")
            self.correctly = StaticsLabel(self, text=self.current_user.attempts_correct)
            self.correctly_tip = CustomToolTip(self.correctly, msg="Number of times you\n correctly spelled words")
            self.learned_words = CTkLabel(self, text=len(current_user.dictionaries.learned_words.keys()),
                                          font=CTkFont(family=None, size=config.TITLE_FONT_SIZE, weight="bold"),
                                          text_color="#6bbe66")
            self.learned_words_tip = CustomToolTip(self.learned_words, msg="The number of words you've consistently\n "
                                                                           "spelled correctly and now you know\n how "
                                                                           "to spell them")
            self.to_learn = StaticsLabel(self, text=len(current_user.dictionaries.vocabulary.keys()))
            self.to_learn_tip = CustomToolTip(self.to_learn, msg="Words in your vocabulary\n "
                                                                 "which require more practice")
            self.to_learn_label = CTkLabel(self, text=strings.TO_LEARN)

            self.incorrectly = StaticsLabel(self, text=self.current_user.attempts_incorrect)
            self.incorrectly_tip = CustomToolTip(self.incorrectly, msg="The number of attempts to spell a word\n "
                                                                       "resulted in a spelling mistake")
        else:
            self.header_text = CTkLabel(self, text=strings.SESSION_STATISTICS,
                                        font=CTkFont(None, config.STATISTICS_FONT_SIZE))
            self.attempts = StaticsLabel(self, text=self.session.total_attempts)
            self.session_attempts_tip = CustomToolTip(self.attempts, msg="Overall number of times\n "
                                                                         "you've spelled words")
            self.correctly = StaticsLabel(self, text=self.session.attempts_correct)
            self.session_correctly = CustomToolTip(self.correctly, msg="Number of times you\n correctly spelled words")
            self.learned_words = CTkLabel(self, text=session.learned_words, text_color="#6bbe66",
                                          font=CTkFont(family=None, size=config.TITLE_FONT_SIZE, weight="bold"))
            self.session_learned_words = CustomToolTip(self.learned_words, msg="The number of words that you've\n"
                                                                               " learned during this learning session")
            self.to_learn = StaticsLabel(self, text=self.session.new_words)
            self.session_to_learn = CustomToolTip(self.to_learn, msg="Words which have been added to your vocabulary\n "
                                                                     "and need more practice")
            self.to_learn_label = CTkLabel(self, text=strings.NEW_WORDS)
            self.incorrectly = StaticsLabel(self, text=self.session.attempts_incorrect)
            self.session_incorrectly = CustomToolTip(self.incorrectly, msg="The number of spelling mistakes you've\n"
                                                                           " made during this learning session")

        self.blue_line = ThickLine(self, progress_color="#5399cf")
        self.light_green_line = ThickLine(self, progress_color="#1ea689")
        self.green_line = ThickLine(self, progress_color=config.GREEN)
        self.yellow_line = ThickLine(self, progress_color="#f9c632")
        self.red_line = ThickLine(self, progress_color="#ef4831")

        self.attempts_label = CTkLabel(self, text=strings.ATTEMPTS)
        self.correctly_label = CTkLabel(self, text=strings.CORRECTLY)
        self.learned_words_label = CTkLabel(self, text=strings.LEARNED_WORDS)
        self.incorrectly_label = CTkLabel(self, text=strings.INCORRECTLY)

        self.header_text.grid(row=0, column=1, columnspan=3, pady=10)
        self.attempts.grid(row=1, column=0)
        self.correctly.grid(row=1, column=1)
        self.learned_words.grid(row=1, column=2)
        self.to_learn.grid(row=1, column=3)
        self.incorrectly.grid(row=1, column=4)

        self.blue_line.grid(row=2, column=0, padx=27)
        self.light_green_line.grid(row=2, column=1)
        self.green_line.grid(row=2, column=2, padx=27)
        self.yellow_line.grid(row=2, column=3)
        self.red_line.grid(row=2, column=4, padx=27)

        self.attempts_label.grid(row=3, column=0)
        self.correctly_label.grid(row=3, column=1)
        self.learned_words_label.grid(row=3, column=2, pady=(0, 10))
        self.to_learn_label.grid(row=3, column=3)
        self.incorrectly_label.grid(row=3, column=4)
