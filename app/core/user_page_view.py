import tkinter
from tkinter import *
from app import config
from PIL import ImageTk, Image


class UserPage(Frame):
    def __init__(self, parent, controller, current_user, session_attempts, session_misspelled_lst):
        Frame.__init__(self, parent)
        self.controller = controller
        self.current_user = current_user
        self.grid(row=0, column=0, sticky="nsew")

        Label(self, text=f'{self.current_user.name}', font=controller.title_font, pady=10).pack()
        im = Image.open(f'assets/avatars/{self.current_user.avatar}')
        avatar_img = ImageTk.PhotoImage(im)
        img_label = Label(self, image=avatar_img)
        img_label.pack()
        img_label.image = avatar_img
        Label(self, text=f'All time words practiced: '
                         f'{self.current_user.attempts_correct + self.current_user.attempts_incorrect}').pack()
        Label(self, text=f'Words spelled correctly: {self.current_user.attempts_correct}').pack()
        Label(self, text=f'Words spelled incorrectly: {self.current_user.attempts_incorrect}').pack()
        Label(self, text=f'Learned words: {len(self.current_user.spelled_ok_lst)}').pack()
        Label(self, text=f'Words to learn: {len(self.current_user.misspelled_dict.keys())}').pack()
        Button(self, text='Show words to learn', command=lambda: self.show_personal_vocabulary(), padx=10).pack()
        Label(self, text='Add word to personal vocabulary').pack()
        word = Entry(self)
        word.pack()
        word.focus()
        Button(self, text='Add', command=lambda: [self.add_word_to_vocabulary(word.get()),
                                                  word.delete(0, 'end')]).pack()
        Button(self, text='Exit', command=self.controller.destroy).pack()

    def show_personal_vocabulary(self):
        words_to_learn = list(self.current_user.misspelled_dict.keys())
        words_to_learn.sort()
        Label(self, text=f'{", ".join(words_to_learn)}', wraplength=config.WINDOW_WIDTH - 10).pack()

    def add_word_to_vocabulary(self, word):
        self.current_user.misspelled_dict.append(word)
        self.current_user.save_progress()
