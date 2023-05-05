from tkinter import *

from PIL import Image
from customtkinter import CTkFrame, CTkLabel, CTkImage, CTkProgressBar, CTkEntry, CTkButton
from app.core.user_vocabulary_view import UserVocabularyPage

from app import config


# noinspection PyTypeChecker
class UserPage(CTkFrame):
    def __init__(self, parent, controller, current_user, session_attempts_correct, session_attempts_incorrect):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.current_user = current_user
        self.session_attempts_correct = session_attempts_correct
        self.session_attempts_incorrect = session_attempts_incorrect
        self.grid(row=0, column=0, sticky="nsew")

        # Header
        # self.avatar().grid(row=0, column=2, pady=10)
        self.user_name().grid(row=0, column=2, pady=10)
        self.description("Your overall statistics").grid(row=1, column=2)

        # Total attempts
        self.stats_int(self.current_user.attempts_correct + self.current_user.attempts_incorrect).grid(row=2, column=0)
        self.short_line().grid(row=3, column=0, padx=5)
        self.stats_description("Attempts").grid(row=4, column=0)

        # Correctly spelled words
        self.stats_int(self.current_user.attempts_correct).grid(row=2, column=1)
        self.short_line(progress_color='light green').grid(row=3, column=1, padx=15)
        self.stats_description("Correctly").grid(row=4, column=1)

        # Incorrectly spelled words
        self.stats_int(self.current_user.attempts_incorrect).grid(row=2, column=2)
        self.short_line(progress_color="red").grid(row=3, column=2, padx=15)
        self.stats_description("Incorrectly").grid(row=4, column=2)

        self.stats_int(len(self.current_user.dictionaries.learned_words)).grid(row=2, column=3)
        self.short_line(progress_color="green").grid(row=3, column=3, padx=15)
        self.stats_description("Learned words").grid(row=4, column=3)

        # Words to learn
        self.stats_int(len(self.current_user.dictionaries.vocabulary.keys())).grid(row=2, column=4)
        self.short_line(progress_color="yellow").grid(row=3, column=4, padx=15)
        self.stats_description("Words to learn").grid(row=4, column=4)

        self.description("Session statistics").grid(row=5, column=2, pady=(15, 0))

        # Total session attempts
        self.stats_int(self.session_attempts_correct + self.session_attempts_incorrect).grid(row=6, column=0)
        self.short_line().grid(row=7, column=0, padx=15)
        self.stats_description("Attempts").grid(row=8, column=0)

        # Spelled correctly this session
        self.stats_int(self.session_attempts_correct).grid(row=6, column=1)
        self.short_line(progress_color="light green").grid(row=7, column=1, padx=15)
        self.stats_description("Correctly").grid(row=8, column=1)

        # Spelled incorrectly this session
        self.stats_int(self.session_attempts_incorrect).grid(row=6, column=2)
        self.short_line(progress_color="red").grid(row=7, column=2, padx=15)
        self.stats_description("Incorrectly").grid(row=8, column=2)

        self.horizontal_line().grid(row=9, column=0, columnspan=5, pady=20, padx=10)

        # Section with manual word adding
        self.description("Manually add words to learn").grid(row=10, column=2)
        word = self.user_input()
        CTkButton(self, text="Add", command=lambda: [self.add_word_to_vocabulary(word.get()),
                                                     word.delete(0, 'end')]).grid(row=11, column=2, pady=15, sticky="W")
        CTkButton(self, text="Show my vocabulary", width=250,
                  command=lambda: UserVocabularyPage(parent=self.parent, controller=self.controller,
                                                     current_user=current_user)).grid(row=12, column=0,
                                                                                      columnspan=2, padx=20)
        self.grid_rowconfigure(13, weight=1)
        CTkButton(self, text='Exit', command=self.controller.destroy).grid(row=14, column=4, pady=(0, 10))

    def avatar(self):
        avatar_img = CTkImage(Image.open(f'assets/avatars/{self.current_user.avatar}'), size=(60, 60))
        return avatar_img

    def user_name(self):
        return CTkLabel(self, text=f'{self.current_user.name}', image=self.avatar(), font=self.controller.title_font,
                        pady=10)

    def short_line(self, progress_color=None):
        progressbar = CTkProgressBar(self, width=80, progress_color=progress_color)
        progressbar.set(1)
        return progressbar

    def horizontal_line(self):
        progressbar = CTkProgressBar(self, width=config.WINDOW_WIDTH - 20)
        progressbar.set(1)
        return progressbar

    def description(self, text):
        return CTkLabel(self, text=text, font=(None, config.FONT_SIZE))

    def stats_description(self, text):
        return CTkLabel(self, text=text)

    def stats_int(self, data, text_color=None):
        return CTkLabel(self, text=f'{data}', text_color=text_color, font=(None, config.STATS_INT_SIZE))

    def user_input(self):
        user_entry = CTkEntry(self, width=250)
        user_entry.grid(row=11, column=0, columnspan=2, pady=15)
        return user_entry

    def show_personal_vocabulary(self):
        words_to_learn = list(self.current_user.misspelled_dict.keys())
        words_to_learn.sort()
        Label(self, text=f'{", ".join(words_to_learn)}', wraplength=config.WINDOW_WIDTH - 10).pack()

    def add_word_to_vocabulary(self, word):
        self.current_user.misspelled_dict.append(word)
        self.current_user.save_progress()
