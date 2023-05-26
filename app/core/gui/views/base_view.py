import tkinter as tk
import webbrowser

from PIL import Image
from customtkinter import CTkLabel, CTkImage, CTkFrame, CTkFont, CTkButton

from core import strings, config
from core.gui.elements import Button, GreyLine, HintLabel
from util import helpers


class BaseView(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.close_button = Button(self, text=strings.CLOSE, command=lambda: self.controller.destroy())
        self.horizontal_line = GreyLine(self, width=750)

    @property
    def report_bug_btn(self):
        bug = CTkImage(Image.open(helpers.get_path('assets/bug.png')), size=(13, 13))
        button = CTkButton(self, text=strings.BUG_REPORT, text_color="#abb0b6", image=bug, compound=tk.LEFT,
                           command=lambda: webbrowser.open("mailto:spellingtrainer@proton.me"))
        button.configure(width=90, height=20, font=CTkFont(None, 8), fg_color="transparent", hover_color="#212121")
        return button

    @property
    def learn_button_image(self):
        return CTkImage(Image.open(helpers.get_path('assets/learn.png')), size=(20, 20))


class BaseFrame(CTkFrame):
    def __init__(self, parent, controller, width=config.WINDOW_WIDTH - 200, border=True, **kwargs):
        CTkFrame.__init__(self, parent, width=width, **kwargs)
        if border:
            self.configure(border_color="#292929", border_width=2)
        self.parent = parent
        self.controller = controller
