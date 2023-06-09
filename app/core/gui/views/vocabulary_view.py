import platform
import tkinter as tk
from _tkinter import TclError
from tkinter import StringVar, Label, BooleanVar, messagebox

from PIL import Image, ImageTk
from customtkinter import CTkFrame, CTkComboBox, CTkFont, CTkImage, CTkLabel, CTkCheckBox, CTkButton, CTkSwitch, \
    CTkProgressBar, CTkToplevel

from core import config, strings, constants
from core.gui.elements import Button, CTAButton, GreyLine, EntryField, HintLabel
from core.gui.views.base_view import BaseView, BaseFrame
from util import helpers


class VocabularyPage(BaseView):
    def __init__(self, parent, controller, previous_page, current_user):
        super().__init__(parent, controller)
        self.parent = parent
        self.controller = controller
        self.previous_page = previous_page  # Profile Page
        self.current_user = current_user

        avatar_image = Image.open(helpers.get_path(f"assets/avatars/{self.current_user.avatar}"))
        avatar_image = avatar_image.resize((60, 60), Image.ANTIALIAS)
        self.avatar = ImageTk.PhotoImage(avatar_image)

        # Create widgets and content blocks
        self.title_text = Label(self, text=strings.VOCABULARY, background="#333333", foreground="#FFFFFF",
                                image=self.avatar, padx=10,
                                compound=tk.LEFT,
                                font=self.controller.title_font)
        self.vocabulary_block = VocabularyBlock(self, controller=self.controller, current_user=self.current_user)
        self.add_words_block = AddWordsBlock(self, controller=self.controller, current_user=self.current_user)
        self.horizontal_line = GreyLine(self, width=100)
        self.about_block = AboutBlock(self, controller=self.controller)
        self.back_btn = CTAButton(self, text=strings.BACK_BUTTON_TEXT, command=lambda: self.previous_page.tkraise())

        # Display widgets and content blocks on the page

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.title_text.grid(row=0, column=0, columnspan=4, pady=(20, 15))
        self.vocabulary_block.grid(row=1, column=1, rowspan=3, padx=10)
        self.add_words_block.grid(row=1, column=2, sticky=tk.N)
        self.about_block.grid(row=2, column=2)
        self.back_btn.grid(row=3, column=2, sticky=tk.E)
        self.report_bug_btn.grid(row=5, column=0, columnspan=4, pady=(0, 5))


class VocabularyBlock(BaseFrame):
    def __init__(self, parent, controller, current_user):
        BaseFrame.__init__(self, parent, controller, width=config.WINDOW_WIDTH - 500, height=config.WINDOW_HEIGHT - 150)
        self.parent = parent
        self.controller = controller
        self.current_user = current_user
        self.grid_propagate(False)

        self.page_size = 14
        self.current_page = 1
        self.total_pages = 0
        self.checkboxes = []
        self.checkbox_vars = []
        self.empty_msg = None
        self.empty_text = None
        self.matched_subset = None
        self.user_vocabulary_copy = None

        self.search_field = EntryField(self, placeholder_text=strings.SEARCH_PLACEHOLDER, width=170, validate=True,
                                       max_chars=50)
        self.search_field.bind("<KeyRelease>", lambda event: self.on_entry_change())
        self.clear_btn = CTAButton(self, text=strings.CLEAR_BTN, width=50, height=28, state=tk.DISABLED,
                                   command=self.clear_search_field)
        self.line = GreyLine(self, width=270)
        self.select_all_var = BooleanVar()
        self.times_to_spell = CTkLabel(self, text=strings.TIMES_TO_SPELL, font=CTkFont("Arial", 11, weight="bold"),
                                       height=15)
        self.prev_button = CTkButton(self, text="",
                                     image=CTkImage(Image.open(helpers.get_path('assets/prev.png')), size=(15, 15)),
                                     command=self.go_to_previous_page, width=40)
        self.page_label = CTkLabel(self, text="")
        self.next_button = CTkButton(self, text="",
                                     image=CTkImage(Image.open(helpers.get_path('assets/next.png')), size=(15, 15)),
                                     command=self.go_to_next_page, width=40)
        self.delete_button = CTkButton(self, text=strings.DELETE, state=tk.DISABLED, fg_color="#565b5e",
                                       command=self.delete_words)

        # Display widgets and content blocks on the page
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.search_field.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=tk.W)
        self.search_field.bind("<KeyRelease>", lambda event: self.after(500, self.display_vocabulary_subset, event))
        self.clear_btn.grid(row=0, column=0, pady=10, sticky=tk.E)
        self.line.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        self.display_sorting_dropdown()
        self.load_vocabulary()
        self.times_to_spell.grid(row=3, column=0, columnspan=2, sticky=tk.E)
        self.prev_button.grid(row=18, column=0, padx=10, pady=(10, 0), sticky=tk.W)
        self.page_label.grid(row=18, column=0, columnspan=2, pady=(10, 0))
        self.next_button.grid(row=18, column=1, pady=(10, 0), sticky=tk.E)
        self.delete_button.grid(row=19, column=0, columnspan=2)

    def load_vocabulary(self, event=None, matched_words=None):
        if not self.current_user.dictionaries.vocabulary:
            self.show_empty_vocab_message()
            return
        if matched_words:
            self.matched_subset = matched_words
            self.total_pages = (len(self.matched_subset) + self.page_size - 1) // self.page_size
        else:
            self.total_pages = (len(self.current_user.dictionaries.vocabulary) + self.page_size - 1) // self.page_size

        if self.sorting.get():
            self.on_sorting_change()
        self.display_vocabulary()

    def clear_search_field(self):
        self.search_field.delete(0, 'end'), self.enable_prev_next_buttons(),
        self.matched_subset = None
        self.load_vocabulary(),
        self.on_entry_change()

    def on_entry_change(self):
        stripped_text = self.search_field.get().strip()
        if stripped_text:
            self.clear_btn.configure(state=tk.NORMAL, fg_color="#246ba3")
        else:
            self.matched_subset = None
            self.clear_btn.configure(state=tk.DISABLED, fg_color="#565b5e")

    def display_vocabulary_subset(self, event=None, reset_page=True):
        search_text = self.search_field.get().lower()
        if search_text:
            matched_words = self.search_vocabulary(search_text)
            if matched_words:
                if reset_page:
                    self.current_page = 1
                subset_dict = {key: self.current_user.dictionaries.vocabulary[key] for key in matched_words
                               if key in self.current_user.dictionaries.vocabulary}
                self.load_vocabulary(matched_words=subset_dict)
            else:
                self.show_word_not_found(search_text)
        else:
            self.load_vocabulary()

    def display_sorting_dropdown(self):
        sorting_hint = CTkLabel(self, text=strings.SORT_BY, font=CTkFont("Arial", 10), height=15)
        self.sorting = CTkComboBox(self, state="readonly", cursor="arrow", width=110, height=20,
                                   font=CTkFont("Arial", 10), values=strings.SORTING_OPTIONS,
                                   command=self.on_sorting_change)
        self.sorting.grid(row=2, column=0, columnspan=2, sticky=tk.E)
        self.sorting.focus_set()  # To avoid bug where default_value appears only on hover
        sorting_hint.grid(row=2, column=0, columnspan=2, padx=(25, 0), pady=(0, 5))

    def on_sorting_change(self, event=None):
        sort_choice = self.sorting.get()
        if sort_choice == strings.AZ:
            self.sort_alphabetically()
        elif sort_choice == strings.ZA:
            self.sort_alphabetically(reverse=True)
        elif sort_choice == strings.TIMES_TO_SPELL_DESC:
            self.sort_by_times_to_spell(reverse=True)
        elif sort_choice == strings.TIMES_TO_SPELL_ASC:
            self.sort_by_times_to_spell()

    def sort_alphabetically(self, reverse=False):
        if self.matched_subset:
            to_sort = self.matched_subset
        else:
            to_sort = self.current_user.dictionaries.vocabulary.copy()
        self.user_vocabulary_copy = dict(sorted(to_sort.items(), reverse=reverse))
        self.display_vocabulary()  # Redisplay the sorted vocabulary

    def sort_by_times_to_spell(self, reverse=False):
        if self.matched_subset:
            to_sort = self.matched_subset
        else:
            to_sort = self.current_user.dictionaries.vocabulary.copy()
        self.user_vocabulary_copy = dict(sorted(to_sort.items(), key=lambda x: x[1][constants.TIMES_TO_SPELL],
                                                reverse=reverse))
        self.display_vocabulary()  # Redisplay the sorted vocabulary

    def create_empty_rows(self):
        for i in range(self.page_size):
            placeholder_label = CTkLabel(self, text="0", text_color="#2b2b2b", height=18)
            placeholder_label.grid(row=i + 4, column=0, columnspan=2, pady=1, sticky=tk.EW)

    def show_empty_vocab_message(self):
        self.clear_data_frame()
        self.create_empty_rows()
        self.empty_msg = CTkLabel(self, text=strings.EMPTY_VOCAB_HEADER, font=("Arial", config.HEADER_FONT_SIZE),
                                  wraplength=250)
        self.empty_text = CTkLabel(self, text=strings.EMPTY_VOCAB_TEXT, wraplength=250)
        self.empty_msg.grid(row=4, column=0, columnspan=2, rowspan=7)
        self.empty_text.grid(row=8, column=0, columnspan=2, rowspan=7)
        self.next_button.configure(state=tk.DISABLED, fg_color="#565b5e")
        self.prev_button.configure(state=tk.DISABLED, fg_color="#565b5e")

    def show_word_not_found(self, search_text):
        self.clear_data_frame()
        self.create_empty_rows()
        self.empty_msg = CTkLabel(self, text=strings.NOT_FOUND.format(search_text), wraplength=250)
        self.empty_msg.grid(row=4, column=0, columnspan=2, rowspan=7)
        self.next_button.configure(state=tk.DISABLED, fg_color="#565b5e")
        self.prev_button.configure(state=tk.DISABLED, fg_color="#565b5e")

    def display_vocabulary(self, *args):
        self.clear_data_frame()
        self.checkboxes = []
        self.checkbox_vars = []

        if self.user_vocabulary_copy and self.matched_subset:  # sort
            words_to_display = self.user_vocabulary_copy
        elif self.user_vocabulary_copy:
            words_to_display = self.user_vocabulary_copy
        elif self.matched_subset:
            words_to_display = self.matched_subset
        else:
            words_to_display = self.current_user.dictionaries.vocabulary
        self.current_page = min(self.current_page, self.total_pages)

        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size
        current_page_data = list(words_to_display)[start_index:end_index]

        self.update_prev_next_buttons()

        for row, word in enumerate(current_page_data, start=4):
            checkbox_var = BooleanVar()
            checkbox_var.trace('w', self.update_select_all_checkbox)
            self.checkbox_vars.append(checkbox_var)

            times_to_spell = words_to_display[word][constants.TIMES_TO_SPELL]
            label_text = f"{word}"
            checkbox = CTkCheckBox(self, checkbox_width=18, checkbox_height=18, border_width=1, height=15,
                                   text=label_text, variable=checkbox_var,
                                   command=self.update_delete_button_state)
            checkbox.grid(row=row, column=0, padx=(10, 0), pady=1, sticky=tk.W)

            times_to_spell_label = CTkLabel(self, text=f"{times_to_spell}", height=15)
            times_to_spell_label.grid(row=row, column=1, padx=(10, 0), pady=1)
            self.checkboxes.append(checkbox_var)
        self.display_master_checkbox()

        # Add empty rows or placeholder widgets to fill the remaining space
        remaining_rows = self.page_size - len(current_page_data)
        for i in range(remaining_rows):
            placeholder_label = CTkLabel(self, text="0", text_color="#2b2b2b", height=18)
            placeholder_label.grid(row=i + len(current_page_data) + 4, column=0, columnspan=2, pady=1,
                                   sticky=tk.EW)

        self.page_label.configure(text=f"Page: {self.current_page}/{self.total_pages}")

    def update_prev_next_buttons(self):
        if self.total_pages <= 1 or self.current_page == 1:
            self.prev_button.configure(state=tk.DISABLED, fg_color="#565b5e")
        else:
            self.prev_button.configure(state=tk.NORMAL, fg_color="#246ba3")

        if self.current_page < self.total_pages:
            self.next_button.configure(state=tk.NORMAL, fg_color="#246ba3")
        else:
            self.next_button.configure(state=tk.DISABLED, fg_color="#565b5e")

    def update_delete_button_state(self):
        checked_count = sum(var.get() for var in self.checkboxes)
        if checked_count > 0:
            self.delete_button.configure(text=f"Delete {checked_count} word(s)", state=tk.NORMAL, fg_color="#246ba3")
        else:
            self.delete_button.configure(text="Delete", state=tk.DISABLED, fg_color="#565b5e")

    def update_select_all_checkbox(self, *args):
        if not self.empty_msg:  # Check if no word found message is displayed
            for checkbox_var in self.checkbox_vars:
                if checkbox_var in self.checkboxes:  # Check if checkbox variable still exists
                    all_checked = all(checkbox_var.get() for checkbox_var in self.checkbox_vars)
                    self.select_all_var.set(all_checked)

    def display_master_checkbox(self):
        select_all_checkbox = CTkCheckBox(self, checkbox_width=18, checkbox_height=18, border_width=1,
                                          text=strings.SELECT_ALL, font=CTkFont("Arial", weight="bold"),
                                          variable=self.select_all_var,
                                          command=lambda: [self.toggle_select_all(), self.update_delete_button_state()])
        select_all_checkbox.grid(row=2, column=0, rowspan=2, padx=10, sticky=tk.W)

    def enable_prev_next_buttons(self):
        self.prev_button.configure(state=tk.NORMAL, fg_color="#246ba3")
        self.next_button.configure(state=tk.NORMAL, fg_color="#246ba3")

    def clear_data_frame(self):
        self.checkboxes = []
        self.checkbox_vars = []
        self.select_all_var.set(False)
        self.update_delete_button_state()

        if self.empty_msg:
            try:
                self.empty_msg.destroy()
            except TclError:
                pass
            self.empty_msg = None

        if self.empty_text:
            try:
                self.empty_text.destroy()
            except TclError:
                pass
            self.empty_text = None

        for widget in self.winfo_children():
            if isinstance(widget, CTkCheckBox):
                widget.destroy()
            elif isinstance(widget, CTkLabel):
                try:
                    value = int(widget.cget("text"))
                    widget.destroy()
                except ValueError:
                    pass

    def go_to_previous_page(self):
        if self.current_page > 1:
            self.next_button.configure(state=tk.NORMAL, fg_color="#246ba3")
            self.current_page -= 1
            self.display_vocabulary()
            self.update_delete_button_state()
        if self.current_page == 1:
            self.prev_button.configure(state=tk.DISABLED, fg_color="#565b5e")

    def go_to_next_page(self):
        if self.current_page < self.total_pages:
            self.prev_button.configure(state=tk.NORMAL, fg_color="#246ba3")
            self.current_page += 1
            self.display_vocabulary()
            self.update_delete_button_state()
        if self.current_page == self.total_pages:
            self.next_button.configure(state=tk.DISABLED, fg_color="#565b5e")

    def toggle_select_all(self):
        select_all = self.select_all_var.get()

        for checkbox_var in self.checkbox_vars:
            checkbox_var.set(select_all)

    def search_vocabulary(self, search_text):
        matched_words = []
        for word in self.current_user.dictionaries.vocabulary:
            if search_text in word.lower():
                matched_words.append(word)
        return matched_words

    def delete_words(self):
        words_to_delete = []
        checkbox_vars_to_delete = []  # Keep track of checkbox variables to delete

        start_index = (self.current_page - 1) * self.page_size

        for i, checkbox_var in enumerate(self.checkbox_vars, start=start_index):
            if checkbox_var.get():
                if self.user_vocabulary_copy and self.matched_subset:
                    word = list(self.user_vocabulary_copy)[i]
                elif self.matched_subset:
                    word = list(self.matched_subset)[i]
                elif self.user_vocabulary_copy:
                    word = list(self.user_vocabulary_copy)[i]
                else:
                    word = list(self.current_user.dictionaries.vocabulary)[i]
                words_to_delete.append(word)
                checkbox_vars_to_delete.append(checkbox_var)  # Store the checkbox variable to delete

        response = self.show_delete_conformation(words_to_delete)
        if response == tk.YES:
            self.current_user.dictionaries.delete_words(words_to_delete)

            # Remove the associated checkbox variables
            for checkbox_var in checkbox_vars_to_delete:
                self.checkbox_vars.remove(checkbox_var)

            self.current_user.save_progress()
            if self.matched_subset:
                self.display_vocabulary_subset(reset_page=False)
            else:
                self.load_vocabulary()  # Refresh the list

    @staticmethod
    def show_delete_conformation(words_to_delete):
        response = messagebox.askyesno(title="Are you sure?",
                                       message=f"Are you sure you want to delete {len(words_to_delete)} word(s)?\n"
                                               "This action cannot be undone")
        return response


class AddWordsBlock(BaseFrame):
    def __init__(self, parent, controller, current_user):
        BaseFrame.__init__(self, parent, controller, width=config.WINDOW_WIDTH - 350, height=config.WINDOW_HEIGHT - 350)
        self.parent = parent
        self.controller = controller
        self.current_user = current_user
        self.dialog = None
        self.grid_propagate(False)

        self.title = CTkLabel(self, text=strings.ADD_WORDS_HEADER, font=CTkFont("Arial", config.HEADER_FONT_SIZE,
                                                                                weight="bold"))
        self.hint = CTkLabel(self, text=strings.ADD_WORDS_HINT, wraplength=350, font=CTkFont("Arial", 12))
        self.entry_field = EntryField(self, placeholder_text=strings.ADD_WORD, width=200, validate=True, max_chars=45)
        self.entry_field.bind("<KeyRelease>", lambda event: self.on_entry_change())
        self.add_btn = CTAButton(self, text=strings.ADD, width=50, height=28, state=tk.DISABLED, fg_color="#565b5e",
                                 command=lambda: self.add_word(self.entry_field.get().strip().title()))
        self.line = GreyLine(self, width=400)
        self.double_spelling = CTAButton(self, text=strings.DOUBLE_SPELLING_BTN, height=30,
                                         command=self.add_word_double_spelling)
        self.double_spelling_hint = CTkLabel(self, text=strings.DOUBLE_SPELLING_HINT, wraplength=350,
                                             font=CTkFont("Arial", 12))

        # Display widgets and content blocks on the page
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.title.grid(row=0, column=0, columnspan=2, pady=10)
        self.hint.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        self.entry_field.grid(row=2, column=0, columnspan=2, padx=(25, 0), sticky=tk.W)
        self.add_btn.grid(row=2, column=1, columnspan=2, padx=10, sticky=tk.W)
        self.line.grid(row=3, column=0, columnspan=2, pady=10)
        self.double_spelling_hint.grid(row=4, column=0, columnspan=2)
        self.double_spelling.grid(row=5, column=0, columnspan=2, pady=(15, 0))

    def on_entry_change(self):
        stripped_text = self.entry_field.get().strip()
        if stripped_text:
            self.add_btn.configure(state=tk.NORMAL, fg_color="#246ba3")
        else:
            self.add_btn.configure(state=tk.DISABLED, fg_color="#565b5e")

    def add_word(self, word, spellcheck=True):
        if spellcheck:
            misspelled = self.current_user.dictionaries.check_spelling(word)
            if misspelled:
                response = messagebox.askyesnocancel(
                    message=f'The word might be misspelled, did you mean to add "{misspelled.title()}"? Press [Yes] '
                            f'to add "{misspelled.title()}", press [No] to add "{word}" anyways.',
                    icon=messagebox.WARNING,
                    default=messagebox.YES,
                )
                if response is None:
                    return
                elif response:
                    self.add_word(misspelled.title(), spellcheck=False)
                    return
                else:
                    self.add_word(word.title(), spellcheck=False)
                    return
        status = self.current_user.dictionaries.add_word_to_vocab_manually(word)
        if status == constants.ALREADY_EXISTS:
            messagebox.showerror(message=f'The word "{word}" is already in your vocabulary')
        else:
            success_message = self.show_success_message(word)
            success_message.grid(row=0, column=0, columnspan=2, rowspan=2)
            self.entry_field.delete(0, 'end')
            self.add_btn.configure(state=tk.DISABLED, fg_color="#565b5e")
            self.current_user.save_progress()
            if self.parent.vocabulary_block.matched_subset:
                self.parent.vocabulary_block.display_vocabulary_subset(reset_page=False)
            else:
                self.parent.vocabulary_block.load_vocabulary()
            self.update_practice_page()
            self.update_user_stats()
            success_message.after(3000, lambda: success_message.destroy())

    def show_success_message(self, word):
        container = CTkFrame(self, width=400, height=50, border_width=2, border_color=config.GREEN)
        validation_msg = CTkLabel(container, wraplength=350, width=400, height=50,
                                  text=f'The word "{word}" has been added to your vocabulary',
                                  text_color=config.GREEN)
        validation_msg.pack(padx=10, pady=10)
        return container

    def add_word_double_spelling(self):
        if self.dialog is None or not self.dialog.winfo_exists():
            self.dialog = CTkToplevel(self)
            if platform.system() == 'Windows':
                self.dialog.iconbitmap(helpers.get_path("assets", "favicon.ico"))
            self.dialog.resizable(False, False)
            self.dialog.attributes("-topmost", True)
            self.dialog.transient(self)
            self.dialog.title("Add new word")
            self.center_dialog()
            self.dialog.grab_set()

            def validate_entries(*args):
                if british_entry.get().strip() and american_entry.get().strip():
                    add.configure(state=tk.NORMAL, fg_color="#246ba3")
                else:
                    add.configure(state=tk.DISABLED, fg_color="#565b5e")

            british_label = CTkLabel(self.dialog, text=strings.BRITISH_SPELLING)
            british_entry_var = StringVar(self.dialog)
            british_entry = EntryField(self.dialog, textvariable=british_entry_var, validate=True, max_chars=45)
            british_entry_var.trace('w', validate_entries)
            american_label = CTkLabel(self.dialog, text=strings.AMERICAN_SPELLING)
            american_entry_var = StringVar(self.dialog)
            american_entry = EntryField(self.dialog, textvariable=american_entry_var, validate=True, max_chars=45)
            american_entry_var.trace('w', validate_entries)
            cancel = Button(self.dialog, text=strings.CANCEL, width=60, command=self.dialog.destroy)
            add = CTAButton(self.dialog, text=strings.ADD, width=60, state=tk.DISABLED, fg_color="#565b5e",
                            command=lambda: self.add_word_with_double_spelling(british_entry.get().strip().title(),
                                                                               american_entry.get().strip().title()))
            british_label.grid(row=0, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky=tk.W)
            british_entry.grid(row=1, column=0, columnspan=2, padx=(10, 0), sticky=tk.W)
            british_entry.focus_set()
            american_label.grid(row=3, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky=tk.W)
            american_entry.grid(row=4, column=0, columnspan=2, padx=(10, 0), pady=(0, 10), sticky=tk.W)
            cancel.grid(row=5, column=0)
            add.grid(row=5, column=1)
        else:
            self.dialog.focus()

    def center_dialog(self):
        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()
        dialog_width = 270
        dialog_height = 200
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    def add_word_with_double_spelling(self, word, alt_spelling):
        status = self.current_user.dictionaries.add_word_to_vocab_manually(word, alternative_spelling=alt_spelling)
        if status == constants.ALREADY_EXISTS:
            messagebox.showerror(message=f'The word "{word}" is already in your vocabulary')
        else:
            self.current_user.save_progress()
            if self.parent.vocabulary_block.matched_subset:
                self.parent.vocabulary_block.display_vocabulary_subset(reset_page=False)
            else:
                self.parent.vocabulary_block.load_vocabulary()
            self.update_practice_page()
            self.update_user_stats()
            success_message = self.show_success_message(word)
            success_message.grid(row=0, column=0, columnspan=2, rowspan=2)
            self.dialog.destroy()
            success_message.after(3000, lambda: success_message.destroy())

    def update_practice_page(self):
        self.parent.previous_page.previous_page.spelling_trainer_block.turn_on_play_btn()

    def update_user_stats(self):
        self.parent.previous_page.session.new_words += 1
        self.parent.previous_page.overall_statistics_block.to_learn.configure(
            text=len(self.current_user.dictionaries.vocabulary))
        self.parent.previous_page.session_statistics_block.to_learn.configure(
            text=self.parent.previous_page.session.new_words)


class AboutBlock(BaseFrame):
    def __init__(self, parent, controller):
        BaseFrame.__init__(self, parent, controller, width=config.WINDOW_WIDTH - 350, height=config.WINDOW_HEIGHT - 450)
        self.parent = parent
        self.controller = controller
        self.grid_propagate(False)

        self.text = CTkLabel(self, text=strings.VOCAB_TUTORIAL_TEXT, wraplength=150, justify=tk.LEFT,
                             font=CTkFont(family="Arial", size=12))
        self.line = self.create_vertical_line()
        self.only_vocab_switch = CTkSwitch(self, text=strings.ONLY_VOCAB_SWITCH, onvalue=True, offvalue=False,
                                           font=CTkFont(family="Arial", underline=True),
                                           command=self.on_vocab_switch)
        self.configure_vocab_switch()
        self.only_vocab_hint = HintLabel(self, text=strings.ONLY_VOCAB_HINT, image=False, wraplength=150)

        # Display widgets and content blocks on the page
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.text.grid(row=0, column=0, rowspan=2)
        self.line.grid(row=0, column=1, rowspan=2)
        self.only_vocab_switch.grid(row=0, column=2, pady=(10, 0), sticky=tk.N)
        self.only_vocab_hint.grid(row=0, column=2, rowspan=2, pady=(0, 40))

    def configure_vocab_switch(self):
        switch_var = BooleanVar(value=self.parent.current_user.only_from_vocabulary)
        self.only_vocab_switch.configure(variable=switch_var)

    def on_vocab_switch(self):
        self.parent.current_user.toggle_only_from_vocabulary(self.only_vocab_switch.get())
        if self.parent.previous_page.previous_page.spelling_trainer_block.word_dict:
            self.parent.previous_page.previous_page.spelling_trainer_block.word_dict = None

    def create_vertical_line(self):
        line = CTkProgressBar(self, orientation=tk.VERTICAL, height=config.WINDOW_HEIGHT - 470, width=2,
                              progress_color="#aab0b5")
        line.set(1)
        return line
