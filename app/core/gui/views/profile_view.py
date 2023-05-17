from tkinter import Label

from PIL import Image
from customtkinter import CTkLabel, CTkImage, CTkFont, StringVar

from core import config, strings
from core.gui.elements import Button, CTAButton, HintLabel, GreyLine, StrictSpellingSwitch, StaticsLabel, ThickLine
from core.gui.views.base_view import BaseView, BaseFrame
from core.gui.views.vocabulary_view import VocabularyPage


class ProfilePage(BaseView):
    def __init__(self, parent, controller, current_user, main_page, previous_page, session):
        super().__init__(parent, controller)
        self.parent = parent
        self.controller = controller
        self.current_user = current_user
        self.main_page = main_page
        self.previous_page = previous_page
        self.session = session

        # Create widgets and content blocks
        self.title_text = Label(self, text=strings.PROFILE_PAGE_TITLE, font=self.controller.title_font)
        self.user_block = UserBlock(self, self.controller, self.current_user)
        self.overall_statistics_block = StatisticsBlock(self, self.controller, current_user=self.current_user)
        self.session_statistics_block = StatisticsBlock(self, self.controller, session=self.session)
        self.show_vocab_btn = CTAButton(self, text=strings.SHOW_VOCAB, width=215,
                                        command=lambda: VocabularyPage(parent=self.parent, controller=self.controller,
                                                                       previous_page=self,
                                                                       current_user=self.current_user).tkraise())
        self.back_to_main_btn = Button(self, text=strings.BACK_TO_MAIN_BTN_TEXT,
                                       command=lambda: self.main_page.tkraise())
        self.back_to_learning = CTAButton(self, text=strings.BACK_TO_LEARNING,
                                          command=lambda: self.previous_page.tkraise())
        self.line = GreyLine(self, width=650)
        self.pencil_icon = CTkLabel(self, text="", image=CTkImage(Image.open("assets/pencil.png"), size=(30, 30)))

        self.title_text.grid(row=0, column=2, columnspan=4, padx=(0, 210), pady=20)
        self.user_block.grid(row=1, column=0, rowspan=3, columnspan=2, padx=20, sticky="n")
        self.overall_statistics_block.grid(row=1, column=2, columnspan=2, pady=(0, 20))
        self.session_statistics_block.grid(row=2, column=2, columnspan=2)
        self.show_vocab_btn.grid(row=2, column=0, columnspan=2, sticky="s")
        self.pencil_icon.grid(row=4, column=3, padx=(350, 0), pady=(40, 0))
        self.line.grid(row=5, column=0, columnspan=4, pady=(0, 40))
        self.back_to_main_btn.grid(row=6, column=0)
        self.close_button.grid(row=6, column=0, columnspan=3, padx=(190, 0))
        self.back_to_learning.grid(row=6, column=3, sticky="e")
        self.report_bug_btn.grid(row=7, column=0, columnspan=4, padx=(42, 0), pady=(71, 0))


class UserBlock(BaseFrame):
    def __init__(self, parent, controller, current_user):
        BaseFrame.__init__(self, parent, controller, width=config.WINDOW_WIDTH - 500)
        self.parent = parent
        self.controller = controller
        self.current_user = current_user

        self.avatar = CTkLabel(self, text="",
                               image=CTkImage(Image.open(f"assets/avatars/{self.current_user.avatar}"), size=(60, 60)))
        self.username = CTkLabel(self, text=self.current_user.name, font=CTkFont(None, config.HEADER_FONT_SIZE,
                                                                                 weight="bold"))
        self.edit_btn = Button(self, text="Edit profile", image=CTkImage(Image.open(f"assets/edit.png"), size=(15, 15)),
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
        switch_var = StringVar(value=self.current_user.strict_spelling)
        self.strict_spelling_switch.configure(variable=switch_var)

    def update_profile(self):
        self.avatar.configure(text="",
                              image=CTkImage(Image.open(f"assets/avatars/{self.current_user.avatar}"), size=(60, 60)))
        self.username.configure(text=self.current_user.name)


class StatisticsBlock(BaseFrame):
    def __init__(self, parent, controller, current_user=None, session=None):
        BaseFrame.__init__(self, parent, controller, width=config.WINDOW_WIDTH - 500)
        self.parent = parent
        self.controller = controller
        self.current_user = current_user
        self.session = session

        if current_user:
            self.header_text = CTkLabel(self, text=strings.OVERALL_STATISTICS,
                                        font=CTkFont(None, config.STATISTICS_FONT_SIZE))
            self.attempts = StaticsLabel(self, text=self.current_user.total_attempts)
            self.correctly = StaticsLabel(self, text=self.current_user.attempts_correct)
            self.learned_words = CTkLabel(self, text=len(current_user.dictionaries.learned_words.keys()),
                                          font=CTkFont(family=None, size=config.TITLE_FONT_SIZE, weight="bold"),
                                          text_color="#0a5826")
            self.to_learn = StaticsLabel(self, text=len(current_user.dictionaries.vocabulary.keys()))
            self.to_learn_label = CTkLabel(self, text=strings.TO_LEARN)
            self.incorrectly = StaticsLabel(self, text=self.current_user.attempts_incorrect)
        else:
            self.header_text = CTkLabel(self, text=strings.SESSION_STATISTICS,
                                        font=CTkFont(None, config.STATISTICS_FONT_SIZE))
            self.attempts = StaticsLabel(self, text=self.session.total_attempts)
            self.correctly = StaticsLabel(self, text=self.session.attempts_correct)
            self.learned_words = CTkLabel(self, text=session.learned_words, text_color="#0a5826",
                                          font=CTkFont(family=None, size=config.TITLE_FONT_SIZE, weight="bold"))
            self.to_learn = StaticsLabel(self, text=self.session.new_words)
            self.to_learn_label = CTkLabel(self, text=strings.NEW_WORDS)
            self.incorrectly = StaticsLabel(self, text=self.session.attempts_incorrect)

        self.blue_line = ThickLine(self, progress_color="#359ded")
        self.light_green_line = ThickLine(self, progress_color="#1ea689")
        self.green_line = ThickLine(self, progress_color="#0a5826")
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

        self.blue_line.grid(row=2, column=0, padx=20)
        self.light_green_line.grid(row=2, column=1)
        self.green_line.grid(row=2, column=2, padx=20)
        self.yellow_line.grid(row=2, column=3)
        self.red_line.grid(row=2, column=4, padx=20)

        self.attempts_label.grid(row=3, column=0)
        self.correctly_label.grid(row=3, column=1)
        self.learned_words_label.grid(row=3, column=2, pady=(0, 10))
        self.to_learn_label.grid(row=3, column=3)
        self.incorrectly_label.grid(row=3, column=4)
