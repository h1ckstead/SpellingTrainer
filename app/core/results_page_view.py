from tkinter import *
from app import config
from app.core.user_page_view import UserPage


class ResultsPage(Frame):
    def __init__(self, parent, controller, current_user, session_attempts, session_misspelled_lst):
        Frame.__init__(self, parent)
        self.controller = controller
        self.current_user = current_user
        self.grid(row=0, column=0, sticky="nsew")

        Label(self, text='These are your results: ').pack(side="top", fill="x", pady=10)
        Label(self, text=f'Correctly spelled words: {session_attempts - len(session_misspelled_lst)}').pack()
        Label(self, text=f'Incorrectly spelled words: {len(session_misspelled_lst)}').pack()
        Label(self, text=f'Misspelled words: {session_misspelled_lst}', wraplength=config.WINDOW_WIDTH - 20).pack()
        Button(self, text='See complete stats', command=lambda: UserPage(parent=parent,
                                                                         controller=self.controller,
                                                                         current_user=self.current_user,
                                                                         session_attempts=session_attempts,
                                                                         session_misspelled_lst=session_misspelled_lst
                                                                         ).tkraise())
        Button(self, text='Exit', command=self.controller.destroy).pack()
