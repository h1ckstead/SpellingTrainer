# from tkinter import *
# from tkinter import font
#
# import config
# import user
# from app.core.new_user_view import NewUserPage
# from app.core.main_page_view import MainPage
#
#
# class SpellingTrainerApp(Tk):
#     def __init__(self, *args, **kwargs):
#         Tk.__init__(self, *args, **kwargs)
#         self.title(config.APP_NAME)
#         self.title_font = font.Font(family=config.MAC_FONT, size=config.TITLE_FONT_SIZE, weight="bold")
#         self.font = font.Font(family=config.MAC_FONT, size=config.FONT_SIZE)
#         self.geometry(f'{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+{self.center_x()}+{self.center_y()}')
#
#         mainframe = Frame(self)
#         mainframe.pack(side="top", fill="both", expand=True)
#         mainframe.grid_rowconfigure(0, weight=1)
#         mainframe.grid_columnconfigure(0, weight=1)
#
#         saved_data = user.User.load_save()
#         if saved_data is None:
#             NewUserPage(parent=mainframe, controller=self).tkraise()
#         else:
#             MainPage(parent=mainframe, controller=self, saved_data=saved_data).tkraise()
#
#     def center_x(self):
#         user_screen_width = self.winfo_screenwidth()
#         return int(user_screen_width / 2 - config.WINDOW_WIDTH / 2)
#
#     def center_y(self):
#         user_screen_height = self.winfo_screenheight()
#         return int(user_screen_height / 2 - config.WINDOW_HEIGHT / 2)


# class MainPage(Frame):
#     def __init__(self, parent, controller, saved_data):
#         Frame.__init__(self, parent)
#         self.controller = controller
#         self.saved_data = saved_data
#         self.last_user = saved_data['last_user']
#         self.grid(row=0, column=0, sticky="nsew")
#
#         Label(self, text=self.greeting(), font=controller.title_font, pady=10).pack()
#         Label(self, text=config.DESCRIPTION_MAIN, font=controller.font, wraplength=config.WINDOW_WIDTH - 20).pack()
#         Button(self, text=f'Continue as {self.last_user}',
#                command=lambda: PracticePage(parent=parent, controller=self.controller,
#                                             current_user=saved_data[self.last_user]).tkraise()).pack()
#         Button(self, text='See complete stats', command=lambda: UserPage(parent=parent,
#                                                                          controller=self.controller,
#                                                                          current_user=self.saved_data[self.last_user],
#                                                                          session_attempts=0,
#                                                                          session_misspelled_lst=0).tkraise()).pack()
#         Button(self, text='Choose a different User',
#                command=lambda: ChooseDifferentUserPage(parent=parent,
#                                                        controller=self.controller,
#                                                        saved_data=self.saved_data).tkraise()).pack()
#         Button(self, text='New User',
#                command=lambda: NewUserPage(parent=parent,
#                                            controller=self.controller).tkraise()).pack()
#         Button(self, text='Exit', command=self.controller.destroy).pack()
#
#     def greeting(self):
#         return config.GREETING_MAIN.format(self.last_user, random.choice(config.GREETING_EMOJI))


# class NewUserPage(Frame):
#     def __init__(self, parent, controller):
#         Frame.__init__(self, parent)
#         self.controller = controller
#         self.parent = parent
#         self.grid(row=0, column=0, sticky="nsew")
#         self.canvas = Canvas(self, width=240, height=200)
#         self.avatars = self.avatars()
#         self.selected_avatar = None
#         self.selected_image_circle = None
#
#         Label(self, text=config.NEW_USER_GREETING).pack(side="top", fill="x", pady=10)
#         Label(self, text='Enter Username: ').pack()
#         entry_field = self.user_input()
#         Label(self, text='Choose avatar: ').pack()
#         self.display_avatars()
#         Button(self, text='Create', command=lambda: self.create_user(entry_field.get(), self.selected_avatar)).pack()
#         Button(self, text='Exit', command=self.controller.destroy).pack()
#
#     @staticmethod
#     def avatars():
#         avatars_dict = dict()
#         for avatar_name in config.AVATARS:
#             im = Image.open(f'assets/avatars/{avatar_name}')
#             im_tk = ImageTk.PhotoImage(im)
#             avatars_dict.update({avatar_name: {'img_object': im_tk}})
#         return avatars_dict
#
#     def display_avatars(self):
#         canvas = Canvas(self, width=243, height=243)
#         canvas.pack()
#         coordinates = [{'x': 3, 'y': 3}, {'x': 63, 'y': 3}, {'x': 123, 'y': 3}, {'x': 183, 'y': 3},
#                        {'x': 3, 'y': 63}, {'x': 63, 'y': 63}, {'x': 123, 'y': 63}, {'x': 183, 'y': 63},
#                        {'x': 3, 'y': 123}, {'x': 63, 'y': 123}, {'x': 123, 'y': 123}, {'x': 183, 'y': 123},
#                        {'x': 3, 'y': 183}, {'x': 63, 'y': 183}, {'x': 123, 'y': 183}, {'x': 183, 'y': 183}]
#         for i, avatar_name in enumerate(self.avatars):
#             place = coordinates[i]
#             canvas.create_image((place['x'], place['y']), anchor="nw", image=self.avatars[avatar_name]['img_object'],
#                                 tags=avatar_name)
#             self.avatars[avatar_name].update({'position': place})
#             canvas.tag_bind(avatar_name, "<Button-1>",
#                             lambda event, image_name=avatar_name: self.image_clicked(canvas, image_name))
#
#     def image_clicked(self, canvas, image_name):
#         print(f"The image {image_name} was clicked!")
#         if self.selected_image_circle is not None:
#             canvas.delete(self.selected_image_circle)
#             self.selected_avatar = None
#         position_x = self.avatars[image_name]['position']['x'] + 3
#         position_y = self.avatars[image_name]['position']['y'] + 3
#         self.selected_image_circle = canvas.create_oval(position_x, position_y, position_x+54, position_y+54,
#                                                         width=3, outline='white')
#         self.selected_avatar = image_name
#
#     def user_input(self):
#         user_entry = Entry(self)
#         user_entry.focus_set()
#         user_entry.pack()
#         return user_entry
#
#     def create_user(self, username, avatar):
#         if username == '':
#             messagebox.showerror(title='Enter username', message='Username cannot be empty!')
#         else:
#             new_user = user.User(username, avatar)
#             PracticePage(parent=self.parent, controller=self.controller, current_user=new_user).tkraise()


# class ChooseDifferentUserPage(Frame):
#     def __init__(self, parent, controller, saved_data):
#         Frame.__init__(self, parent)
#         self.controller = controller
#         self.saved_data = saved_data
#         self.grid(row=0, column=0, sticky="nsew")
#
#         Label(self, text=config.CHANGE_USER).pack(side="top", fill="x", pady=10)
#         users = [k for k in saved_data.keys() if k != 'last_user']
#         dropdown = ttk.Combobox(self, state="readonly", values=users)
#         dropdown.pack()
#         Button(text='Continue',
#                command=lambda: PracticePage(parent=parent,
#                                             controller=self.controller,
#                                             current_user=saved_data[dropdown.get()]).tkraise()).pack()


# class PracticePage(Frame):
#     def __init__(self, parent, controller, current_user):
#         Frame.__init__(self, parent)
#         self.controller = controller
#         self.current_user = current_user
#         self.session_attempts = 0
#         self.session_misspelled_lst = []
#         self.word = word_generation.next_word(self.current_user)
#         self.grid(row=0, column=0, sticky="nsew")
#
#         Label(self, text="Spelling Trainer - Practice!").pack(side="top", fill="x", pady=10)
#         Button(self, text='Listen to word', command=lambda: speech.read_aloud(self.word)).pack()
#         Button(self, text='Show definition', command=lambda: self.show_definition(self.word)).pack()
#         entry = Entry(self)
#         entry.pack()
#         entry.focus_set()
#         entry.bind('<Return>', lambda event: [self.spell_check(self.word, entry.get()),
#                                               entry.delete(0, 'end'),
#                                               self.new_word(self.current_user),
#                                               self.after(1000, lambda: speech.read_aloud(self.word))])
#         Button(self, text='Check',
#                command=lambda: [self.spell_check(self.word, entry.get()),
#                                 entry.delete(0, 'end'),
#                                 self.new_word(self.current_user),
#                                 self.after(1000, lambda: speech.read_aloud(self.word))]).pack()
#         Button(self, text='Finish',
#                command=lambda: [self.current_user.save_progress(),
#                                 ResultsPage(parent=parent,
#                                             controller=self.controller,
#                                             current_user=self.current_user,
#                                             session_attempts=self.session_attempts,
#                                             session_misspelled_lst=self.session_misspelled_lst).tkraise()]).pack()
#
#     def new_word(self, current_user):
#         self.word = word_generation.next_word(current_user)
#
#     @staticmethod
#     def get_definition(word):
#         dictionary = PyDictionary()
#         return dictionary.meaning(word)
#
#     def show_definition(self, word):
#         definition = self.get_definition(word)
#         Label(self, text=definition).pack()
#
#     def spell_check(self, word, user_word):
#         if word == '':
#             validation_msg = Label(self, text='Enter a word!')
#         elif user_word.lower() == word:
#             validation_msg = Label(self, text='Correct!')
#             self.current_user.correct += 1
#             self.session_attempts += 1
#             self.current_user.correctly_spelled_lst.append(word.title())
#         else:
#             validation_msg = Label(self, text=f"Incorrect! It's {word.title()}")
#             self.current_user.misspelled_lst.append(word.title())
#             self.session_misspelled_lst.append(word.title())
#         validation_msg.pack()
#         validation_msg.after(2000, lambda: validation_msg.destroy())


# class UserPage(Frame):
#     def __init__(self, parent, controller, current_user, session_attempts, session_misspelled_lst):
#         Frame.__init__(self, parent)
#         self.controller = controller
#         self.current_user = current_user
#         self.grid(row=0, column=0, sticky="nsew")
#
#         Label(self, text=f'Current user: {self.current_user.name}').pack()
#         Label(self, text=f'All time words practiced: '
#                          f'{self.current_user.correct + len(current_user.misspelled_lst)}').pack()
#         Button(self, text='Show personal vocabulary', command=lambda: self.show_personal_vocabulary(),
#                wraplength=config.WINDOW_WIDTH - 20).pack()
#         Label(self, text='Add word to personal vocabulary').pack()
#         word = Entry(self)
#         word.pack()
#         word.focus()
#         Button(self, text='Add', command=lambda: [self.add_word_to_vocabulary(word.get()),
#                                                   word.delete(0, 'end')]).pack()
#         Button(self, text='Exit', command=self.controller.destroy).pack()
#
#     def show_personal_vocabulary(self):
#         Label(self, text=f'{self.current_user.misspelled_lst}').pack()
#
#     def add_word_to_vocabulary(self, word):
#         self.current_user.misspelled_lst.append(word)
#         self.current_user.save_progress()


# class ResultsPage(Frame):
#     def __init__(self, parent, controller, current_user, session_attempts, session_misspelled_lst):
#         Frame.__init__(self, parent)
#         self.controller = controller
#         self.current_user = current_user
#         self.grid(row=0, column=0, sticky="nsew")
#
#         Label(self, text='These are your results: ').pack(side="top", fill="x", pady=10)
#         Label(self, text=f'Correctly spelled words: {session_attempts - len(session_misspelled_lst)}').pack()
#         Label(self, text=f'Incorrectly spelled words: {len(session_misspelled_lst)}').pack()
#         Label(self, text=f'Misspelled words: {session_misspelled_lst}', wraplength=config.WINDOW_WIDTH - 20).pack()
#         Button(self, text='See complete stats', command=lambda: UserPage(parent=parent,
#                                                                          controller=self.controller,
#                                                                          current_user=self.current_user,
#                                                                          session_attempts=session_attempts,
#                                                                          session_misspelled_lst=session_misspelled_lst).tkraise())
#         Button(self, text='Exit', command=self.controller.destroy).pack()


# def load_config():
#     with open(config.USER_CONFIG) as user_config:
#         return pickle.load(user_config)
