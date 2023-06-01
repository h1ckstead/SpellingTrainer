import logging
import tkinter as tk
from tkinter import Canvas, Label, StringVar

from PIL import Image, ImageTk
from customtkinter import CTkLabel, CTkFont

from core import strings, config
from core.gui.elements import EntryField, StrictSpellingSwitch, HintLabel
from core.gui.views.base_view import BaseFrame
from util import helpers


class RegistrationEditBlock(BaseFrame):
    def __init__(self, parent, controller, current_user=None):
        BaseFrame.__init__(self, parent, controller, width=config.WINDOW_WIDTH - 200)
        self.controller = controller
        self.parent = parent
        self.current_user = current_user
        self.canvas = Canvas(self, width=243, height=243, bg="#2b2b2b", highlightthickness=0)
        self.selected_image_circle = None
        self.selected_avatar = None

        if self.current_user:
            self.title_text = strings.EDIT_PROFILE_TITLE
            self.username = self.current_user.name
            self.selected_avatar = self.current_user.avatar
        else:
            self.title_text = strings.REGISTRATION_TITLE
            self.username = None
            self.strict_spelling_switch = StrictSpellingSwitch(self)
            self.strict_spelling_hint = HintLabel(self, text=strings.STRICT_SPELLING_HINT, wraplength=250)

        self.title = Label(self, text=self.title_text, font=self.controller.title_font, background="#2b2b2b",
                           foreground="#FFFFFF")
        self.username_field_title = CTkLabel(self, text=strings.USERNAME_FIELD_TITLE,
                                             font=CTkFont(family="Arial", size=config.HEADER_FONT_SIZE))
        self.entry_var = StringVar()
        self.username_field = EntryField(self, text=self.username, validate=True, textvariable=self.entry_var)
        self.entry_var.trace_add('write', self.on_entry_change)
        self.avatars_title = CTkLabel(self, text=strings.AVATARS_TITLE,
                                      font=CTkFont(family="Arial", size=config.HEADER_FONT_SIZE))
        self.load_avatars_to_canvas()

        self.display_widgets()

    def on_entry_change(self, *args):
        stripped_text = self.entry_var.get().strip()
        if stripped_text:
            self.parent.save_btn.configure(state=tk.NORMAL, fg_color="#246ba3")
        else:
            self.parent.save_btn.configure(state=tk.DISABLED, fg_color="#565b5e")

    def display_widgets(self):
        self.title.grid(row=0, column=0, pady=(10, 0), ipady=2)
        self.username_field_title.grid(row=1, column=0, padx=(40, 0), sticky=tk.W)
        self.username_field.grid(row=2, column=0, pady=(0, 15))
        self.avatars_title.grid(row=3, column=0, padx=(40, 0), sticky=tk.W)
        self.canvas.grid(row=4, column=0, padx=40, pady=(0, 15))
        if not self.username:
            self.strict_spelling_switch.grid(row=5, column=0, padx=(40, 0), sticky=tk.W)
            self.strict_spelling_hint.grid(row=6, column=0, padx=(32, 0), pady=(0, 15), sticky=tk.W)

    def get_username(self):
        return self.username_field.get()

    def get_strict_spelling_value(self):
        return self.strict_spelling_switch.get()

    @property
    def avatars(self):
        if not hasattr(self, '_avatars'):
            self._avatars = self._create_avatars()
        return self._avatars

    @staticmethod
    def _create_avatars():
        avatars_dict = {}
        for avatar_name in helpers.get_avatars_list():
            image = Image.open(helpers.get_path(f'assets/avatars/{avatar_name}'))
            image = image.resize((55, 55), Image.ANTIALIAS)
            photo_image = ImageTk.PhotoImage(image)
            avatars_dict[avatar_name] = {'img_object': photo_image}
        return avatars_dict

    def load_avatars_to_canvas(self):
        coordinates = [{'x': 3, 'y': 3}, {'x': 63, 'y': 3}, {'x': 123, 'y': 3}, {'x': 183, 'y': 3},
                       {'x': 3, 'y': 63}, {'x': 63, 'y': 63}, {'x': 123, 'y': 63}, {'x': 183, 'y': 63},
                       {'x': 3, 'y': 123}, {'x': 63, 'y': 123}, {'x': 123, 'y': 123}, {'x': 183, 'y': 123},
                       {'x': 3, 'y': 183}, {'x': 63, 'y': 183}, {'x': 123, 'y': 183}, {'x': 183, 'y': 183}]
        for i, avatar_name in enumerate(self.avatars):
            place = coordinates[i]
            self.canvas.create_image((place['x'], place['y']), anchor=tk.NW,
                                     image=self.avatars[avatar_name]['img_object'],
                                     tags=avatar_name)
            self.avatars[avatar_name].update({'position': place})
            self.canvas.tag_bind(avatar_name, "<Button-1>",
                                 lambda event, image_name=avatar_name: self.select_avatar(image_name))
        if self.selected_avatar:
            self.select_avatar(self.current_user.avatar)

    def select_avatar(self, image_name):
        logging.debug(f"Avatar clicked: {image_name}")
        if self.selected_image_circle is not None:
            self.canvas.delete(self.selected_image_circle)
            self.selected_avatar = None
        position_x = self.avatars[image_name]['position']['x']
        position_y = self.avatars[image_name]['position']['y']
        self.selected_image_circle = self.canvas.create_oval(position_x, position_y, position_x + 54, position_y + 54,
                                                             width=3, outline='white')
        self.selected_avatar = image_name
