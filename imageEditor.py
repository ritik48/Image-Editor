import time
import tkinter as tk
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import PIL
import imagehash
from PIL import ImageDraw
from PIL import ImageEnhance
from PIL import ImageFilter

import os
from PIL import ImageOps


class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        # code for the splash screen
        self.wm_overrideredirect(1)
        self.configure(background="black")

        window_width, window_height = 500, 320
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()

        x_co = int(screen_width / 2 - window_width / 2)
        y_co = int(screen_height / 2 - window_height / 2) - 50



        self.loading_label = None

        self.geometry(f"{window_width}x{window_height}+{x_co}+{y_co}")

        self.splash_frame = tk.Frame(self, background="black")
        self.splash_frame.pack(fill="both", expand=True)

        self.image_editor_window = tk.Frame(self)

        wallpaper = Image.open('images_ie/splash_screen_ie.jpg')
        wallpaper = wallpaper.resize((window_width, window_height - 30), Image.ANTIALIAS)
        wallpaper = ImageTk.PhotoImage(wallpaper)

        self.loading = Image.open('images_ie/loader_ie.png')
        self.loading = self.loading.resize((19, 19), Image.ANTIALIAS)
        self.loading = ImageTk.PhotoImage(self.loading)

        self.wallpaper_label = tk.Label(self, image=wallpaper, bd=0)
        self.wallpaper_label.place(x=0, y=0)

        self.delay = 50

        self.developer_label = tk.Label(self, text='Developed by Ritik', foreground="white",
                                        font="lucida 10 bold", background='#1e2329')
        self.developer_label.place(x=350, y=260)

        self.x = 8

        # code for the image editor

        self.button_background = 'grey'
        self.original_image_resized = None
        self.image_copy_resized = None
        self.modified_img_resized = None
        self.image_before_draw = None
        self.draw_active = False
        self.crop_active = False
        self.mirrored = False
        self.current_index = None
        self.image_paths = []
        self.lines_drawn = []
        self.current_image_size = None
        self.current_resized_image_size = None
        self.original_image = None
        self.modified_img = None
        self.image_copy = None
        self.rect = None
        self.event_x = self.event_y = None  # to store the bottom right corner's coordinates(for cropping)
        self.rectangles = []
        self.point_x = self.point_y = None
        self.image_x_co = self.image_y_co = None
        self.original_hash = None

        self.max_height = 812
        self.max_width = 1220

        self.degree = 90
        self.error = None

        flip_icon = Image.open('images_ie/flip2_ie.png')
        flip_icon = flip_icon.resize((25, 25), Image.ANTIALIAS)
        flip_icon = ImageTk.PhotoImage(flip_icon)

        rotate_icon = Image.open('images_ie/rotate_ie.png')
        rotate_icon = rotate_icon.resize((25, 25), Image.ANTIALIAS)
        rotate_icon = ImageTk.PhotoImage(rotate_icon)

        next_icon = Image.open('images_ie/right_ie.png')
        next_icon = next_icon.resize((25, 25), Image.ANTIALIAS)
        next_icon = ImageTk.PhotoImage(next_icon)

        previous_icon = Image.open('images_ie/left_ie.png')
        previous_icon = previous_icon.resize((25, 25), Image.ANTIALIAS)
        previous_icon = ImageTk.PhotoImage(previous_icon)

        adjust_icon = Image.open('images_ie/adjust_ie.png')
        adjust_icon = adjust_icon.resize((25, 25), Image.ANTIALIAS)
        adjust_icon = ImageTk.PhotoImage(adjust_icon)

        filter_icon = Image.open('images_ie/filter_ie.png')
        filter_icon = filter_icon.resize((25, 25), Image.ANTIALIAS)
        filter_icon = ImageTk.PhotoImage(filter_icon)

        save_icon = Image.open('images_ie/save_ie.png')
        save_icon = save_icon.resize((25, 25), Image.ANTIALIAS)
        save_icon = ImageTk.PhotoImage(save_icon)

        delete_icon = Image.open('images_ie/delete_ie.png')
        delete_icon = delete_icon.resize((25, 25), Image.ANTIALIAS)
        delete_icon = ImageTk.PhotoImage(delete_icon)

        power_off_icon = Image.open('images_ie/power-button_ie.png')
        power_off_icon = power_off_icon.resize((25, 25), Image.ANTIALIAS)
        power_off_icon = ImageTk.PhotoImage(power_off_icon)

        self.error_icon = Image.open('images_ie/error_ie.png')
        self.error_icon = self.error_icon.resize((50, 50), Image.ANTIALIAS)
        self.error_icon = ImageTk.PhotoImage(self.error_icon)

        self.open_image_icon = Image.open('images_ie/open_image_ie.png')
        self.open_image_icon = self.open_image_icon.resize((150, 120), Image.ANTIALIAS)
        self.open_image_icon = ImageTk.PhotoImage(self.open_image_icon)

        self.open_image_small_icon = Image.open('images_ie/open_image_ie.png')
        self.open_image_small_icon = self.open_image_small_icon.resize((50, 40), Image.ANTIALIAS)
        self.open_image_small_icon = ImageTk.PhotoImage(self.open_image_small_icon)

        self.checked_icon = Image.open('images_ie/checked_ie.png')
        self.checked_icon = self.checked_icon.resize((25, 25), Image.ANTIALIAS)
        self.checked_icon = ImageTk.PhotoImage(self.checked_icon)

        self.unchecked_icon = Image.open('images_ie/unchecked_ie.png')
        self.unchecked_icon = self.unchecked_icon.resize((25, 25), Image.ANTIALIAS)
        self.unchecked_icon = ImageTk.PhotoImage(self.unchecked_icon)

        reset_icon = Image.open('images_ie/reset_ie.png')
        reset_icon = reset_icon.resize((25, 25), Image.ANTIALIAS)
        reset_icon = ImageTk.PhotoImage(reset_icon)

        color_picker_icon = Image.open('images_ie/color_picker_ie.png')
        color_picker_icon = color_picker_icon.resize((25, 25), Image.ANTIALIAS)
        color_picker_icon = ImageTk.PhotoImage(color_picker_icon)

        heading = tk.Label(self.image_editor_window, text="Image Editor", background="sky blue", font="lucida 9 bold")
        heading.pack(fill="x")

        self.image_canvas = tk.Canvas(self.image_editor_window, bd=0, highlightbackground="black", background="black")
        self.image_canvas.bind('<B1-Motion>', self.draw_crop)
        self.image_canvas.bind('<ButtonPress-1>', self.get_mouse_pos)
        self.image_canvas.bind('<ButtonRelease-1>', self.button_release)
        self.image_canvas.pack(fill="both", expand=True)

        self.button_frame_color = "#333331"

        self.button_frame2 = tk.Frame(self.image_editor_window, background=self.button_frame_color)
        self.button_frame2.pack(fill="x")

        self.button_frame = tk.Frame(self.button_frame2, background=self.button_frame_color)
        self.button_frame.pack()

        previous_b = tk.Button(self.button_frame, text="Previous", image=previous_icon,
                               background=self.button_frame_color, command=self.previous_image,
                               padx=5, bd=0, cursor="hand2")
        previous_b.bind("<Enter>", lambda e: mouse_hover(previous_b, color='#1c1c1b'))
        previous_b.bind("<Leave>", lambda e: mouse_not_hover(previous_b, color=self.button_frame_color))
        previous_b.pack(side="left", padx=2)

        rotate_b = tk.Button(self.button_frame, text="Rotate", image=rotate_icon, background=self.button_frame_color,
                             command=self.rotate, padx=5, bd=0, cursor="hand2")
        rotate_b.bind("<Enter>", lambda e: mouse_hover(rotate_b, color='#1c1c1b'))
        rotate_b.bind("<Leave>", lambda e: mouse_not_hover(rotate_b, color=self.button_frame_color))
        rotate_b.pack(side="left", padx=10)

        flip_b = tk.Button(self.button_frame, text="Flip", background=self.button_frame_color,
                           image=flip_icon, command=self.mirror, padx=5, bd=0, cursor="hand2")
        flip_b.bind("<Enter>", lambda e: mouse_hover(flip_b, color='#1c1c1b'))
        flip_b.bind("<Leave>", lambda e: mouse_not_hover(flip_b, color=self.button_frame_color))
        flip_b.pack(side="left", padx=10)

        self.delete_b = tk.Button(self.button_frame, text="Flip", background=self.button_frame_color, image=delete_icon,
                                  command=self.delete,
                                  padx=5, bd=0, cursor="hand2", state="disable")
        self.delete_b.bind("<Enter>", lambda e: mouse_hover(self.delete_b, color='#1c1c1b'))
        self.delete_b.bind("<Leave>", lambda e: mouse_not_hover(self.delete_b, color=self.button_frame_color))
        self.delete_b.pack(side="left", padx=10)

        next_b = tk.Button(self.button_frame, text="Next", image=next_icon, command=self.next_image,
                           background=self.button_frame_color, padx=5, bd=0, cursor="hand2")
        next_b.bind("<Enter>", lambda e: mouse_hover(next_b, color='#1c1c1b'))
        next_b.bind("<Leave>", lambda e: mouse_not_hover(next_b, color=self.button_frame_color))
        next_b.pack(side="left", padx=2)

        exit_window = tk.Button(self.image_editor_window, image=power_off_icon, compound="left",
                                text="Exit", font="lucida 9 bold", foreground='white', background="black",
                                command=self.exit_window, padx=12, cursor="hand2")
        exit_window.bind("<Enter>", lambda e: mouse_hover(exit_window))
        exit_window.bind("<Leave>", lambda e: mouse_not_hover(exit_window))
        exit_window.place(x=1418, y=640)

        self.side_frame = tk.Frame(self.image_editor_window, background="black")

        adjust_b = tk.Button(self.side_frame, text="Adjust", foreground="white", compound="left", font="lucida 9 bold",
                             image=adjust_icon, background="black", cursor="hand2",
                             command=self.open_adjustment_window, padx=5)
        adjust_b.bind("<Enter>", lambda e: mouse_hover(adjust_b))
        adjust_b.bind("<Leave>", lambda e: mouse_not_hover(adjust_b))
        adjust_b.pack(pady=2)

        filter_b = tk.Button(self.side_frame, text="Filters", foreground="white", compound="left",
                             font="lucida 9 bold", image=filter_icon, background="black", cursor="hand2",
                             command=self.open_filter_window, padx=5)
        filter_b.bind("<Enter>", lambda e: mouse_hover(filter_b))
        filter_b.bind("<Leave>", lambda e: mouse_not_hover(filter_b))
        filter_b.pack(pady=2)

        self.reset_b = tk.Button(self.image_editor_window, text="Reset", foreground="white", compound="left",
                                 font="lucida 9 bold", image=reset_icon, background="black",
                                 command=self.reset, padx=6, cursor="hand2")
        self.reset_b.bind("<Enter>", lambda e: mouse_hover(self.reset_b))
        self.reset_b.bind("<Leave>", lambda e: mouse_not_hover(self.reset_b))

        self.draw_b = tk.Button(self.image_editor_window, text="Draw", image=self.unchecked_icon, foreground="white",
                                font="lucida 9 bold", compound="left", background="black", command=self.activate_draw,
                                padx=3, cursor="hand2")
        self.draw_b.bind("<Enter>", lambda e: mouse_hover(self.draw_b))
        self.draw_b.bind("<Leave>", lambda e: mouse_not_hover(self.draw_b))

        self.crop_b = tk.Button(self.image_editor_window, text="Crop", image=self.unchecked_icon, foreground="white",
                                font="lucida 9 bold", compound="left", background="black",
                                command=self.activate_crop, padx=4, cursor="hand2")
        self.crop_b.bind("<Enter>", lambda e: mouse_hover(self.crop_b))
        self.crop_b.bind("<Leave>", lambda e: mouse_not_hover(self.crop_b))

        self.crop_save = tk.Button(self.image_editor_window, image=save_icon, compound='left', text="Save",
                                   foreground="white", font="lucida 9 bold", background="black",
                                   command=self.crop_image, padx=4, cursor="hand2")
        self.crop_save.bind("<Enter>", lambda e: mouse_hover(self.crop_save))
        self.crop_save.bind("<Leave>", lambda e: mouse_not_hover(self.crop_save))

        self.save_b = tk.Button(self.image_editor_window, text="Save", foreground="white", compound="left",
                                font="lucida 9 bold", state='disabled', image=save_icon, background="black",
                                command=self.save, padx=10, cursor="hand2")

        self.draw_save = tk.Button(self.image_editor_window, image=save_icon, compound='left', text="Save",
                                   foreground="white", font="lucida 10 bold", background="black",
                                   command=self.image_after_draw, padx=3, cursor="hand2")
        self.draw_save.bind("<Enter>", lambda e: mouse_hover(self.draw_save))
        self.draw_save.bind("<Leave>", lambda e: mouse_not_hover(self.draw_save))

        version_label = tk.Label(self.button_frame2,text="v 1.0", background=self.button_frame_color,
                                   foreground="white", font="lucida 9 bold")
        version_label.place(x=20)

        self.status_bar = tk.Label(self.button_frame2, background=self.button_frame_color,
                                   foreground="white", font="lucida 10 bold")
        self.status_bar.place(x=1200)

        self.open_image_button = tk.Button(self.image_editor_window, command=self.open_image, cursor="hand2",
                                           image=self.open_image_icon, compound='top', text="Click To Open Image",
                                           font="lucida 12 bold", foreground="white", bd=0, background="black",)
        self.open_image_button.bind("<Enter>", lambda e: mouse_hover(self.open_image_button, color='#1c1c1b'))
        self.open_image_button.bind("<Leave>", lambda e: mouse_not_hover(self.open_image_button))
        self.open_image_button.place(x=685, y=350)

        self.error_b = tk.Button(self.image_editor_window, text="It appears that we don't support this file format.",
                                 image=self.error_icon, compound="left", font="lucida 11 bold",
                                 background="black", foreground="white", bd=0, padx=5)

        self.pencil_size = 2
        self.pencil_color = 'red'

        self.pencil_size_label = tk.Label(self.image_editor_window, text="Size", font="lucida 10 bold",
                                          background='black', foreground="white")

        self.pencil_size_scale = tk.Scale(self.image_editor_window, from_=1, to=15, sliderrelief='flat',
                                          orient="horizontal", fg='white', highlightthickness=0,
                                          command=self.change_pencil_size, cursor="hand2", background='black',
                                          troughcolor='#73B5FA', activebackground='#1065BF')

        self.color_chooser_button = tk.Button(self.image_editor_window, image=color_picker_icon, text="Color",
                                              font="lucida 10 bold", cursor="hand2", background='black',
                                              foreground="white", bd=0, command=self.choose_color)
        self.color_chooser_button.bind("<Enter>", lambda e: mouse_hover(self.color_chooser_button))
        self.color_chooser_button.bind("<Leave>", lambda e: mouse_not_hover(self.color_chooser_button))

        self.img2 = None
        self.start_time = time.time()

        self.show_splash_screen()
        self.mainloop()

    def show_splash_screen(self):
        self.loading_label = tk.Label(self.splash_frame, image=self.loading, bd=0)
        self.loading_label.place(x=self.x, y=294)
        self.x += 22
        if self.x != 470:
            self.after(self.delay, self.show_splash_screen)
        else:
            self.developer_label.destroy()
            self.splash_frame.destroy()
            self.loading_label.destroy()
            self.wallpaper_label.destroy()
            self.wm_overrideredirect(0)

            self.image_editor_window.pack(fill="both", expand=True)
            self.wm_attributes('-fullscreen', True)

    def change_pencil_size(self, size):
        self.pencil_size = int(size)

    def choose_color(self):
        color = colorchooser.askcolor(initialcolor='red')
        if color[0]:
            self.pencil_color = color[1]

    def open_image(self):
        file_object = filedialog.askopenfile(filetype=(('jpg', '*.jpg'), ('png', '*.png')))
        if file_object:

            self.open_image_button.configure(image=self.open_image_small_icon, text="Open Image", compound="left",
                                             font="lucida 9 bold")
            self.open_image_button.place(x=1407, y=720)

            self.side_frame.place(x=1418, y=114)
            self.save_b.place(x=1418, y=680)
            self.draw_b.place(x=1465, y=232)
            self.crop_b.place(x=1390, y=232)
            self.reset_b.place(x=1418, y=190)

            self.delete_b.configure(state="normal")

            filename = file_object.name
            directory = filename.replace(os.path.basename(filename), "")
            files_list = os.listdir(directory)

            self.image_paths = []
            for file in files_list:
                if '.jpg' in file or '.png' in file or '.JPG' in file or '.JPEG' in file or '.PNG' in file:
                    self.image_paths.append(os.path.join(directory, file))

            for i, image in enumerate(self.image_paths):
                if image == filename:
                    self.current_index = i
            self.show_image(image=self.image_paths[self.current_index])

    def resize_image(self, image):
        image.thumbnail((self.max_width, self.max_height))

        self.original_hash = imagehash.average_hash(image)

        self.current_resized_image_size = (image.size[0], image.size[1])
        return image

    def photo_image_object(self, image):
        self.original_image = Image.open(image)
        self.current_image_size = self.original_image.size
        self.modified_img = self.original_image
        self.image_copy = self.original_image

        self.original_image_resized = Image.open(image)

        self.modified_img_resized = self.original_image_resized
        self.image_copy_resized = self.original_image_resized

        im = self.resize_image(self.original_image_resized)
        im = ImageTk.PhotoImage(im)
        return im

    def show_image(self, image=None, modified=None):
        self.status_bar.configure(text=f"Image  :  {self.current_index + 1}  of  {len(self.image_paths)}")
        if self.error:
            self.error_b.place_forget()
            self.error = None

        im = None
        if image:
            try:
                im = self.photo_image_object(image)
            except:
                self.image_copy = self.modified_img = self.original_image_resized = self.original_image = None
                self.image_canvas.image = ''
                self.error_b.place(x=600, y=380)
                self.error = True
                return

        elif modified:
            im = modified

        image_width, image_height = self.current_resized_image_size[0], self.current_resized_image_size[1]
        self.image_x_co, self.image_y_co = (self.winfo_screenwidth() / 2) - image_width / 2, (
                self.max_height / 2) - image_height / 2
        self.image_canvas.image = im

        if image_height < self.max_height:
            self.image_canvas.create_image(self.image_x_co, self.image_y_co, image=im, anchor="nw")
        else:
            self.image_canvas.create_image(self.image_x_co, 0, image=im, anchor="nw")

    def previous_image(self):
        if self.image_paths:
            self.save_b.configure(state="disable")

            if self.current_index != 0:
                self.current_index -= 1
            self.show_image(image=self.image_paths[self.current_index])

            self.delete_b.configure(state="normal")

    def next_image(self):
        if self.image_paths:
            self.save_b.configure(state="disable")

            if self.current_index != len(self.image_paths) - 1:
                self.current_index += 1
            self.show_image(image=self.image_paths[self.current_index])

            self.delete_b.configure(state="normal")

    def rotate(self):
        if self.original_image and not self.error:
            self.modified_img_resized = self.image_copy_resized.rotate(-self.degree, expand=True)
            self.image_copy_resized = self.modified_img_resized

            self.modified_img = self.image_copy.rotate(-self.degree, expand=True)

            self.image_copy = self.modified_img
            self.image_copy_resized = self.modified_img_resized

            self.compare_images()

            self.current_resized_image_size = self.modified_img_resized.size

            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.show_image(modified=im)

    def mirror(self):
        if self.original_image and not self.error:
            if not self.mirrored:
                self.modified_img = self.image_copy.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.modified_img_resized = self.image_copy_resized.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.mirrored = True
            else:
                self.modified_img = self.modified_img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.modified_img_resized = self.modified_img_resized.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.mirrored = False

            self.image_copy = self.modified_img
            self.image_copy_resized = self.modified_img_resized

            self.compare_images()

            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.show_image(modified=im)

    def get_mouse_pos(self, event):
        if not self.draw_active and self.crop_active:
            if self.rect:
                self.rectangles = []
                self.image_canvas.delete(self.rect)

            self.rect = self.image_canvas.create_rectangle(0, 0, 0, 0, outline="black", width=3)

        self.point_x, self.point_y = event.x, event.y

    def button_release(self, event):
        if self.crop_active:
            self.crop_save.place(x=1464, y=232)

    def activate_draw(self):
        if self.original_image and not self.error:
            if not self.draw_active:

                # if we write self.image_before_draw = self.image_copy , then drawing on self.image_before_draw changes
                # self.image_copy too therefore create a new image and paste image_copy on it
                self.image_before_draw = Image.new('RGB', size=self.current_image_size)
                self.image_before_draw.paste(self.image_copy, (0, 0))

                self.pencil_size_label.place(x=1388, y=282)
                self.pencil_size_scale.place(x=1425, y=267)
                self.color_chooser_button.place(x=1450, y=312)

                self.image_canvas.configure(cursor='pencil')
                self.draw_save.place(x=1390, y=232)

                self.draw_b.configure(image=self.checked_icon)
                self.open_image_button.place_forget()
                self.button_frame.pack_forget()
                self.side_frame.place_forget()
                self.crop_b.place_forget()
                self.save_b.place_forget()

                print("draw activated..")
                self.draw_active = True
            else:
                if self.lines_drawn:
                    for line in self.lines_drawn:
                        self.image_canvas.delete(line)
                    self.lines_drawn = []
                    self.image_before_draw = None
                    self.image_before_draw = self.image_copy

                self.image_canvas.configure(cursor='arrow')
                self.draw_b.configure(image=self.unchecked_icon)
                print("draw deactivated..")
                self.draw_active = False
                self.button_frame.pack()

                self.side_frame.place(x=1418, y=114)
                self.save_b.place(x=1418, y=680)
                self.crop_b.place(x=1390, y=232)
                self.open_image_button.place(x=1407, y=720)

                self.pencil_size_label.place_forget()
                self.pencil_size_scale.place_forget()
                self.color_chooser_button.place_forget()
                self.draw_save.place_forget()

    def activate_crop(self):
        if self.original_image and not self.error:

            # to deactivate draw when we switch from draw to crop as we don't want both to be active at the same time
            if self.draw_active:
                self.activate_draw()

            if not self.crop_active:
                self.crop_b.configure(image=self.checked_icon)
                self.image_canvas.configure(cursor='plus')
                self.crop_active = True
                self.reset_b.place_forget()
                self.button_frame.pack_forget()
                self.side_frame.place_forget()
                self.draw_b.place_forget()
                self.save_b.place_forget()

            else:
                self.image_canvas.configure(cursor='arrow')
                self.crop_b.configure(image=self.unchecked_icon)
                self.crop_save.place_forget()
                if self.rect:
                    self.image_canvas.delete(self.rect)

                self.crop_active = False
                self.side_frame.place(x=1418, y=114)
                self.save_b.place(x=1418, y=680)
                self.draw_b.place(x=1465, y=232)
                self.crop_b.place(x=1390, y=232)
                self.reset_b.place(x=1418, y=190)
                self.button_frame.pack()

    def draw_crop(self, event):
        if self.crop_active:
            if not self.rectangles:
                self.rectangles.append(self.rect)

            image_width, image_height = self.current_resized_image_size[0], self.current_resized_image_size[1]
            x_co_1, x_co_2 = int((self.winfo_screenwidth() / 2) - image_width / 2), int(
                (self.winfo_screenwidth() / 2) + image_width / 2)
            y_co_1, y_co_2 = int(self.max_height / 2 - image_height / 2), int((self.max_height / 2) + image_height / 2)

            if x_co_2 > event.x > x_co_1 and y_co_1 + 2 < event.y < y_co_2:
                self.image_canvas.coords(self.rect, self.point_x, self.point_y, event.x, event.y)

                self.event_x, self.event_y = event.x, event.y

        elif self.draw_active:
            image_width, image_height = self.current_resized_image_size[0], self.current_resized_image_size[1]
            x_co_1, x_co_2 = int((self.winfo_screenwidth() / 2) - image_width / 2), int(
                (self.winfo_screenwidth() / 2) + image_width / 2)
            y_co_1, y_co_2 = int(self.max_height / 2 - image_height / 2), int((self.max_height / 2) + image_height / 2)

            if x_co_2 > self.point_x > x_co_1 and y_co_1 < self.point_y < y_co_2:
                if x_co_2 > event.x > x_co_1 and y_co_1 < event.y < y_co_2:
                    lines = self.image_canvas.create_line(self.point_x, self.point_y, event.x, event.y,
                                                          fill=self.pencil_color, width=self.pencil_size)

                    # create line image and calculating x ,y coordinates as per original image size since
                    # here self.point_x - self.image_x_co and all are with respect to the resized image
                    x_co_1, y_co_1, x_co_2, y_co2 = ((self.point_x - self.image_x_co) * self.current_image_size[0])/self.current_resized_image_size[0], ((self.point_y - self.image_y_co)*self.current_image_size[1])/self.current_resized_image_size[1], ((event.x - self.image_x_co)*self.current_image_size[0])/self.current_resized_image_size[0], ((event.y - self.image_y_co)*self.current_image_size[1])/self.current_resized_image_size[1]

                    img = ImageDraw.Draw(self.image_before_draw)
                    img.line([(x_co_1, y_co_1), (x_co_2, y_co2)], fill=self.pencil_color, width=self.pencil_size + 1)

                    self.lines_drawn.append(lines)
                    self.point_x, self.point_y = event.x, event.y

    def crop_image(self):
        if self.rectangles:
            x_co_1, y_co_1, x_co_2, y_co2 = ((self.point_x - self.image_x_co) * self.current_image_size[0])/self.current_resized_image_size[0], ((self.point_y - self.image_y_co) * self.current_image_size[1]) / self.current_resized_image_size[1], ((self.event_x - self.image_x_co) * self.current_image_size[0]) / self.current_resized_image_size[0], ((self.event_y - self.image_y_co) * self.current_image_size[1]) / self.current_resized_image_size[1]

            self.image_copy = self.image_copy.crop((int(x_co_1), int(y_co_1), int(x_co_2), int(y_co2)))
            x_co_1, y_co_1, x_co_2, y_co2 = self.point_x - self.image_x_co, self.point_y - self.image_y_co, self.event_x - self.image_x_co, self.event_y - self.image_y_co

            self.save()
        else:
            messagebox.showinfo(title="Can't crop !", message="Please select the portion of the image,"
                                                              " you want to crop")

    def image_after_draw(self):
        if self.lines_drawn:
            self.image_copy = self.image_before_draw
            self.save()
        else:
            messagebox.showinfo(title='Cannot save!', message='You have not drawn anything on the image.')

    def save(self):
        image_path_object = filedialog.asksaveasfile(defaultextension='.jpg')

        if image_path_object:
            image_path = image_path_object.name
            if self.draw_active:
                for line in self.lines_drawn:
                    self.image_canvas.delete(line)
                self.lines_drawn = []

                # as crop is still active after cropping the image so on calling activate_crop, it will get deactivated
                self.activate_draw()

            if self.crop_active:
                self.image_canvas.delete(self.rect)

                # as crop is still active after cropping the image so on calling activate_crop, it will get deactivated
                self.activate_crop()

            self.image_copy.save(image_path)
            self.image_paths.insert(self.current_index + 1, image_path)
            self.current_index += 1
            self.show_image(image=image_path)

        self.delete_b.configure(state="normal")
        self.save_b.configure(state="disable")

    def reset(self):
        if self.original_image and not self.error:
            if self.draw_active:
                for line in self.lines_drawn:
                    self.image_canvas.delete(line)
                    self.lines_drawn = []
                self.image_before_draw = self.image_copy
            else:
                current_original_image = self.image_paths[self.current_index]
                self.show_image(image=current_original_image)

            self.delete_b.configure(state="normal")
            self.save_b.configure(state="disable")

    def open_adjustment_window(self):
        if self.original_image and not self.error:
            self.delete_b.configure(state="disable")
            Adjustments(self, self.image_copy, self.modified_img, self.image_copy_resized, self.modified_img_resized)

    def open_filter_window(self):
        if self.original_image and not self.error:
            self.delete_b.configure(state="disable")
            Filters(self, self.image_copy, self.modified_img, self.image_copy_resized, self.modified_img_resized)

    def delete(self):
        if self.image_paths:
            import winshell
            self.original_image.close()
            winshell.delete_file(self.image_paths[self.current_index])
            print(len(self.image_paths), self.current_index)

            print(len(self.image_paths), self.current_index)
            if len(self.image_paths) - 1 == self.current_index:
                self.image_paths.remove(self.image_paths[self.current_index])
                self.current_index = 0
            else:
                self.image_paths.remove(self.image_paths[self.current_index])

            if self.image_paths:

                self.show_image(image=self.image_paths[self.current_index])
            else:
                self.status_bar.configure(text="")
                self.image_canvas.image = ''

                self.open_image_button.configure(image=self.open_image_icon, command=self.open_image,
                                                 text="Click To Open Image", font="lucida 12 bold")
                self.open_image_button.place(x=685, y=350)

                if self.error:
                    self.error_b.place_forget()
                    self.error = None

    def compare_images(self):
        if self.original_hash != imagehash.average_hash(self.image_copy_resized):
            self.save_b.configure(state="normal")
        else:
            self.save_b.configure(state='disable')

    def exit_window(self):
        self.destroy()


def mouse_not_hover(button, color=None):
    if not color:
        color = 'black'
    button.configure(bg=color)


def mouse_hover(button, color=None):
    if not color:
        color = '#473f3f'
    button.configure(bg=color)


class Adjustments(tk.Toplevel):
    def __init__(self, parent, image_copy, modified_img, image_copy_resized, modified_img_resized):
        super().__init__(parent)

        self.parent = parent
        self.configure(background="grey")
        self.wm_overrideredirect(True)
        self.grab_set()
        self.winfo_parent()
        self.geometry("260x280+1200+100")

        self.image_copy = image_copy
        self.modified_img = modified_img

        self.image_copy_resized = image_copy_resized
        self.modified_img_resized = modified_img_resized

        self.modifications = {'contrast': 1.0, 'sharpness': 1.0, 'brightness': 1.0}

        background_color1 = '#19191a'
        background_color2 = 'black'

        f1 = tk.Frame(self, background=background_color1)
        f1.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Label(f1, text="Adjustments", background="black", foreground="white").pack(fill="x")

        contrast_l = tk.Label(f1, text="Contrast", relief="solid", font="lucida 11 bold", background=background_color2,
                              foreground="red")
        contrast_l.place(x=15, y=60)

        self.contrast_b = tk.Scale(f1, from_=0, to=20, sliderrelief='flat',
                                   command=lambda e: self.adjust(e, 'contrast'),
                                   orient="horizontal", highlightthickness=0, background=background_color1, fg='white',
                                   troughcolor='#73B5FA', activebackground='#1065BF')
        self.contrast_b.place(x=120, y=40)

        sharpness_l = tk.Label(f1, text="Sharpness", font="lucida 11 bold", background=background_color2,
                               foreground="red")
        sharpness_l.place(x=15, y=100)

        self.sharpness_b = tk.Scale(f1, from_=0, to=30, sliderrelief='flat',
                                    command=lambda e: self.adjust(e, 'sharpness'),
                                    orient="horizontal", highlightthickness=0, background=background_color1, fg='white',
                                    troughcolor='#73B5FA', activebackground='#1065BF')
        self.sharpness_b.place(x=120, y=80)
        #
        brightness_l = tk.Label(f1, text="Brightness", font="lucida 11 bold", background=background_color2,
                                foreground="red")
        brightness_l.place(x=15, y=140)

        self.brightness_b = tk.Scale(f1, from_=0, to=20, sliderrelief='flat',
                                     command=lambda e: self.adjust(e, 'brightness'),
                                     orient="horizontal", highlightthickness=0, background=background_color1,
                                     fg='white',
                                     troughcolor='#73B5FA', activebackground='#1065BF')
        self.brightness_b.place(x=120, y=120)

        cancel_b = tk.Button(f1, text="Cancel", command=self.cancel, relief="solid", background=background_color1,
                             foreground="red", font="lucida 12 bold", cursor="hand2")
        cancel_b.bind("<Enter>", lambda e: mouse_hover(cancel_b))
        cancel_b.bind("<Leave>", lambda e: mouse_not_hover(cancel_b))
        cancel_b.place(x=45, y=220)

        apply_b = tk.Button(f1, text="Apply", command=self.apply, relief="solid", background=background_color1,
                            foreground="red",
                            font="lucida 12 bold", padx=8, cursor="hand2")
        apply_b.bind("<Enter>", lambda e: mouse_hover(apply_b))
        apply_b.bind("<Leave>", lambda e: mouse_not_hover(apply_b))
        apply_b.place(x=130, y=220)

    def adjust(self, e, changes):
        im2 = self.image_copy
        im2_resized = self.image_copy_resized

        if 'original_image':
            if self.modifications:
                for modification in self.modifications.copy():

                    if changes == 'sharpness' and modification == 'sharpness':
                        del self.modifications[modification]

                    elif changes == 'contrast' and modification == 'contrast':
                        del self.modifications[modification]

                    elif changes == 'brightness' and modification == 'brightness':
                        del self.modifications[modification]

                    else:
                        property_ = modification
                        value = self.modifications[property_]

                        if property_ == 'sharpness':

                            enhancer = ImageEnhance.Sharpness(im2)
                            self.modified_img = enhancer.enhance(value)

                            enhancer = ImageEnhance.Sharpness(im2_resized)
                            self.modified_img_resized = enhancer.enhance(value)

                            im = ImageTk.PhotoImage(self.modified_img_resized)
                            self.parent.show_image(modified=im)

                            im2 = self.modified_img
                            im2_resized = self.modified_img_resized

                        elif property_ == 'contrast':

                            enhancer = ImageEnhance.Contrast(im2)
                            self.modified_img = enhancer.enhance(value)

                            enhancer = ImageEnhance.Contrast(im2_resized)
                            self.modified_img_resized = enhancer.enhance(value)

                            im = ImageTk.PhotoImage(self.modified_img_resized)
                            self.parent.show_image(modified=im)

                            im2 = self.modified_img
                            im2_resized = self.modified_img_resized

                        elif property_ == 'brightness':

                            enhancer = ImageEnhance.Brightness(im2)
                            self.modified_img = enhancer.enhance(value)

                            enhancer = ImageEnhance.Brightness(im2_resized)
                            self.modified_img_resized = enhancer.enhance(value)

                            im = ImageTk.PhotoImage(self.modified_img_resized)
                            self.parent.show_image(modified=im)

                            im2 = self.modified_img
                            im2_resized = self.modified_img_resized

                if changes == 'sharpness':
                    self.modifications['sharpness'] = int(e) / 10

                    enhancer = ImageEnhance.Sharpness(self.modified_img)
                    self.modified_img = enhancer.enhance(int(e) / 10)

                    enhancer = ImageEnhance.Sharpness(self.modified_img_resized)
                    self.modified_img_resized = enhancer.enhance(int(e) / 10)

                    im = ImageTk.PhotoImage(self.modified_img_resized)
                    self.parent.show_image(modified=im)

                elif changes == 'contrast':
                    self.modifications['contrast'] = int(e) / 10

                    enhancer = ImageEnhance.Contrast(self.modified_img)
                    self.modified_img = enhancer.enhance(int(e) / 10)

                    enhancer = ImageEnhance.Contrast(self.modified_img_resized)
                    self.modified_img_resized = enhancer.enhance(int(e) / 10)

                    im = ImageTk.PhotoImage(self.modified_img_resized)
                    self.parent.show_image(modified=im)

                elif changes == 'brightness':
                    self.modifications['brightness'] = int(e) / 10

                    enhancer = ImageEnhance.Brightness(self.modified_img)
                    self.modified_img = enhancer.enhance(int(e) / 10)

                    enhancer = ImageEnhance.Brightness(self.modified_img_resized)
                    self.modified_img_resized = enhancer.enhance(int(e) / 10)

                    im = ImageTk.PhotoImage(self.modified_img_resized)
                    self.parent.show_image(modified=im)

    def cancel(self):
        self.grab_release()

        im = ImageTk.PhotoImage(self.image_copy_resized)
        self.parent.show_image(modified=im)
        self.destroy()

    def apply(self):
        self.modifications = {'contrast': 1.0, 'sharpness': 1.0, 'brightness': 1.0}
        self.grab_release()

        for i in (self.brightness_b, self.contrast_b, self.sharpness_b):
            if i.get() != 10:
                self.parent.save_b.configure(state="normal")
                break

        self.parent.image_copy = self.modified_img
        self.parent.image_copy_resized = self.modified_img_resized

        im = ImageTk.PhotoImage(self.parent.image_copy_resized)
        self.parent.show_image(modified=im)
        self.destroy()


class Filters(tk.Toplevel):
    def __init__(self, parent, image_copy, modified_img, image_copy_resized, modified_img_resized):
        super().__init__(parent)

        self.configure(background="grey")
        self.wm_overrideredirect(True)
        self.grab_set()
        self.winfo_parent()
        self.geometry("150x250+1328+100")
        self.filter_ = None

        self.parent = parent

        self.image_copy = image_copy
        self.modified_img = modified_img

        self.image_copy_resized = image_copy_resized
        self.modified_img_resized = modified_img_resized

        background_color1 = '#19191a'
        foreground_color = 'sky blue'

        f1 = tk.Frame(self, background=background_color1)
        f1.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Label(f1, text="Filters", background="black", foreground="#ba5a14", font="lucida 11 bold").pack(fill="x")

        filters_frame = tk.Frame(f1, background=background_color1)
        filters_frame.pack(fill="both", expand=True)

        buttons_frame = tk.Frame(f1, background="black", pady=0)
        buttons_frame.pack(fill="both", expand=True)

        emboss_b = tk.Button(filters_frame, text="Emboss", font="lucida 8 bold", command=lambda: self.filters(emboss_b),
                             foreground=foreground_color, background="black", padx=17, cursor="hand2")
        emboss_b.bind("<Enter>", lambda e: mouse_hover(button=emboss_b))
        emboss_b.bind("<Leave>", lambda e: mouse_not_hover(button=emboss_b))
        emboss_b.pack(pady=9)

        grey_b = tk.Button(filters_frame, text="Grey", font="lucida 8 bold", command=lambda: self.filters(grey_b),
                           foreground=foreground_color, background="black", padx=8, cursor="hand2")
        grey_b.bind("<Enter>", lambda e: mouse_hover(button=grey_b))
        grey_b.bind("<Leave>", lambda e: mouse_not_hover(button=grey_b))
        grey_b.pack(pady=9)

        negative_b = tk.Button(filters_frame, text="Negative", font="lucida 8 bold",
                               command=lambda: self.filters(negative_b), foreground=foreground_color,
                               background="black", padx=17, cursor="hand2")
        negative_b.bind("<Enter>", lambda e: mouse_hover(button=negative_b))
        negative_b.bind("<Leave>", lambda e: mouse_not_hover(button=negative_b))
        negative_b.pack(pady=9)

        blur_b = tk.Button(filters_frame, text="Gaussian Blur", font="lucida 8 bold",
                           command=lambda: self.filters(blur_b), foreground=foreground_color,
                           background="black", padx=17, cursor="hand2")
        blur_b.bind("<Enter>", lambda e: mouse_hover(button=blur_b))
        blur_b.bind("<Leave>", lambda e: mouse_not_hover(button=blur_b))
        blur_b.pack(pady=9)

        cancel_b = tk.Button(f1, text="Cancel", command=self.cancel, background='black',
                             foreground=foreground_color, font="lucida 12 bold", cursor="hand2")
        cancel_b.bind("<Enter>", lambda e: mouse_hover(button=cancel_b))
        cancel_b.bind("<Leave>", lambda e: mouse_not_hover(button=cancel_b))
        cancel_b.pack(side="left")

        apply_b = tk.Button(f1, text="Apply", command=self.apply, background='black', foreground=foreground_color,
                            font="lucida 12 bold", padx=8, cursor="hand2")
        apply_b.bind("<Enter>", lambda e: mouse_hover(button=apply_b))
        apply_b.bind("<Leave>", lambda e: mouse_not_hover(button=apply_b))
        apply_b.pack(side="left")

    def filters(self, button):
        self.filter_ = button['text'].lower()

        if self.filter_ == 'emboss':
            self.modified_img = self.image_copy.filter(ImageFilter.EMBOSS)

            self.modified_img_resized = self.image_copy_resized.filter(ImageFilter.EMBOSS)
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

        elif self.filter_ == 'negative':
            self.modified_img = ImageOps.invert(self.image_copy)

            self.modified_img_resized = ImageOps.invert(self.image_copy_resized)
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

        elif self.filter_ == 'grey':
            self.modified_img = ImageOps.grayscale(self.image_copy)

            self.modified_img_resized = ImageOps.grayscale(self.image_copy_resized)
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

        elif self.filter_ == 'gaussian blur':
            self.modified_img = self.image_copy.filter(ImageFilter.GaussianBlur)

            self.modified_img_resized = self.image_copy_resized.filter(ImageFilter.GaussianBlur)
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

    def cancel(self):
        self.grab_release()

        im = ImageTk.PhotoImage(self.image_copy_resized)
        self.parent.show_image(modified=im)
        self.destroy()

    def apply(self):
        self.grab_release()

        self.parent.image_copy = self.modified_img

        self.parent.image_copy_resized = self.modified_img_resized
        if self.filter_:
            self.parent.save_b.configure(state="normal")

        im = ImageTk.PhotoImage(self.parent.image_copy_resized)
        self.parent.show_image(modified=im)
        self.destroy()


start = ImageEditor()
