import tkinter as tk
import sketches as sk
import home_page_gui as home



class MainWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lensor")
        self.sketch = None
        self.properties_table = None
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.menu = None
        self.create_home_menu()

        self.base = home.HomePage(self)

        self.root.config(menu=self.menu)

    def create_home_menu(self):
        self.menu = tk.Menu(self.root)
        filemenu = tk.Menu(self.menu, tearoff=0)
        filemenu.add_command(label="New Graphic Project", command=self.create_graphic_project)
        filemenu.add_command(label="New Numeric Project", command=self.create_numeric_project)
        self.menu.add_cascade(label="File", menu=filemenu)

    def create_graphic_project(self):
        self.root.state('zoomed')
        if self.sketch is not None:
            self.sketch.base.destroy()
        if self.base is not None:
            self.base.destroy()
            self.base = None
        self.sketch = GraphicProject(self)

    def create_numeric_project(self):
        self.root.state('zoomed')
        if self.sketch is not None:
            self.sketch.base.destroy()
        if self.base is not None:
            self.base.destroy()
            self.base = None
        self.sketch = NumericProject(self)

    def create_properties_table(self):
        properties_table = PropertiesTable(self)
        return properties_table
    

    def return_to_home_page(self):
        self.sketch.base.destroy()
        self.base = home.HomePage(self)
        self.create_home_menu()
        self.root.config(menu=self.menu)
    

class PropertiesTable:

    def __init__(self, project) -> None:
        self.project = project
        self.base = self.create_base()
        self.table_screen_frame = None
        self.object_properties_frame = None
        self.table_screen = self.create_table_screen()
        self.object_properties = self.create_object_properties()
    
    def create_base(self):
        base = tk.Frame(self.project.root, width=100, height=self.project.screen_height)
        base.place(x=1120, y=0)
        return base

    def create_table_screen_frame(self):
        frame = tk.Frame(self.base, height=240, width=240)
        frame.pack()
        frame.pack_propagate(0)
        return frame
    
    def create_object_properties_frame(self):
        frame = tk.Frame(self.base, height=500, width=240)
        frame.pack(pady=10)
        frame.pack_propagate(0)
        return frame

    def create_table_screen(self):
        frame = self.create_table_screen_frame()
        table = tk.Canvas(
            master=frame,
            highlightbackground="black",
            highlightthickness=2,
            background="white",
            )
        table.pack()
        return table
    
    def create_object_properties(self):
        frame = self.create_object_properties_frame()
        table = tk.Canvas(
            master=frame,
            highlightbackground="black",
            highlightthickness=2,
            background="white",
            )
        table.pack()
        return table




class Mouse:
    x = None
    y = None

    left_button_is_held = False

    def mouse_motion(event):
        Mouse.x, Mouse.y = event.x, event.y

    def left_button_held(event):
        Mouse.left_button_is_held = True

    def left_button_released(event):
        Mouse.left_button_is_held = False


def pos_on_widget(event):
    Mouse.on_widget_x, Mouse.on_widget_y = event.x, event.y


class GraphicProject:

    def __init__(self, window, lenses=1):

        self.window = window
        self.width = window.root.winfo_width()
        self.height = window.root.winfo_height()
        self.lenses = []
        self.points = []
        self.resulting_points = {}
        self.lines = []
        self.resulting_lines = {}
        self.shapes = []
        self.resulting_shapes = {}
        self.building_shape = False
        self.building_line = False
        self.line_initial_points = []
        self.shape_initial_lines = []
        self.points_coords = []

        processed_point = None
        self.window.menu = self.create_graphic_project_menu_bar()
        self.base = self.create_project_frame()


    def create_graphic_project_menu_bar(self):
        graphic_project_menu = tk.Menu(self.window.root)
        file_menu = tk.Menu(graphic_project_menu, tearoff=0)
        file_menu.add_command(label="Return to home page", command=self.window.return_to_home_page)
        file_menu.add_command(label="New Graphic Project", command=self.window.create_graphic_project)
        file_menu.add_command(label="New Numeric Project", command=self.window.create_numeric_project)
        graphic_project_menu.add_cascade(label="File", menu=file_menu)
        sketch_menu = tk.Menu(graphic_project_menu, tearoff=0)
        sketch_menu.add_command(label="Clear", command=self.clear_sketch)
        sketch_menu.add_command(label="Toggle Lens Type", command=self.toggle_type)
        graphic_project_menu.add_cascade(label="Sketch", menu=sketch_menu)
        object_menu = tk.Menu(graphic_project_menu, tearoff=0)
        object_menu.add_command(label="Place Line", command=self.build_line)
        object_menu.add_command(label="Place Shape", command=self.build_shape)
        graphic_project_menu.add_cascade(label="Object", menu=object_menu)
        rays_menu = tk.Menu(graphic_project_menu, tearoff=0)
        rays_menu.add_command(label="Hide All Rays", command=self.hide_all_rays)
        rays_menu.add_command(label="Unhide All Rays", command=self.unhide_all_rays)
        graphic_project_menu.add_cascade(label="Rays", menu=rays_menu)
        lens_menu = tk.Menu(graphic_project_menu, tearoff=0)
        lens_menu.add_command(label="Lenses Properties", command=self.change_lenses_properties)
        lens_menu.add_command(label="Add Lens", command=self.add_lens)
        graphic_project_menu.add_cascade(label="Lens", menu=lens_menu)
        data_menu = tk.Menu(graphic_project_menu, tearoff=0)
        data_menu.add_command(label="Show Data", command=self.show_data)
        graphic_project_menu.add_cascade(label="Data", menu=data_menu)
        

        self.window.root.config(menu=graphic_project_menu)
        return graphic_project_menu


    def create_left_frame(self, master):
        left_frame = tk.Frame(master)
        left_frame.pack(side=tk.LEFT)
        self.create_sketch_frame(left_frame)
        #self.create_console_frame(left_frame)



    def create_sketch_frame(self, master):
        sketch_frame = tk.Frame(master, width= self.width, height=self.height)
        sketch_frame.pack(side=tk.TOP)
        sketch_frame.pack_propagate(0)
        self.create_graphic_sketch(sketch_frame)


    def create_console_frame(self, master):
        console_frame = tk.Frame(master, width= self.width, height=self.height/5, bg="grey")
        console_frame.pack(side=tk.TOP)
        console_frame.pack_propagate(0)


    def create_project_frame(self):
        frame = tk.Frame(self.window.root)
        frame.pack()
        self.create_left_frame(frame)
        return frame
        


    def create_graphic_sketch(self, master):
        self.canv = sk.GraphicSketch(self, master)

    def change_lenses_properties(self):
        ...
    
    def add_lens(self):
        ...
        
    def build_line(self):
        self.window.root.bind("<Escape>", lambda event: self.canv.stop_creating_line())
        self.building_line = True

    def build_shape(self):
        self.window.root.bind("<Return>", lambda event: self.canv.create_shape())
        self.window.root.bind("<Escape>", lambda event: self.canv.stop_creating_shape())
        self.building_shape = True

    def clear_sketch(self):
        if self.building_shape is False and self.building_line is False:
            return self.canv.clear_sketch()

    def hide_all_rays(self):
        return self.canv.hide_all_rays()

    def show_data(self):
        ...

    def toggle_type(self):
        return self.canv.toggle_type()

    def unhide_all_rays(self):
        return self.canv.unhide_all_rays()



class NumericProject:
    def __init__(self, window, lenses=1):

        self.window = window
        self.lenses = []
        self.user_defined_lenses = []
        self.real_plane_lenses = []
        self.resulting_lenses = {}
        self.lens_numbers_dictionary = {}
        self.apertures = []
        self.user_defined_apertures = []
        self.real_plane_apertures = []
        self.resulting_apertures = {}
        self.points = []
        self.user_defined_points = []
        self.real_plane_points = []
        self.resulting_points = {}
        self.objects = []
        
        self.aperture_rays = []
        self.field_rays = []

        self.window.menu = self.create_numeric_project_menu_bar()
        self.base = self.create_project_frame()

    def create_numeric_project_menu_bar(self):
        numeric_project_menu = tk.Menu(self.window.root)
        file_menu = tk.Menu(numeric_project_menu, tearoff=0)
        file_menu.add_command(label="Return to home page", command=self.window.return_to_home_page)
        file_menu.add_command(label="New Graphic Project", command=self.window.create_graphic_project)
        file_menu.add_command(label="New Numeric Project", command=self.window.create_numeric_project)
        numeric_project_menu.add_cascade(label="File", menu=file_menu)
        sketch_menu = tk.Menu(numeric_project_menu, tearoff=0)
        sketch_menu.add_command(label="Clear", command=self.clear_sketch)
        numeric_project_menu.add_cascade(label="Sketch", menu=sketch_menu)
        object_menu = tk.Menu(numeric_project_menu, tearoff=0)
        object_menu.add_command(label="Place Aperture", command=self.create_aperture)
        object_menu.add_command(label="Place Lens", command=self.create_lens)
        object_menu.add_command(label="Define Rays", command=self.define_rays)
        object_menu.add_command(label="Define Aperture Ray", command=self.define_aperture_ray)
        object_menu.add_command(label="Define Field Ray", command=self.define_aperture_ray)
        numeric_project_menu.add_cascade(label="Object", menu=object_menu)

        self.window.root.config(menu=numeric_project_menu)
        return numeric_project_menu

    def create_left_frame(self, master):
        left_frame = tk.Frame(master)
        left_frame.pack(side=tk.LEFT)
        self.create_sketch_frame(left_frame)
        #self.create_console_frame(left_frame)

    def create_right_frame(self, master):
        right_frame = tk.Frame(master)
        right_frame.pack(side=tk.RIGHT)
        self.create_object_properties_frame(right_frame)
    
    def create_buttons_frame(self, master):
        button_frame = tk.Frame(master, width=1150, height=40)
        button_frame.pack(side=tk.TOP)
        button_frame.pack_propagate(0)
        self.create_menu(button_frame)
        self.create_buttons(button_frame)

    def create_sketch_frame(self, master):
        sketch_frame = tk.Frame(master, width=1100, height=self.window.screen_height)
        sketch_frame.pack(side=tk.TOP)
        sketch_frame.pack_propagate(0)
        self.create_numeric_sketch(sketch_frame)

    def create_console_frame(self, master):
        console_frame = tk.Frame(master, width=1100, height=200, bg="white", highlightbackground="black", highlightthickness=1)
        console_frame.pack(side=tk.TOP)
        console_frame.pack_propagate(0)

    def create_object_properties_frame(self, master):
        self.object_properties = NumericObjectsProperties(master=master, width=self.window.screen_width-1100, height=self.window.screen_height, window=self.window)

    def create_project_frame(self):
        frame = tk.Frame(self.window.root)
        frame.pack()
        self.create_left_frame(frame)
        self.create_right_frame(frame)
        return frame

    def clear_sketch(self):
        ...

    def create_numeric_sketch(self, master):
        self.canv = sk.NumericSketch(self, master)

    def create_object_properties(self, master):
        master.update()
        width = master.winfo_width()
        height = master.winfo_height()
        self.object_properties_table = tk.Label(master, width=width, height=height)
        self.object_properties_table.pack(side=tk.TOP)


    def define_rays(self):
        self.canv.define_rays(self)

    def define_aperture_ray(self):
        ...


    def create_aperture(self):
        return self.canv.create_aperture()
    
    def create_lens(self):
        return self.canv.create_lens2()

    def move_distance_label(self, event):
        self.canv.unbind("<ButtonRelease-1>")
        self.canv.bind("<ButtonRelease-1>", self.place_aperture)


class NumericObjectsProperties(tk.Frame):

    def __init__(self, master, width, height, window):
        super().__init__(master=master, width=width, height=height, highlightbackground="black", highlightthickness=1)
        self.pack(side=tk.TOP)
        self.pack_propagate(0)
        self.master = master
        self.width = width
        self.height = height
        self.window = window
        self.list_of_rows = []
        self.create_properties()

    def create_properties(self):
        self.create_properties_label(self)
        self.table_columns = self.create_table(self)

    def create_properties_label(self, master):
        properties_label = tk.Label(master=master, width=self.width, text="OBJECTS PROPERTIES", highlightbackground="black", highlightthickness=1)
        properties_label.pack(side=tk.TOP)

    def create_properties_columns(self, master):
        self.object_name_column = self.create_object_name_column(master)
        self.object_distance_column = self.create_object_distance_column(master)
        self.object_diameter_column = self.create_object_diameter_column(master)
        self.object_focal_column = self.create_object_focal_column(master)

    def create_object_name_column(self, master):
        object_name_column = tk.Frame(master, width=2*self.width/5, height=self.window.screen_height)
        object_name_column.pack(side=tk.LEFT)
        object_name_column.pack_propagate(0)
        return object_name_column
    
    def create_object_distance_column(self, master):
        object_distance_column = tk.Frame(master, width=self.width/5, height=self.window.screen_height)
        object_distance_column.pack(side=tk.LEFT)
        object_distance_column.pack_propagate(0)
        return object_distance_column
    
    def create_object_diameter_column(self, master):
        object_diameter_column = tk.Frame(master, width=self.width/5, height=self.window.screen_height)
        object_diameter_column.pack(side=tk.LEFT)
        object_diameter_column.pack_propagate(0)
        return object_diameter_column
    
    def create_object_focal_column(self, master):
        object_focal_column = tk.Frame(master, width=self.width/5, height=self.window.screen_height)
        object_focal_column.pack(side=tk.LEFT)
        object_focal_column.pack_propagate(0)
        return object_focal_column
    
    def create_table(self, master):
        table_frame = tk.Frame(master, width=self.width, height=self.window.screen_height)
        table_frame.pack(side=tk.TOP)
        table_frame.pack_propagate(0)
        self.create_properties_columns(table_frame)
        self.create_first_row()
        return table_frame

    def create_first_row(self):
        name_label = tk.Label(master=self.object_name_column, width=int(2*self.width/5), text="Name", highlightbackground="black", highlightthickness=1)
        name_label.pack(side=tk.TOP)
        distance_label = tk.Label(master=self.object_distance_column, width=int(self.width/2), text="Distance", highlightbackground="black", highlightthickness=1)
        distance_label.pack(side=tk.TOP)
        diameter_label = tk.Label(master=self.object_diameter_column, width=int(self.width/5), text="Diameter", highlightbackground="black", highlightthickness=1)
        diameter_label.pack(side=tk.TOP)
        focal_label = tk.Label(master=self.object_focal_column, width=int(self.width/5), text="Focal", highlightbackground="black", highlightthickness=1)
        focal_label.pack(side=tk.TOP)

    def create_properties_row(self, numeric_object):
        new_row = NumericPropertiesRow(self, numeric_object)
        self.list_of_rows.append(new_row)

    def remove_properties_row(self, numeric_object):
        for properties_row in self.list_of_rows:
            if properties_row.numeric_object is numeric_object:
                properties_row.delete_row()
                self.list_of_rows.remove(properties_row)
                return


class NumericPropertiesRow:

    def __init__(self, properties, numeric_object):
        self.properties = properties
        self.numeric_object = numeric_object
        self.create_row()

    def create_row(self):
        self.name_label = self.create_name_label()
        self.distance_label = self.create_distance_label()
        self.diameter_label = self.create_diameter_label()
        self.focal_label = self.create_focal_label()

    def create_name_label(self):
        name_label = tk.Label(master=self.properties.object_name_column, width=int(2*self.properties.width/5), text=self.numeric_object, bg="white")
        name_label.pack(side=tk.TOP)
        return name_label
    
    def create_distance_label(self):
        distance_label = tk.Label(master=self.properties.object_distance_column, width=int(self.properties.width/5), text=self.numeric_object.distance_value, bg="white")
        distance_label.pack(side=tk.TOP)
        return distance_label
    
    def create_diameter_label(self):
        try:
            diameter_label = tk.Label(master=self.properties.object_diameter_column, width=int(self.properties.width/5) , text= "%.3f" % self.numeric_object.diameter, bg="white")
        except AttributeError:
            diameter_label = tk.Label(master=self.properties.object_diameter_column, width=int(self.properties.width/5) , text="-", bg="white")
        diameter_label.pack(side=tk.TOP)
        return diameter_label
    
    def create_focal_label(self):
        try:
            if self.numeric_object.focal is not None:
                focal_label = tk.Label(master=self.properties.object_focal_column, width=int(self.properties.width/4) , text=self.numeric_object.focal, bg="white")
            else:
                focal_label = tk.Label(master=self.properties.object_focal_column, width=int(self.properties.width/4) , text="-", bg="white")
        except AttributeError:
            focal_label = tk.Label(master=self.properties.object_focal_column, width=int(self.properties.width/4) , text="-", bg="white")
        focal_label.pack(side=tk.TOP)
        return focal_label

    def update_row(self):
        self.delete_row()
        self.create_row()
    

    def delete_row(self):
        self.name_label.destroy()
        self.distance_label.destroy()
        self.diameter_label.destroy()
        self.focal_label.destroy()



if __name__ == "__main__":
    app = MainWindow()
    app.root.mainloop()