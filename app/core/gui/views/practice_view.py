import logging
import tkinter as tk
from tkinter import Text, Label, BooleanVar

from PIL import Image
from PIL.ImageTk import PhotoImage
from customtkinter import CTkFrame, CTkLabel, CTkImage, CTkSlider, CTkFont, CTkScrollbar, CTkToplevel, CTkSwitch

from core import config, strings, constants
from core.gui.elements import Button, CTAButton, HintLabel, EntryField, GreyLine, CustomToolTip, PlayButton
from core.gui.views.base_view import BaseView, BaseFrame
from core.gui.views.profile_view import ProfilePage
from core.spell_checker import SpellChecker
from core.word_generator import WordGenerator
from util import helpers
from util import speech


class PracticePage(BaseView):
    def __init__(self, parent, controller, current_user, previous_page, session):
        super().__init__(parent, controller)
        self.parent = parent
        self.controller = controller
        self.current_user = current_user
        self.previous_page = previous_page  # Main Page
        self.session = session
        self.avatar = self.load_avatar()

        # Create widgets and content blocks
        self.title_text = Label(self, text=strings.PRACTICE_PAGE_TITLE, font=self.controller.title_font,
                                background="#333333", foreground="#FFFFFF",
                                image=self.avatar, compound=tk.LEFT, padx=10)
        self.spelling_trainer_block = SpellingTrainerBlock(self, self.controller, self.current_user, self.session)
        self.session_history_block = SessionHistoryBlock(self, self.controller)
        self.definition_block = DefinitionBlock(self, self.controller)
        self.back_to_main_btn = Button(self, text=strings.BACK_TO_MAIN_BTN_TEXT,
                                       command=lambda: self.previous_page.tkraise())
        self.finish_button = CTAButton(self, text=strings.FINISH,
                                       command=lambda: ProfilePage(parent=self.parent, controller=self.controller,
                                                                   current_user=self.current_user,
                                                                   main_page=self.previous_page,
                                                                   previous_page=self,
                                                                   session=self.session).tkraise())

        # Display widgets and content blocks on the page
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.title_text.grid(row=0, column=0, columnspan=6, pady=(10, 15))
        self.spelling_trainer_block.grid(row=1, column=1, columnspan=2, sticky=tk.NW)
        self.definition_block.grid(row=1, column=3, columnspan=2, sticky=tk.NE)
        self.session_history_block.grid(row=2, column=2, columnspan=2, pady=(10, 20), sticky=tk.NSEW)
        self.back_to_main_btn.grid(row=4, column=1, columnspan=2, sticky=tk.W)
        self.close_button.grid(row=4, column=2, sticky=tk.E)
        self.finish_button.grid(row=4, column=3, sticky=tk.E)
        self.report_bug_btn.grid(row=6, column=0, columnspan=6, pady=(0, 5))

        # Create event listeners
        self.spelling_trainer_block.add_input_change_listener(self.session_history_block.update_user_input)
        self.spelling_trainer_block.add_new_word_listener(self.definition_block.update_definition)
        self.spelling_trainer_block.add_input_change_listener(self.definition_block.hide_definition)

    def load_avatar(self):
        image = Image.open(helpers.get_path(f"assets/avatars/{self.current_user.avatar}"))
        image = image.resize((60, 60), Image.ANTIALIAS)
        return PhotoImage(image)

    def change_current_user(self, new_user):
        # Needed for change user feature
        self.current_user = new_user
        self.spelling_trainer_block.update_user(new_user)
        self.avatar = self.load_avatar()
        self.title_text.configure(image=self.avatar)


class SpellingTrainerBlock(BaseFrame):
    def __init__(self, parent, controller, current_user, session):
        BaseFrame.__init__(self, parent, controller, width=config.WINDOW_WIDTH - 430)
        self.parent = parent
        self.controller = controller
        self.current_user = current_user
        self.grid_propagate(False)
        self.word_generator = WordGenerator(current_user, self.handle_empty_vocabulary)
        self.spell_checker = SpellChecker(current_user)
        self.session = session
        self.dialog = None

        # Attributes for event listeners
        self.word_dict = None
        self.generated_data = None
        self.user_input = None
        self.input_change_listeners = []
        self.new_word_listeners = []

        # Create widgets and content blocks
        self.play_word_btn = self.create_play_sound_btn()
        self.volume_slider = self.create_volume_slider()
        self.spelling_hint = self.create_spelling_hint()
        self.spellcheck_hint = HintLabel(self, text=strings.SPELLCHECK_HINT, wraplength=250)
        self.word_entry = self.create_word_entry_field()
        self.spellcheck_btn = CTAButton(self, text=strings.CHECK, width=125, state=tk.DISABLED,
                                        command=self.handle_enter)

        # Display widgets and content blocks on the page
        self.play_word_btn.grid(row=0, column=0, padx=20, pady=(10, 0), sticky=tk.W)
        self.volume_slider.grid(row=0, column=1, columnspan=3, padx=(0, 40), sticky=tk.W)
        self.grid_rowconfigure(1, minsize=29)  # placeholder for Br/Am spelling hint
        self.word_entry.grid(row=2, column=0, columnspan=3, padx=20, sticky=tk.W)
        self.spellcheck_hint.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)
        self.spellcheck_btn.grid(row=4, column=0, columnspan=2, padx=20, pady=15, sticky=tk.W)

    def update_user(self, new_user):
        self.current_user = new_user
        self.word_generator = WordGenerator(new_user, self.handle_empty_vocabulary)
        self.spell_checker = SpellChecker(new_user)

    def create_spelling_hint(self):
        attention_img = CTkImage(Image.open(helpers.get_path('assets/attention.png')), size=(15, 15))
        return CTkLabel(self, text="", text_color="#f8c543", image=attention_img, compound=tk.LEFT,
                        padx=5, font=CTkFont(family="Arial", size=13, underline=True))

    def create_play_sound_btn(self):
        button = PlayButton(self)
        if self.current_user.only_from_vocabulary and len(self.current_user.dictionaries.vocabulary) == 0:
            self.is_play_btn_on = False
            button.bind("<Button-1>", lambda event: self.show_empty_vocab_message())
        else:
            self.is_play_btn_on = True
            button.bind("<Button-1>", lambda event: self.say_word())
        return button

    def create_volume_slider(self):
        volume_slider = CTkSlider(self)
        volume_slider.set(self.current_user.volume)
        volume_slider.bind("<ButtonRelease-1>", command=lambda event: self.change_volume())
        return volume_slider

    def create_word_entry_field(self):
        entry_field = EntryField(self, placeholder_text=strings.ENTRY_FIELD_PLACEHOLDER_TEXT, font=CTkFont("Arial", 18),
                                 validate=True, max_chars=50)
        entry_field.bind('<Return>', lambda event: self.handle_enter(event))
        entry_field.bind("<KeyRelease>", lambda event: self.on_entry_change())
        return entry_field

    def handle_enter(self, event=None):
        user_input = self.word_entry.get().strip()
        if user_input:
            self.perform_spellcheck()
            self.word_entry.delete(0, 'end')
            if self.current_user.only_from_vocabulary and len(self.current_user.dictionaries.vocabulary) == 0:
                self.show_empty_vocab_message()
            else:
                self.new_word()
                self.after(1000, self.say_word)

    def on_entry_change(self):
        stripped_text = self.word_entry.get().strip()
        if stripped_text:
            self.spellcheck_btn.configure(state=tk.NORMAL, fg_color="#246ba3")
        else:
            self.spellcheck_btn.configure(state=tk.DISABLED, fg_color="#565b5e")

    def add_input_change_listener(self, listener):
        self.input_change_listeners.append(listener)

    def add_new_word_listener(self, listener):
        self.new_word_listeners.append(listener)

    def on_input_change(self, word_dict, user_word, status):
        for listener in self.input_change_listeners:
            listener(word_dict, user_word, status)

    def on_new_word(self, word_dict):
        for listener in self.new_word_listeners:
            listener(word_dict)

    def perform_spellcheck(self):
        if not self.word_dict:
            self.show_validation_label("no_word_dict")
        else:
            status = self.spell_checker.spell_check(self.word_dict, self.word_entry.get().strip(), self.session)
            self.update_session_stats(status)
            self.show_validation_label(status)
            self.on_input_change(self.word_dict, self.word_entry.get(), status)

    def update_session_stats(self, status):
        if status == constants.CORRECT:
            self.session.increment_attempts_correct()
        elif status == constants.INCORRECT:
            self.session.increment_attempts_incorrect()
        else:
            logging.debug(
                f"Unable to update session stats. Unknown status: {status}. Expected 'Correct' or 'Incorrect'")

    def show_validation_label(self, status):
        if status == constants.CORRECT:
            validation_msg = self.show_green_message()
        elif status == constants.INCORRECT:
            validation_msg = self.show_red_message()
        elif status == constants.NO_WORD_DICT:
            validation_msg = self.show_empty_word_string_message()
        else:
            validation_msg = CTkLabel(self, text=strings.UNKNOWN)
        validation_msg.grid(row=4, column=2, padx=(0, 5), sticky=tk.W)
        validation_msg.after(2000, lambda: validation_msg.destroy())

    def show_empty_word_string_message(self):
        validation_container = CTkFrame(self)
        validation_msg = CTkLabel(validation_container, text=strings.EMPTY, text_color="#dce4ee")
        validation_msg.pack(padx=4, pady=4)
        return validation_container

    def show_green_message(self):
        validation_container = CTkFrame(self)
        validation_msg = CTkLabel(validation_container, text=strings.CORRECT, text_color=config.GREEN,
                                  font=CTkFont(weight="bold"), compound=tk.LEFT, padx=6,
                                  image=CTkImage(Image.open(helpers.get_path('assets/correct.png')), size=(15, 15)))
        validation_msg.pack(padx=4, pady=4)
        return validation_container

    def show_red_message(self):
        validation_container = CTkFrame(self)
        validation_msg = CTkLabel(validation_container, text=strings.INCORRECT, text_color=config.RED,
                                  font=CTkFont(weight="bold"),
                                  image=CTkImage(Image.open(helpers.get_path('assets/incorrect.png')),
                                                 size=(15, 15)), compound=tk.LEFT, padx=6)
        validation_msg.pack(padx=4, pady=4)
        return validation_container

    def change_volume(self):
        volume = self.volume_slider.get()
        self.current_user.set_volume(volume)

    def say_word(self, event=None):
        if self.word_dict is None:  # case when user just opened the page
            self.new_word()
        word = list(self.word_dict)[0]
        speech.say(word, self.volume_slider.get())

    def new_word(self):
        self.spelling_hint.grid_forget()
        self.word_dict = self.word_generator.generate_word()
        word = list(self.word_dict)[0]
        if constants.SPELLING in self.word_dict[word]:
            if self.word_dict[word][constants.SPELLING] == constants.AmE:
                self.spelling_hint.configure(text=strings.AMERICAN_SPELLING)
            elif self.word_dict[word][constants.SPELLING] == constants.BrE:
                self.spelling_hint.configure(text=strings.BRITISH_SPELLING)
            self.spelling_hint.grid(row=1, column=0, columnspan=2, padx=(10, 0), sticky=tk.W)
        self.on_new_word(self.word_dict)

    def handle_empty_vocabulary(self):
        self.show_empty_vocab_message()
        self.turn_off_play_btn()

    def turn_off_play_btn(self):
        if self.is_play_btn_on:
            self.play_word_btn.unbind("<Button-1>")
            self.play_word_btn.bind("<Button-1>", self.show_empty_vocab_message)
            self.is_play_btn_on = False

    def turn_on_play_btn(self):
        if not self.is_play_btn_on:
            self.play_word_btn.unbind("<Button-1>")
            self.play_word_btn.bind("<Button-1>", self.say_word)
            self.is_play_btn_on = True

    def show_empty_vocab_message(self, event=None):
        if self.dialog is None or not self.dialog.winfo_exists():
            self.dialog = CTkToplevel(self)
            self.dialog.resizable(False, False)
            self.dialog.attributes("-topmost", True)
            self.dialog.transient(self)
            self.dialog.title("Vocabulary Empty")
            self.center_dialog()
            self.turn_off_play_btn()

            def configure_vocab_switch():
                switch_var = BooleanVar(value=self.current_user.only_from_vocabulary)
                only_vocab_switch.configure(variable=switch_var)

            def handle_switch():
                switch_value = only_vocab_switch.get()
                self.current_user.toggle_only_from_vocabulary(switch_value)
                if not switch_value:
                    self.turn_on_play_btn()
                    self.new_word()

            header = CTkLabel(self.dialog, text="Your vocabulary is empty!",
                              font=CTkFont(family="Arial", size=config.HEADER_FONT_SIZE, weight="bold"))
            message = CTkLabel(self.dialog, text="To continue practicing add more words to your vocabulary or "
                                                 "switch off \"Vocabulary only\" to practice spelling random words",
                               wraplength=220, justify="left")
            only_vocab_switch = CTkSwitch(self.dialog, text=strings.ONLY_VOCAB_SWITCH, onvalue=True, offvalue=False,
                                          font=CTkFont(family="Arial", underline=True),
                                          command=handle_switch)
            configure_vocab_switch()
            button = CTAButton(self.dialog, text="Ok", command=self.dialog.destroy, width=60, height=30)

            header.pack(pady=10)
            message.pack()
            only_vocab_switch.pack(pady=10)
            button.pack()
        else:
            self.dialog.focus()

    def center_dialog(self):
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        dialog_width = 270
        dialog_height = 200
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")


class SessionHistoryBlock(BaseFrame):
    def __init__(self, parent, controller):
        BaseFrame.__init__(self, parent, controller, width=config.WINDOW_WIDTH - 50)
        self.parent = parent
        self.controller = controller
        self.grid_propagate(False)
        self.statuses = []
        self.status_labels = []
        self.corrections = []
        self.correction_labels = []
        self.times_to_spell = []
        self.times_to_spell_labels = []
        self.user_input = []

        self.status_header = CTkLabel(self, text=strings.STATUS_HEADER)
        self.header_text = CTkLabel(self, text=strings.HISTORY_HEADER, font=CTkFont("Arial", config.HEADER_FONT_SIZE,
                                                                                    weight="bold"))
        self.times_to_spell_text = CTkLabel(self, text=strings.TIMES_TO_SPELL_HEADER)
        self.times_to_spell_tooltip = CustomToolTip(self.times_to_spell_text, text=strings.TIMES_TO_SPELL_TOOLTIP)
        self.filler_image = CTkLabel(self, text="", image=self.cat_image())

        self.status_header.grid(row=0, column=0)
        self.header_text.grid(row=0, column=0, columnspan=3)
        self.times_to_spell_text.grid(row=0, column=1, columnspan=2, padx=(0, 15), sticky=tk.E)
        self.filler_image.grid(row=0, column=3, rowspan=7, sticky=tk.E)

        # Create empty rows initially
        for _ in range(6):
            status_label = CTkLabel(self, text="")
            correction_label = CTkLabel(self, text="")
            times_to_spell_label = CTkLabel(self, text="")
            self.status_labels.append(status_label)
            self.correction_labels.append(correction_label)
            self.times_to_spell_labels.append(times_to_spell_label)

        # Display the rows
        for i, (status_label, correction_label, times_to_spell_label) in \
                enumerate(zip(self.status_labels, self.correction_labels, self.times_to_spell_labels), start=1):
            status_label.grid(row=i, column=0, sticky=tk.W, padx=20)
            correction_label.grid(row=i, column=1, sticky=tk.W)
            times_to_spell_label.grid(row=i, column=1, columnspan=2, padx=(0, 15), sticky=tk.E)
            self.grid_columnconfigure(0, minsize=100)
            self.grid_columnconfigure(1, minsize=300)
            self.grid_columnconfigure(2, minsize=100)

    @staticmethod
    def cat_image():
        return CTkImage(Image.open(helpers.get_path(f'assets/cat.png')), size=(200, 200))

    def update_user_input(self, word_dict, user_word, status):
        self.statuses.append(status)
        word = list(word_dict)[0]
        if constants.SPELLING in word_dict[word] and word_dict[word][constants.SPELLING] == constants.AmE:
            self.corrections.append(word_dict[word][constants.AmE])
        else:
            self.corrections.append(word)
        self.user_input.append(user_word.title())
        try:
            self.times_to_spell.append(
                self.parent.current_user.dictionaries.vocabulary[list(word_dict)[0]][constants.TIMES_TO_SPELL])
        except KeyError:
            self.times_to_spell.append("Learned")
        self.statuses = self.statuses[-6:]  # Limit the list size to 6

        # Update the displayed rows
        for i, (status, correction, times_to_spell) in enumerate(zip(self.status_labels, self.correction_labels,
                                                                     self.times_to_spell_labels)):
            if i < len(self.statuses):
                if self.statuses[-(i + 1)] == constants.CORRECT:
                    status.configure(text=self.statuses[-(i + 1)], text_color=config.GREEN)
                    correction.configure(text=self.corrections[-(i + 1)][:45])
                    times_to_spell.configure(text=self.times_to_spell[-(i + 1)])
                else:
                    status.configure(text=self.statuses[-(i + 1)], text_color=config.RED)
                    word = self.corrections[-(i + 1)]
                    user_word = self.user_input[-(i + 1)]
                    correction.configure(text=f"{word}. You wrote {user_word}"[:45])
                    times_to_spell.configure(text=self.times_to_spell[-(i + 1)])
            else:
                status.configure(text="")


class DefinitionBlock(BaseFrame):
    def __init__(self, parent, controller):
        BaseFrame.__init__(self, parent, controller, width=config.WINDOW_WIDTH - 430)
        self.parent = parent
        self.controller = controller
        self.scroll = None
        self.grid_propagate(False)

        # Create widgets and content blocks
        self.show_definition_btn = CTAButton(self, text=strings.SHOW_DEFINITION, command=self.show_definition,
                                             state=tk.DISABLED, width=120)
        self.definition_hint = HintLabel(self, text=strings.DEFINITION_HINT, wraplength=220, padx=10)
        self.definition_header = CTkLabel(self, text=strings.DEFINITION_HEADER, font=CTkFont(weight="bold"))
        self.horizontal_line = GreyLine(self, width=345)
        self.definition_field = self.create_definition_field()

        # Display widgets and content blocks on the page
        self.grid_columnconfigure(0, minsize=92)
        self.grid_columnconfigure(1, minsize=92)
        self.grid_columnconfigure(2, minsize=30)
        self.grid_rowconfigure(1, minsize=30)

        self.show_definition_btn.grid(row=0, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        self.definition_hint.grid(row=0, column=1, columnspan=2, padx=(38, 0), pady=(10, 0))
        self.horizontal_line.grid(row=2, column=0, columnspan=3, padx=(10, 0), pady=(0, 10), sticky=tk.NW)

    def create_definition_field(self):
        definition_field = Text(self, height=6, width=42, background="#333333", foreground="#FFFFFF",
                                cursor='arrow', wrap="word", highlightthickness=0, font=(None, 12))
        definition_field.tag_config("bold", font=CTkFont(None, 12, "bold"))
        return definition_field

    def show_definition(self):
        self.definition_hint.grid_forget()
        self.definition_header.grid(row=1, column=0, padx=(10, 0), sticky=tk.NW)
        self.definition_field.grid(row=3, column=0, rowspan=2, columnspan=3, padx=(8, 0), sticky=tk.W)
        if self.scroll:
            self.scroll.grid(row=3, column=3, columnspan=2)
        self.show_definition_btn.configure(state=tk.DISABLED, fg_color="#565b5e")

    def hide_definition(self, *args):
        self.definition_hint.grid(row=0, column=1, columnspan=2, padx=(38, 0), pady=(10, 0))
        self.definition_header.grid_forget()
        self.definition_field.grid_forget()
        if self.scroll:
            self.scroll.grid_forget()
        self.show_definition_btn.after(500, lambda: self.show_definition_btn.configure(state=tk.NORMAL,
                                                                                       fg_color="#246ba3"))

    def update_definition(self, word_dict):
        self.definition_field.configure(state=tk.NORMAL)
        self.definition_field.delete("1.0", tk.END)
        self.show_definition_btn.configure(state=tk.NORMAL, fg_color="#246ba3")

        word = list(word_dict)[0]
        if constants.DEFINITIONS not in word_dict[word] or word_dict[word][constants.DEFINITIONS] is None:
            self.definition_field.insert(tk.END, f"{strings.NO_DEFINITION_FOUND}")
        else:
            for part_of_speech in word_dict[word][constants.DEFINITIONS]:
                self.definition_field.insert(tk.END, f"{part_of_speech}:\n", "bold")
                for i, definition in enumerate(word_dict[word][constants.DEFINITIONS][part_of_speech], start=1):
                    self.definition_field.insert(tk.END, f"{i}. {definition}\n")
                self.definition_field.insert(tk.END, "\n")
            self.scroll = CTkScrollbar(self, height=105, command=self.definition_field.yview)
            self.definition_field.configure(yscrollcommand=self.scroll.set)
            self.definition_field.configure(state=tk.DISABLED)
            self.definition_field.bind('<Button-1>', lambda _: "break")
