from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkImage, CTkSwitch, CTkEntry, StringVar, CTkToplevel, \
    CTkCanvas

from app import config
from PIL import ImageTk, Image


# noinspection PyAttributeOutsideInit
class UserSettingsPage(CTkFrame):
    def __init__(self, parent, controller, current_user):
        CTkFrame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.current_user = current_user
        self.avatars = self.avatars()
        self.selected_image_circle = None
        self.grid(row=0, column=0, sticky="nsew")

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        self.header = CTkLabel(self, text='My settings', font=self.controller.title_font)
        self.header.grid(row=0, column=1, columnspan=2, pady=5)

        self.avatar = CTkLabel(self, text='')
        self.avatar.grid(row=1, column=0)

        self.edit_avatar_btn = CTkButton(self, text='Edit', command=self.open_avatar_selection)
        self.edit_avatar_btn.grid(row=2, column=0)

        self.username = CTkLabel(self, text=self.current_user.name)
        self.username.grid(row=1, column=1)

        self.edit_username_btn = CTkButton(self, text='Edit', command=self.show_new_username_entry)
        self.edit_username_btn.grid(row=1, column=2)

        self.username_entry = CTkEntry(self)
        self.save_username_btn = CTkButton(self, text='Save', command=self.edit_username)

        self.strict_spelling = CTkSwitch(self, text='Strict spelling', onvalue="True", offvalue="False",
                                         command=self.update_strict_spelling)
        self.strict_spelling.grid(row=2, column=1)

        self.exit_btn = CTkButton(self, text='Exit', command=lambda: [self.current_user.save_progress(),
                                                                      self.controller.destroy()])
        self.exit_btn.grid(row=3, column=3)

    def load_data(self):
        self.avatar.configure(image=CTkImage(Image.open(f'assets/avatars/{self.current_user.avatar}'), size=(60, 60)))
        switch_var = StringVar(value=self.current_user.strict_spelling)
        self.strict_spelling.configure(variable=switch_var)

    def open_avatar_selection(self):
        popup = CTkToplevel(self.parent)
        popup.title("Avatar Selection")
        # popup.geometry("243x")

        # Calculate the center of the parent window
        parent_center_x = self.winfo_rootx() + self.winfo_width() // 2
        parent_center_y = self.winfo_rooty() + self.winfo_height() // 2

        # Calculate the top-left corner of the CTkToplevel window
        popup_width = 245
        popup_height = 306
        popup_x = parent_center_x - popup_width // 2
        popup_y = parent_center_y - popup_height // 2

        # Set the CTkToplevel window's geometry to center it on the parent window
        popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

        popup.transient(self)
        popup.grab_set()

        canvas = CTkCanvas(popup, width=243, height=243)
        canvas.grid()

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
        self.image_clicked(canvas, self.current_user.avatar)  # Highlight existing user avatar

        def select_avatar():
            self.current_user.edit_avatar(self.selected_avatar)
            self.avatar.configure(image=CTkImage(Image.open(f'assets/avatars/{self.current_user.avatar}'),
                                                 size=(60, 60)))
            popup.destroy()

        select_btn = CTkButton(popup, text="Select", command=select_avatar)
        select_btn.grid()

        cancel_btn = CTkButton(popup, text="Cancel", command=popup.destroy)
        cancel_btn.grid()

    def image_clicked(self, canvas, image_name):
        #  TODO: Remove debug prints
        print(f"The image {image_name} was clicked!")
        if self.selected_image_circle is not None:
            canvas.delete(self.selected_image_circle)
            self.selected_avatar = None
        position_x = self.avatars[image_name]['position']['x'] + 3
        position_y = self.avatars[image_name]['position']['y'] + 3
        self.selected_image_circle = canvas.create_oval(position_x, position_y, position_x+54, position_y+54,
                                                        width=3, outline='white')
        self.selected_avatar = image_name

    @staticmethod
    def avatars():
        # TODO: Custom TkInter
        avatars_dict = dict()
        for avatar_name in config.AVATARS:
            im = Image.open(f'assets/avatars/{avatar_name}')
            im_tk = ImageTk.PhotoImage(im)
            avatars_dict.update({avatar_name: {'img_object': im_tk}})
        return avatars_dict

    def show_new_username_entry(self):
        self.username_entry.grid(row=1, column=1)
        self.save_username_btn.grid(row=1, column=2)

    def edit_username(self):
        new_name = self.username_entry.get()
        self.username_entry.delete(0, 'end')
        self.current_user.edit_username(new_name)
        self.username.configure(text=new_name)
        self.username_entry.grid_forget()
        self.save_username_btn.grid_forget()

    def update_strict_spelling(self):
        state = self.strict_spelling.get()
        self.current_user.toggle_strict_spelling(state)
