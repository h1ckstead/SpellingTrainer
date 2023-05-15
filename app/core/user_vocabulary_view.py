from tkinter import BooleanVar
from tkinter import messagebox

from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkCheckBox
import tkinter


# noinspection PyTypeChecker,PyAttributeOutsideInit
class UserVocabularyPage(CTkFrame):
    def __init__(self, parent, controller, current_user):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.current_user = current_user
        self.title = 'Vocabulary'
        self.page_size = 10
        self.current_page = 1
        self.total_pages = 0
        self.data = []
        self.grid(row=0, column=0, sticky="nsew")

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        self.header = CTkLabel(self, text='My vocabulary')
        self.header.grid(row=0, column=1, columnspan=2)

        self.search_entry = self.user_input()
        self.search_entry.grid(row=1, column=0, columnspan=2)

        self.search_btn = CTkButton(self, text='Search')
        self.search_btn.grid(row=1, column=2)

        self.select_all_var = BooleanVar()

        self.prev_button = CTkButton(self, text="Previous", command=self.go_to_previous_page)
        self.prev_button.grid(row=self.page_size+3, column=1)

        self.page_label = CTkLabel(self, text="Page: 1")
        self.page_label.grid(row=self.page_size+3, column=2)

        self.next_button = CTkButton(self, text="Next", command=self.go_to_next_page)
        self.next_button.grid(row=self.page_size+3, column=3)

        self.delete_button = CTkButton(self, text="Delete", state="disabled", command=self.delete_words)
        self.delete_button.grid(row=self.page_size+4, column=2)

        self.new_word_entry = self.user_input()
        self.new_word_entry.grid(row=self.page_size+5, column=0, columnspan=2)

        self.add_btn = CTkButton(self, text='Add', command=lambda: self.add_word(self.new_word_entry.get()))
        self.add_btn.grid(row=self.page_size+5, column=2)

        self.exit_btn = CTkButton(self, text='Exit', command=lambda: [self.current_user.save_progress(),
                                                                      self.controller.destroy()])
        self.exit_btn.grid(row=self.page_size+6, column=4)

    def load_data(self):
        self.data = list(self.current_user.dictionaries.vocabulary.keys())
        self.total_pages = (len(self.data) + self.page_size - 1) // self.page_size
        self.display_data()

    def display_data(self):
        self.clear_data_frame()

        self.checkboxes = []
        self.checkbox_vars = []

        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size
        current_page_data = self.data[start_index:end_index]

        if self.current_page == 1:
            self.prev_button.configure(state=tkinter.DISABLED)

        for row, word in enumerate(current_page_data, start=3):
            checkbox_var = BooleanVar()
            checkbox_var.trace('w', self.update_select_all_checkbox)
            self.checkbox_vars.append(checkbox_var)

            checkbox = CTkCheckBox(self, text=word, variable=checkbox_var, command=self.update_delete_button_state)
            checkbox.grid(row=row, column=1, pady=2, sticky='w')

            self.checkboxes.append(checkbox_var)
        self.display_master_checkbox()

    def display_master_checkbox(self):
        select_all_checkbox = CTkCheckBox(self, text="Select All/Deselect All", variable=self.select_all_var,
                                          command=lambda: [self.toggle_select_all(), self.update_delete_button_state()])
        select_all_checkbox.grid(row=2, column=1)

    def clear_data_frame(self):
        for widget in self.winfo_children():
            if isinstance(widget, CTkCheckBox):
                widget.destroy()
        self.select_all_var.set(False)

    def go_to_previous_page(self):
        if self.current_page > 1:
            self.next_button.configure(state=tkinter.NORMAL)
            self.current_page -= 1
            self.display_data()
            self.update_delete_button_state()
        if self.current_page == 1:
            self.prev_button.configure(state=tkinter.DISABLED)

    def go_to_next_page(self):
        if self.current_page < self.total_pages:
            self.prev_button.configure(state=tkinter.NORMAL)
            self.current_page += 1
            self.display_data()
            self.update_delete_button_state()
        if self.current_page == self.total_pages:
            self.next_button.configure(state=tkinter.DISABLED)

    def toggle_select_all(self):
        select_all = self.select_all_var.get()

        for checkbox_var in self.checkbox_vars:
            checkbox_var.set(select_all)

    def update_select_all_checkbox(self, *args):
        # Check if all individual checkboxes are checked or not and update the select all checkbox accordingly
        all_checked = all(var.get() for var in self.checkbox_vars)
        self.select_all_var.set(all_checked)

    def update_delete_button_state(self):
        checked_count = sum(var.get() for var in self.checkboxes)

        if checked_count > 0:
            self.delete_button.configure(text=f"Delete {checked_count} words", state=tkinter.NORMAL)
        else:
            self.delete_button.configure(text="Delete", state=tkinter.DISABLED)

    def user_input(self):
        user_entry = CTkEntry(self, width=250)
        user_entry.focus_set()
        return user_entry

    def add_word(self, word, spellcheck=True):
        word.title()
        if word == '':
            messagebox.showerror(message='Please, enter a word!')
        if spellcheck:
            misspelled = self.current_user.dictionaries.check_spelling(word)
            if misspelled:
                response = messagebox.askyesnocancel(
                    message=f'The word might be misspelled, did you mean to add {misspelled}?',
                    icon=messagebox.WARNING,
                    default=messagebox.YES,
                    # buttons=(f'Yes, add {misspelled}', f'No, add {word} anyways')
                )
                if response is None:
                    return
                elif response == 'yes':
                    self.add_word(misspelled, spellcheck=False)
                else:
                    self.add_word(word, spellcheck=False)
        status = self.current_user.dictionaries.add_word_to_vocab_manually(word)
        if status == 'already_exists':
            messagebox.showerror(message=f'The word "{word}" is already in your vocabulary')
        else:
            # TODO Instead of messagebox show like on practice page correct/incorrect
            messagebox.showinfo(message=f'The word "{word}" has been added to your vocabulary')
            self.load_data()

    def delete_words(self):
        words_to_delete = []
        for checkbox_var in self.checkbox_vars:
            if checkbox_var.get():
                index = self.checkbox_vars.index(checkbox_var)
                word = self.data[index]
                words_to_delete.append(word)
        self.current_user.dictionaries.delete_words(words_to_delete)
        self.load_data()  # refresh the list
