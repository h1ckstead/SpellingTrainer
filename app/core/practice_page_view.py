from tkinter import *

from app.util.spell_check import spell_check
from app.util import speech, word_generation
from PyDictionary import PyDictionary
from app.core.user_page_view import UserPage


class PracticePage(Frame):
    #  TODO: Count session attempts
    def __init__(self, parent, controller, current_user):
        Frame.__init__(self, parent)
        self.controller = controller
        self.current_user = current_user
        self.session_attempts = 0
        self.session_misspelled_lst = []
        self.word = word_generation.next_word(self.current_user)
        self.grid(row=0, column=0, sticky="nsew")

        Label(self, text="Spelling Trainer - Practice!").pack(side="top", fill="x", pady=10)
        Button(self, text='Listen to word', command=lambda: speech.read_aloud(self.word)).pack()
        Button(self, text='Show definition', command=lambda: self.show_definition(self.word)).pack()
        entry = Entry(self)
        entry.pack()
        entry.focus_set()
        entry.bind('<Return>', lambda event: [self.show_validation_label(spell_check(self.current_user,
                                                                                     self.word,
                                                                                     entry.get()), self.word),
                                              entry.delete(0, 'end'),
                                              self.new_word(self.current_user),
                                              self.after(1000, lambda: speech.read_aloud(self.word))])
        Button(self, text='Check',
               command=lambda: [spell_check(self.current_user, self.word, entry.get()),
                                entry.delete(0, 'end'),
                                self.new_word(self.current_user),
                                self.after(1000, lambda: speech.read_aloud(self.word))]).pack()
        Button(self, text='Finish',
               command=lambda: [self.current_user.save_progress(),
                                UserPage(parent=parent,
                                         controller=self.controller,
                                         current_user=self.current_user,
                                         session_attempts=self.session_attempts,
                                         session_misspelled_lst=self.session_misspelled_lst).tkraise()]).pack()

    def new_word(self, current_user):
        self.word = word_generation.next_word(current_user)

    @staticmethod
    def get_definition(word):
        dictionary = PyDictionary()
        return dictionary.meaning(word)

    def show_definition(self, word):
        definition = self.get_definition(word)
        Label(self, text=definition).pack()

    def show_validation_label(self, status, word):
        if status == 'correct':
            validation_msg = Label(self, text='Correct!')
        elif status == 'incorrect':
            validation_msg = Label(self, text=f"Incorrect! It's {word.title()}")
        else:
            validation_msg = Label(self, text='Enter a word!')
        validation_msg.pack()
        validation_msg.after(2000, lambda: validation_msg.destroy())
