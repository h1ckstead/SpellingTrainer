import tkinter as tk
from tkinter import Label
from typing import Callable, Union

from PIL import ImageTk, Image
from customtkinter import CTkButton, CTkEntry, CTkSwitch, CTkLabel, CTkFont, CTkProgressBar, CTkImage
from tktooltip import ToolTip

from core import strings, config
from util import helpers


class Button(CTkButton):
    def __init__(self, parent, text, command=None, image=None, width=140, height=35, **kwargs):
        super().__init__(parent, text=text, command=command, image=image, width=width, height=height, **kwargs)
        self.configure(border_width=1, border_color="white", fg_color="transparent", hover_color="#212121")
        # self.hover_bg_color = "#d3d3d3"
        # self.bind("<Enter>", self.on_enter)
        # self.bind("<Leave>", self.on_leave)

    # def on_enter(self, event):
    #     self.config(bg=self.hover_bg_color)
    #
    # def on_leave(self, event):
    #     self.config(bg=self["bg"])


class CTAButton(CTkButton):
    def __init__(self, parent, text, width=160, height=35, command=None, state="normal", **kwargs):
        super().__init__(parent, text=text, width=width, height=height, command=command, **kwargs)
        if state == "disabled":
            self.configure(fg_color="#565b5e", state=tk.DISABLED)


class PlayButton(CTkLabel):
    def __init__(self, parent, **kwargs):
        CTkLabel.__init__(self, parent, **kwargs)
        self.normal = CTkImage(Image.open(helpers.get_path("assets", "play.png")), size=(40, 40))
        self.hovered = CTkImage(Image.open(helpers.get_path("assets", "play-dark.png")), size=(40, 40))

        self.configure(image=self.normal, text="")
        self.bind("<Enter>", self.on_enter)  # Bind hover enter event
        self.bind("<Leave>", self.on_leave)  # Bind hover leave event

    def on_enter(self, event):
        self.configure(image=self.hovered)

    def on_leave(self, event):
        self.configure(image=self.normal)


class EntryField(CTkEntry):
    def __init__(self, parent, text=None, placeholder_text=None, width=250, validate=False, max_chars=20, **kwargs):
        super().__init__(parent, placeholder_text=placeholder_text, width=width, **kwargs)
        if text:
            self.insert(0, text)
        if not placeholder_text:
            self.focus_set()
        if validate:
            self.configure(validate="key", validatecommand=(self.register(lambda s: len(s) <= max_chars), '%P'))


class StrictSpellingSwitch(CTkSwitch):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text=strings.STRICT_SPELLING, onvalue=True, offvalue=False, **kwargs)
        self.configure(font=CTkFont(family="Arial", underline=True))


class HintLabel(Label):
    def __init__(self, parent, text, wraplength=200, image=True, **kwargs):
        super().__init__(parent, text=text, fg="grey", bg="#2b2b2b",
                         font=CTkFont(family="Arial", size=config.HINT_FONT_SIZE),
                         wraplength=wraplength, justify="left", **kwargs)
        if image:
            original_image = Image.open(helpers.get_path('assets/info.png'))
            resized_image = original_image.resize((5, 10), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(resized_image)
            self.image = image  # Keep the reference from Python's garbage collector
            self.config(image=self.image, compound="left", padx=6)


class StrictSpellingHint(CTkLabel):
    def __init__(self, parent, wraplength=200):
        super().__init__(parent, text=strings.STRICT_SPELLING_HINT,
                         font=CTkFont(family=None, size=config.HINT_FONT_SIZE),
                         wraplength=wraplength, justify="left", pady=10)


class GreyLine(CTkProgressBar):
    def __init__(self, parent, width, height=2, progress_color="#aab0b5", **kwargs):
        CTkProgressBar.__init__(self, parent, **kwargs)
        self.configure(width=width, height=height, progress_color=progress_color)
        self.set(1)


class StaticsLabel(CTkLabel):
    def __init__(self, parent, text, text_color=None):
        super().__init__(parent, text=text, text_color=text_color,
                         font=CTkFont(family=None, size=config.STATISTICS_FONT_SIZE,
                                      weight="bold"))  # TODO: Experiment with size


class ThickLine(CTkProgressBar):
    def __init__(self, parent, width=80, height=7, progress_color=None, **kwargs):
        CTkProgressBar.__init__(self, parent, **kwargs)
        self.configure(width=width, height=height, progress_color=progress_color)
        self.set(1)


class CustomToolTip(ToolTip):
    def __init__(self, widget, text, ):
        super().__init__(widget=widget, msg=text, delay=0.7, parent_kwargs={"bg": "white", "padx": 1, "pady": 1},
                         bg="yellow", fg="red")
