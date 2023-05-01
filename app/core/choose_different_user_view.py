from customtkinter import CTkFrame, CTkLabel, CTkComboBox, CTkButton

from app import config
from app.core import spelling_trainer
from app.core.practice_page_view import PracticePage


class ChooseDifferentUserPage(CTkFrame):
    def __init__(self, parent, controller, saved_data):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.saved_data = saved_data
        self.grid(row=0, column=0, sticky="nsew")

        self.header().pack(side="top", fill="x", pady=10)
        users = [k for k in saved_data.keys() if k != 'last_user']
        dropdown = CTkComboBox(self, state="readonly", values=users)
        dropdown.pack(pady=20)
        CTkButton(self, text='Continue',
                  command=lambda: PracticePage(parent=parent,
                                               controller=self.controller,
                                               current_user=saved_data[dropdown.get()]).tkraise()).pack()
        self.back_btn().pack(pady=10)
        self.exit_btn().pack(side="bottom", anchor="e", padx=10, pady=(0, 10))

    def header(self):
        return CTkLabel(self, text=config.CHANGE_USER, font=self.controller.title_font)

    def back_btn(self):
        return CTkButton(self, text='Back',
                         command=lambda: spelling_trainer.MainPage(parent=self.parent,
                                                                   controller=self.controller,
                                                                   saved_data=self.saved_data).tkraise())

    def exit_btn(self):
        return CTkButton(self, text='Exit', width=160, height=35, command=self.controller.destroy)
