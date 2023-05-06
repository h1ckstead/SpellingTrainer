from tkinter import *
from tkinter import StringVar

from PIL import Image
from PyDictionary import PyDictionary
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkImage, CTkEntry

from app import config
from app.core.spell_checker import SpellChecker
from app.core.user_page_view import UserPage
from app.core.word_generator import WordGenerator
from app.util import speech


# noinspection PyTypeChecker
class PracticePage(CTkFrame):
    #  TODO: Count session attempts
    def __init__(self, parent, controller, current_user):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.current_user = current_user
        self.session_attempts_correct = 0
        self.session_attempts_incorrect = 0
        self.word_generator = WordGenerator(current_user)
        self.spell_checker = SpellChecker(current_user)
        self.word_dict = self.word_generator.generate_word()
        self.grid(row=0, column=0, sticky="nsew")

        #  Header
        self.back_to_menu_btn().grid(row=0, column=0, padx=20)
        self.header().grid(row=0, column=1, columnspan=2, pady=10)

        # Main area
        self.grid_rowconfigure(1, weight=1)
        self.play_word_btn().grid(row=2, column=0)
        self.show_def_btn().grid(row=2, column=1)
        entry = CTkEntry(self, width=250)
        entry.grid(row=3, column=0, columnspan=2, pady=15)
        entry.focus_set()
        entry.bind('<Return>', lambda event: [self.show_validation_label(self.spell_checker.spell_check(self.word_dict,
                                                                                                  entry.get()),
                                                                         self.word_dict),
                                              entry.delete(0, 'end'),
                                              self.new_word(),
                                              self.after(1000, lambda: self.read_aloud(self.word_dict))])
        CTkButton(self, text='Check',
                  command=lambda: [self.show_validation_label(self.spell_checker.spell_check(self.word_dict,
                                                                                       entry.get()),
                                                              self.word_dict),
                                   entry.delete(0, 'end'),
                                   self.new_word(),
                                   self.after(1000, lambda: self.read_aloud(self.word_dict))]).grid(row=3, column=3)
        self.grid_rowconfigure(4, weight=1)
        self.finish_btn().grid(row=5, column=4, padx=10, pady=(0, 10))

    def header(self):
        return CTkLabel(self, text="Spelling Trainer - Practice!", font=self.controller.title_font)

    def play_word_btn(self):
        speaker_img = CTkImage(Image.open('assets/speaker.png'))
        return CTkButton(self, text='', image=speaker_img, width=35, height=35,
                         command=lambda: self.read_aloud(self.word_dict))

    def show_def_btn(self):
        return CTkButton(self, text='Show definition', height=35, command=lambda: self.show_definition(self.word_dict))

    def finish_btn(self):
        return CTkButton(self, text='Finish',
                         command=lambda: [self.current_user.save_progress(),
                                          UserPage(parent=self.parent,
                                                   controller=self.controller,
                                                   current_user=self.current_user,
                                                   session_attempts_correct=self.session_attempts_correct,
                                                   session_attempts_incorrect=self.session_attempts_incorrect).tkraise()
                                          ])

    def back_to_menu_btn(self):
        from app.core.main_page_view import MainPage
        return CTkButton(self, text='Back to Main Menu',
                         command=lambda: [self.current_user.save_progress(),
                                          MainPage(parent=self.parent,
                                                   controller=self.controller,
                                                   saved_data=self.current_user.load_save())])

    def new_word(self):
        self.word_dict = self.word_generator.generate_word()

    def update_and_show_spelling_text(self, clear=False):
        spelling = StringVar()
        if clear:
            spelling.set('')
        else:
            spelling.set(value=f'{self.word_dict[list(self.word_dict.keys())[0]]["spelling"]}')
        Label(self, textvariable=spelling, width=20, height=5).grid(row=1, column=1, columnspan=2)

    def read_aloud(self, word_dict):
        if 'spelling' in word_dict[list(self.word_dict.keys())[0]].keys():
            self.update_and_show_spelling_text()
        else:
            self.update_and_show_spelling_text(clear=True)
        speech.read_aloud(word_dict)

    @staticmethod
    def get_definition(word):
        dictionary = PyDictionary()
        return dictionary.meaning(word)

    def show_definition(self, word_dict):
        word = list(word_dict)[0]
        definition = word_dict[word]["definition"]
        CTkLabel(self, text=definition, wraplength=config.WINDOW_WIDTH - 20).grid(row=4, column=0, columnspan=2)

    def show_validation_label(self, status, word_dict):
        if status == 'correct':
            self.session_attempts_correct += 1
            validation_msg = CTkLabel(self, text='Correct!')
        elif status == 'incorrect':
            self.session_attempts_incorrect += 1
            validation_msg = CTkLabel(self, text=f"Incorrect! It's {list(word_dict)[0]}")
        else:
            validation_msg = CTkLabel(self, text='Enter a word!')
        validation_msg.grid(row=1, column=1, columnspan=2)
        validation_msg.after(2000, lambda: validation_msg.destroy())
