from tkinter import ttk, Frame, Label, Button
from app.core.practice_page_view import PracticePage
from app import config


class ChooseDifferentUserPage(Frame):
    def __init__(self, parent, controller, saved_data):
        Frame.__init__(self, parent)
        self.controller = controller
        self.saved_data = saved_data
        self.grid(row=0, column=0, sticky="nsew")

        Label(self, text=config.CHANGE_USER).pack(side="top", fill="x", pady=10)
        users = [k for k in saved_data.keys() if k != 'last_user']
        dropdown = ttk.Combobox(self, state="readonly", values=users)
        dropdown.pack()
        Button(text='Continue',
               command=lambda: PracticePage(parent=parent,
                                            controller=self.controller,
                                            current_user=saved_data[dropdown.get()]).tkraise()).pack()
