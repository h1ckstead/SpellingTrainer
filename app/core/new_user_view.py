from tkinter import Frame, Label, Button, Canvas, Entry
from app import config
from PIL import ImageTk, Image
from tkinter import messagebox
from app.core import user
from app.core.practice_page_view import PracticePage


class NewUserPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")
        self.canvas = Canvas(self, width=240, height=200)
        self.avatars = self.avatars()
        self.selected_avatar = None
        self.selected_image_circle = None

        Label(self, text=config.NEW_USER_GREETING).pack(side="top", fill="x", pady=10)
        Label(self, text='Enter Username: ').pack()
        entry_field = self.user_input()
        Label(self, text='Choose avatar: ').pack()
        self.display_avatars()
        Button(self, text='Create', command=lambda: self.create_user(entry_field.get(), self.selected_avatar)).pack()
        Button(self, text='Exit', command=self.controller.destroy).pack()

    @staticmethod
    def avatars():
        avatars_dict = dict()
        for avatar_name in config.AVATARS:
            im = Image.open(f'assets/avatars/{avatar_name}')
            im_tk = ImageTk.PhotoImage(im)
            avatars_dict.update({avatar_name: {'img_object': im_tk}})
        return avatars_dict

    def display_avatars(self):
        canvas = Canvas(self, width=243, height=243)
        canvas.pack()
        coordinates = [{'x': 3, 'y': 3}, {'x': 63, 'y': 3}, {'x': 123, 'y': 3}, {'x': 183, 'y': 3},
                       {'x': 3, 'y': 63}, {'x': 63, 'y': 63}, {'x': 123, 'y': 63}, {'x': 183, 'y': 63},
                       {'x': 3, 'y': 123}, {'x': 63, 'y': 123}, {'x': 123, 'y': 123}, {'x': 183, 'y': 123},
                       {'x': 3, 'y': 183}, {'x': 63, 'y': 183}, {'x': 123, 'y': 183}, {'x': 183, 'y': 183}]
        for i, avatar_name in enumerate(self.avatars):
            place = coordinates[i]
            canvas.create_image((place['x'], place['y']), anchor="nw", image=self.avatars[avatar_name]['img_object'],
                                tags=avatar_name)
            self.avatars[avatar_name].update({'position': place})
            canvas.tag_bind(avatar_name, "<Button-1>",
                            lambda event, image_name=avatar_name: self.image_clicked(canvas, image_name))

    def image_clicked(self, canvas, image_name):
        print(f"The image {image_name} was clicked!")
        if self.selected_image_circle is not None:
            canvas.delete(self.selected_image_circle)
            self.selected_avatar = None
        position_x = self.avatars[image_name]['position']['x'] + 3
        position_y = self.avatars[image_name]['position']['y'] + 3
        self.selected_image_circle = canvas.create_oval(position_x, position_y, position_x+54, position_y+54,
                                                        width=3, outline='white')
        self.selected_avatar = image_name

    def user_input(self):
        user_entry = Entry(self)
        user_entry.focus_set()
        user_entry.pack()
        return user_entry

    def create_user(self, username, avatar):
        if username == '':
            messagebox.showerror(title='Enter username', message='Username cannot be empty!')
        else:
            new_user = user.User(username, avatar)
            PracticePage(parent=self.parent, controller=self.controller, current_user=new_user).tkraise()
