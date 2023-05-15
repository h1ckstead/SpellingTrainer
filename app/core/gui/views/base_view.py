import webbrowser

from PIL import Image
from customtkinter import CTkLabel, CTkImage, CTkFrame, CTkFont, CTkButton

from core import strings, config
from core.gui.elements import Button, GreyLine


class BaseView(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")

        self.close_button = Button(self, text=strings.CLOSE, command=lambda: self.controller.destroy())
        self.pencil_icon = CTkLabel(self, text="", image=CTkImage(Image.open("assets/pencil.png"), size=(20, 20)))
        self.horizontal_line = GreyLine(self, width=600)

    @property
    def report_bug_btn(self):
        bug = CTkImage(Image.open('assets/bug-solid.png'), size=(10, 10))
        button = CTkButton(self, text=strings.BUG_REPORT, image=bug, compound="left",
                           command=lambda: webbrowser.open("mailto:lazarevavictoria@gmail.com"))
        button.configure(width=90, height=20, font=CTkFont(None, 8), fg_color="transparent", hover_color="#212121")
        return button


class BaseFrame(CTkFrame):
    def __init__(self, parent, controller, width=config.WINDOW_WIDTH - 200, border=True, **kwargs):
        CTkFrame.__init__(self, parent, width=width, **kwargs)
        if border:
            self.configure(border_color="#292929", border_width=2)
        self.parent = parent
        self.controller = controller