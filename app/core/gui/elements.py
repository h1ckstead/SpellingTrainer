from PIL import ImageTk, Image
from customtkinter import CTkButton, CTkEntry, CTkSwitch, CTkLabel, CTkFont, CTkImage, CTkProgressBar
from core import strings, config
from tkinter import Label
import tkinter as tk
from tktooltip import ToolTip

import time
import tkinter as tk
from typing import Callable, Union


class Button(CTkButton):
    def __init__(self, parent, text, command=None, image=None, width=140, height=35, **kwargs):
        super().__init__(parent, text=text, command=command, image=image, width=width, height=height, **kwargs)
        self.configure(border_width=1, border_color="white", fg_color="transparent", hover_color="#212121")
        # self.hover_bg_color = "#d3d3d3"
        # self.bind("<Enter>", self.on_enter)
        #self.bind("<Leave>", self.on_leave)

    # def on_enter(self, event):
    #     self.config(bg=self.hover_bg_color)
    #
    # def on_leave(self, event):
    #     self.config(bg=self["bg"])


class CTAButton(CTkButton):
    def __init__(self, parent, text, width=160, height=35, command=None, state="normal", **kwargs):
        super().__init__(parent, text=text, width=width, height=height, command=command, **kwargs)
        if state == "disabled":
            self.configure(fg_color="#565b5e", state="disabled")


# class BackButton(CTkButton):
#     def __init__(self, parent, text, previous_page):
#         super().__init__(parent, text=text, command=lambda: previous_page.tkraise())
#         self.configure(width=160, height=35)


class EntryField(CTkEntry):
    def __init__(self, parent, text=None, placeholder_text=None, width=250, validate=False, **kwargs):
        super().__init__(parent, placeholder_text=placeholder_text, width=width, **kwargs)
        if text:
            self.insert(0, text)
        if not placeholder_text:
            self.focus_set()
        if validate:
            self.configure(validate="key", validatecommand=(self.register(lambda s: len(s) <= 20), '%P'))


class StrictSpellingSwitch(CTkSwitch):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text=strings.STRICT_SPELLING, onvalue="True", offvalue="False", **kwargs)
        self.configure(font=CTkFont(family="Arial", underline=True))


class HintLabel(Label):
    def __init__(self, parent, text, wraplength=200, image=True, **kwargs):
        super().__init__(parent, text=text, fg="grey", bg="#2b2b2b",
                         font=CTkFont(family="Arial", size=config.HINT_FONT_SIZE),
                         wraplength=wraplength, justify="left", **kwargs)
        if image:
            original_image = Image.open("assets/info.png")
            resized_image = original_image.resize((10, 10), Image.ANTIALIAS)
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
                         font=CTkFont(family=None, size=config.STATISTICS_FONT_SIZE, weight="bold"))  # TODO: Experiment with size


class ThickLine(CTkProgressBar):
    def __init__(self, parent, width=80, height=7, progress_color=None, **kwargs):
        CTkProgressBar.__init__(self, parent, **kwargs)
        self.configure(width=width, height=height, progress_color=progress_color)
        self.set(1)


class CustomToolTip(ToolTip):
    def __init__(
        self,
        widget: tk.Widget,
        msg: Union[str, Callable] = None,
        delay: float = 0.0,
        follow: bool = True,
        refresh: float = 1.0,
        x_offset: int = +10,
        y_offset: int = +10,
        parent_kwargs: dict = {"bg": "black", "padx": 1, "pady": 1},
        bordercolor: str = "black",
        **message_kwargs,
    ):
        # Call the super constructor to initialize the ToolTip
        super().__init__(
            widget,
            msg,
            delay,
            follow,
            refresh,
            x_offset,
            y_offset,
            parent_kwargs,
            **message_kwargs,
        )
        # Add the bordercolor attribute to the CustomToolTip class
        self.bordercolor = bordercolor

    def _show(self):
        super()._show()  # Call the super method to display the ToolTip

        # Modify the border color
        self.configure(background="white")
        if isinstance(self.msg, tk.StringVar):
            self.msg.set(self.msg.get())
            self.msg.config(highlightbackground=self.bordercolor, highlightthickness=1)

