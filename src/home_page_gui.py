import tkinter as tk
from PIL import Image, ImageTk

class HomePage(tk.Frame):

    app = None
    header_color = "#BFC2EF"
    body_color = "#D1D3EB"

    def __init__(self, app):
        super().__init__(
            app.root,
            width=app.screen_width,
            height=app.screen_height,
            )
        HomePage.app = app
        self.width = app.screen_width
        self.height = app.screen_height
        self.pack()
        self.main = None
        self.header = None
        self.body = None
        self.build_home_page()

    def build_home_page(self):
        self.build_header()
        self.build_body()

    def build_header(self):
        self.header = HomeWidgetHeader(master=self, height=int(self.height/5))
        self.header.pack()

    def build_body(self):
        self.body = HomeWidgetBody(master=self, height=int(4*self.height/5))
        self.body.pack()

    def build_program_manager(self):
        ...

    def build_program_description(self):
        ...


class HomeWidgetHeader(tk.Frame):

    def __init__(self, master, height):
        super().__init__(
            master=master,
            width=master.width,
            height=height,
            bg=HomePage.header_color,
            highlightbackground="black",
            highlightthickness=1,
        )
        self.master = master
        self.width = master.width
        self.height = height
        self.logo_image = ImageTk.PhotoImage(Image.open("..\img\logo.png").convert("RGBA"))
        self.set_logo()

    def set_logo(self):
        logo_label = tk.Label(self, image=self.logo_image)
        logo_label.pack()
        

class HomeWidgetBody(tk.Frame):

    def __init__(self, master, height):
        super().__init__(
            master=master,
            width=master.width,
            height=height,
        )
        self.master = master
        self.width = master.width
        self.height = height
        self.program_manager = None
        self.program_description = None
        self.build_body()
    

    def build_body(self):
        self.program_manager = ProgramMenu(self, int(3*self.width/10))
        self.program_manager.pack(side=tk.LEFT)
        self.program_description = ProgramDescription(self, int(7*self.width/10))
        self.program_description.pack(side=tk.LEFT)


class ProgramMenu(tk.Frame):

    color = f'#BFC2EF'

    def __init__(self, master, width):
        super().__init__(
            master=master,
            height=master.height,
            width=width,
            bg=HomePage.body_color,
        )
        self.width = width
        self.height = master.height
        self.new_graphic_project_button = None
        self.new_numeric_project_button = None
        self.pack_propagate(0)
        self.build_program_menu()

    def build_program_menu(self):
        self.widget = ProgramMenuWidget(self, int(self.width*0.8), int(self.height*0.8))
        self.widget.place(x=self.width/2, y=self.height/2.2, anchor=tk.CENTER)
        


class ProgramMenuWidget(tk.Frame):


    def __init__(self, master, width, height):
        super().__init__(
            master,
            width=width,
            height=height,
            bg=HomePage.body_color,
        )
        self.width = width
        self.height = height
        self.pack_propagate(0)
        self.graphic_sketch_example_img = tk.PhotoImage(file="..\img\graphic_sketch_example.png")
        self.numeric_sketch_example_img = tk.PhotoImage(file=r"..\img\numeric_sketch_example.png")
        self.graphic_sketch_example_darker_img = tk.PhotoImage(file="..\img\graphic_sketch_example_darker.png")
        self.numeric_sketch_example_darker_img = tk.PhotoImage(file=r"..\img\numeric_sketch_example_darker.png")
        self.transparent_bg = tk.PhotoImage(file=r"..\img\transparent_bg.png")
        self.new_graphic_project_button = None
        self.new_numeric_project_button = None
        self.graphic_button_label = None
        self.numeric_button_label = None
        self.label_over_graphic_button = None
        self.build_menu_buttons()

    def build_menu_buttons(self):
        
        self.new_graphic_project_button = tk.Button(self, width=self.width, height=220,
                                               image=self.graphic_sketch_example_img,
                                               command=HomePage.app.create_graphic_project)
        self.new_graphic_project_button.bind("<Enter>", self.mouse_over_graphic_button)
        self.new_graphic_project_button.bind("<Leave>", self.mouse_left_graphic_button)
        #new_graphic_project_button.place(x=0, y=0)
        self.new_graphic_project_button.pack()
        
        self.new_numeric_project_button = tk.Button(self, width=self.width, height=220,
                                               image=self.numeric_sketch_example_img,
                                                command=HomePage.app.create_numeric_project)
        
        self.new_numeric_project_button.bind("<Enter>", self.mouse_over_numeric_button)
        self.new_numeric_project_button.bind("<Leave>", self.mouse_left_numeric_button)
        self.new_numeric_project_button.pack(side=tk.BOTTOM)
        
        self.numeric_button_label = tk.Label(self, width=self.width, height=220,
                                             text="Create numeric project...")
        

    def mouse_over_graphic_button(self, event):
        #self.new_numeric_project_button
        self.new_graphic_project_button.configure(image=self.graphic_sketch_example_darker_img)

    def mouse_left_graphic_button(self, event):
        self.new_graphic_project_button.configure(image=self.graphic_sketch_example_img)

    def mouse_over_numeric_button(self, event):
        self.new_numeric_project_button.configure(image=self.numeric_sketch_example_darker_img)

    def mouse_left_numeric_button(self, event):
        self.new_numeric_project_button.configure(image=self.numeric_sketch_example_img)
        

class ProgramDescription(tk.Frame):

    color = f'#FFFFFF'
    header_font = ("Arial", 30, "bold")
    subheader_font = ("Arial", 24, "bold")
    text_font = ("Arial", 15)

    header_text = "Welcome to Lensor!"
    subheader_text = "A software developed to solve optical problems."
    segment_1_text = "      The software calculates images of 2D objects through a lens, "\
                    "offering a comprehensive solution for simulating optical systems. "\
                    "By inputting parameters such as object distance, lens characteristics, "\
                    "and focal length, users can accurately predict the resulting images formed "\
                    "on the image plane."

    segment_2_text = "      Utilize graphic or numeric methods to simulate optical systems. "
                    

    segment_3_text = "      Draw any shapes when working with graphic project to find out drawn object's theoretical image. "\
                    

    segment_4_text = "      Simulate optical system using numeric project to get information about its aperture and field stops. "\
                    "Using numeric project, find out aperture and field rays of simulated system."

    text_bg = "#FFFFFF"

    text_x_padding = 10
    text_y_padding = 10
    

    def __init__(self, master, width):
        super().__init__(
            master=master,
            height=master.height,
            width=width,
            bg=ProgramDescription.color
        )
        self.width = width
        self.height = master.height
        self.pack_propagate(0)
        self.built_description()

    def built_description(self):
        text_frame = tk.Frame(self, width=int(self.width*0.9), height=int(self.height*0.8), bg=ProgramDescription.text_bg)
        text_frame.pack(padx=50, pady=40)
        text_frame.pack_propagate(0)
        header = self.build_header(text_frame, ProgramDescription.header_text)
        header.pack(padx=ProgramDescription.text_x_padding, pady=ProgramDescription.text_y_padding)
        subheader = self.build_subheader(text_frame, ProgramDescription.subheader_text)
        subheader.pack(padx=ProgramDescription.text_x_padding, pady=ProgramDescription.text_y_padding)
        text_segment_1 = self.build_text_segment(text_frame, ProgramDescription.segment_1_text)
        text_segment_1.pack(padx=ProgramDescription.text_x_padding, pady=ProgramDescription.text_y_padding)
        text_segment_2 = self.build_text_segment(text_frame, ProgramDescription.segment_2_text)
        text_segment_2.pack(padx=ProgramDescription.text_x_padding, pady=ProgramDescription.text_y_padding)
        text_segment_3 = self.build_text_segment(text_frame, ProgramDescription.segment_3_text)
        text_segment_3.pack(padx=ProgramDescription.text_x_padding, pady=ProgramDescription.text_y_padding)
        text_segment_4 = self.build_text_segment(text_frame, ProgramDescription.segment_4_text)
        text_segment_4.pack(padx=ProgramDescription.text_x_padding, pady=ProgramDescription.text_y_padding)

    def build_header(self, master, text):
        return tk.Label(
                        master,
                        width=int(self.width*0.8),
                        text=text,
                        font=ProgramDescription.header_font,
                        bg=ProgramDescription.text_bg,
                        wraplength=int(self.width*0.8),
                        anchor="w",
                        justify="left",
                        )

    def build_subheader(self, master, text):
        return tk.Label(
                        master,
                        width=int(self.width*0.8),
                        text=text,
                        font=ProgramDescription.subheader_font,
                        bg=ProgramDescription.text_bg,
                        wraplength=int(self.width*0.8),
                        anchor="w",
                        justify="left"
                        )

    def build_text_segment(self, master, text):
        return tk.Label(
                        master,
                        width=int(self.width*0.8),
                        text=text,
                        font=ProgramDescription.text_font,
                        bg=ProgramDescription.text_bg,
                        wraplength=int(self.width*0.8),
                        anchor="w",
                        justify="left"
                        )