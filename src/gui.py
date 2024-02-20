import tkinter as tk
import object as obj
#import object as obj
#import object as obj
import algorithm as alg
#import algorithm as alg


class MainWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lensor")
        self.sketch = None

        self.new_graphic_button = tk.Button(self.root, text="New graphic method project", command=self.create_graphic_project)
        self.new_graphic_button.pack(pady=20)

        self.new_numeric_button = tk.Button(self.root, text="New numeric method project", command=self.create_numeric_project)
        self.new_numeric_button.pack(pady=20)

        self.open_graphic_button = tk.Button(self.root, text="Open graphic method project...", command=self.open_graphic_project)
        self.open_graphic_button.pack(pady=20)

        self.open_numeric_button = tk.Button(self.root, text="Open numeric method project...", command=self.open_numeric_project)
        self.open_numeric_button.pack(pady=20)



    def destroy_starting_buttons(self):
        self.new_graphic_button.destroy()
        print(self.new_graphic_button)
        self.new_numeric_button.destroy()
        self.open_graphic_button.destroy()
        self.open_numeric_button.destroy()



    def create_graphic_project(self):
        self.destroy_starting_buttons()
        self.root.geometry("1000x500")
        self.sketch = GraphicSketch(self.root)


    def create_numeric_project(self):
        self.destroy_starting_buttons()
        self.root.geometry("1000x500")
        self.sketch = NumericSketch(self.root)

    def open_graphic_project(self):
        self.destroy_starting_buttons()

    def open_numeric_project(self):
        self.destroy_starting_buttons()



class Mouse:

    x = None
    y = None


    left_button_is_held = False

    def mouse_motion(event):
        Mouse.x, Mouse.y = event.x, event.y
        print('MOUSE: {}, {}'.format(Mouse.x, Mouse.y))


    def left_button_held(event):
        print("LPM CLICKED")
        Mouse.left_button_is_held = True

    def left_button_released(event):
        print("LPM RELEASED")
        Mouse.left_button_is_held = False


def pos_on_widget(event):
    Mouse.on_widget_x, Mouse.on_widget_y = event.x, event.y



class Sketch:

    def __init__(self, master, lenses=1):
        self.master = master
        self.canv = tk.Canvas(master=master, width=800, height=400, highlightbackground="black", highlightthickness=2, background="white")
        self.canv.pack(padx=100, pady=50)
        self.canv.bind('<Enter><Button-3>', Mouse.mouse_motion)
        self.axis = self.create_axis()
        


    def create_axis(self):
        return obj.Axis(self, 0, 200, 800, 200)




class GraphicSketch(Sketch):

    over_point = False
    deleting_point_mode = False
    processed_point = None
    shape_initial_points = []
    points_coords = []


    def __init__(self, master, lenses=1):
        super().__init__(master, lenses)
        self.lens = self.create_lens()
        self.clear_sketch_button = tk.Button(master=master, text="Clear", command=self.clear_sketch)
        self.clear_sketch_button.place(x=5,y=5)
        self.create_shape_button = tk.Button(master=master, text="Shape", command=self.build_shape)
        self.create_shape_button.place(x=50,y=5)
        self.show_data_button = tk.Button(master=master, text="Data", command=self.show_data)
        self.show_data_button.place(x=95,y=5)
        self.toggle_type_button = tk.Button(master=master, text="Toggle type", command=self.toggle_type)
        self.toggle_type_button.place(x=140,y=5)
        self.hide_all_rays_button = tk.Button(master=master, text="Hide all rays", command=self.hide_all_rays)
        self.hide_all_rays_button.place(x=215,y=5)
        self.unhide_all_rays_button = tk.Button(master=master, text="Unhide all rays", command=self.unhide_all_rays)
        self.unhide_all_rays_button.place(x=300,y=5)
        self.canv.bind('<ButtonRelease-3>', self.create_point)
        self.points = []
        self.resulting_points = {}
        self.shapes = []
        self.building_shape = False
        


    def create_lens(self, focal = 100, pos = 400, space = 30):
        return obj.GraphicLens(self, focal, pos, space)
    
    def check_point_presence(self, x, y):
        if len(self.points) > 0:
            for point in self.points:
                if x == point.x and y == point.y:
                    return True
                else:
                    return False
        else:
            return False


    def create_point(self, event):
        point_presence = self.check_point_presence(event.x, event.y)
        if point_presence is False:
            GraphicSketch.points_coords.append((event.x, event.y))
            point = self.new_point(event.x, event.y)
            if self.building_shape:
                GraphicSketch.shape_initial_points.append(point)
                obj.Shape.initial_points.append(point)
            
            for x in range (0, len(self.points)):
                print(f"{x+1}. {self.points[x]}: {self.points[x].x}x{self.points[x].y}, {event.x}x{event.y} -> {self.points[x].its_image_point}, ")
        else:
            print("THE POINT IS ALREADY DRAWN")
            for x in self.points:
                print(x)

    def new_point(self, x, y):
        return obj.Point(x, y, self)


    def cursor_over_point(self, point: obj.Point):
        self.canv.unbind("<ButtonRelease-3>")
        print(f"CURSOR OVER POINT OF ID {point.point_img}")
        GraphicSketch.processed_point = point
        
    def cursor_left_point(self):
        self.canv.bind('<ButtonRelease-3>', self.create_point)
        print("CURSOR LEFT THE POINT")
        GraphicSketch.processed_point = None


    def build_shape(self):
        print("CREATING SHAPE")
        self.create_shape_button.config(bg="red")
        self.master.bind("<Return>", lambda event: GraphicSketch.create_shape(self))
        self.building_shape = True

    def clear_sketch(self):
        for shape in self.shapes:
            shape.delete_shape(self)
        self.shapes.clear()
        print(f"POINTS: {len(self.points)}, SHAPES: {len(self.shapes)}")
        counter = 1
        print(self.points)
        for x in range (0, len(self.points)):
            self.points[-1].delete_point(self)
            print(self.points)
            counter += 1
        

    def delete_point(self, point: obj.Point):
        try:
            point.delete_point(self)
        except KeyError:
            ...


    def hide_all_rays(self):
        for point in self.points:
            obj.Point.hide_rays(point, self)


    def show_data(self):
        print(f"SHAPES: {len(self.shapes)}, POINTS: {len(self.points)}")
        for x in range(0, len(list(self.resulting_points.keys()))):
            keys = list(self.resulting_points.keys())
            print(f"{x+1}: {keys[x]} : {self.resulting_points[keys[x]]}")


    def toggle_type(self):
        focal = self.lens.focal * -1
        pos = self.lens.pos
        space = self.lens.space
        print(f"{focal} {pos} {space}")
        self.lens.erase_image(self)
        del self.lens
        self.lens = self.create_lens(focal, pos, space)
        obj.lens_toggle_render(self)


    def unhide_all_rays(self):
        for point in self.points:
            obj.Point.unhide_rays(point, self)



    @staticmethod
    def create_shape(sketch):
        shape = obj.Shape(None, None, GraphicSketch.shape_initial_points, sketch)
        GraphicSketch.shape_initial_points.clear()
        obj.Shape.initial_points = []
        print(f"SHAPE CREATED, length: {len(shape.points)}")
        sketch.create_shape_button.config(bg="white")
        sketch.master.unbind("<Return>")
        sketch.building_shape = False



class NumericSketch(Sketch):

    def __init__(self, master, lenses=1):
        super().__init__(master, lenses)
        self.create_lens()
        self.lenses = []
        self.apertures = []
        self.points = []
        
        self.place_object_button = tk.Button(master=master, text="Object", command=self.create_point)
        self.place_object_button.place(x=5, y=5)
        self.place_aperture_button = tk.Button(master=master, text="Aperture", command=self.create_aperture)
        self.place_aperture_button.place(x=50, y=5)
        self.place_lens_button = tk.Button(master=master, text="Lens", command=self.create_lens2)
        self.place_lens_button.place(x=115, y=5)
        self.show_data_button = tk.Button(master=master, text="Data", command=self.show_data)
        self.show_data_button.place(x=160, y=5)
        self.define_rays_button = tk.Button(master=master, text="Define rays", command=self.define_rays)
        self.define_rays_button.place(x=220, y=5)
        self.define_aperture_ray_button = tk.Button(master=master, text="Define aperture ray", command=self.define_aperture_ray)
        self.define_aperture_ray_button.place(x=300, y=5)
        
        

    def create_lens(self):
        return CreateLensWindow(400, 200, self.master, self)
    

    def create_lens2(self):
        self.place_lens_button.config(background="red")
        self.canv.bind('<ButtonRelease-1>', self.place_lens)

    
    def create_point(self):
        self.place_object_button.config(background="red")
        self.canv.bind('<ButtonRelease-1>', self.place_point)


    def define_rays(self):
        for point in self.points:
            aperture_tan_dict = alg.NumericCalc.define_main_aperture(point, self.apertures)
            main_aperture = list(aperture_tan_dict.keys())[0]
            aperture_ray = obj.NumericApertureRay(self, point, main_aperture)
            field_tan_dict = alg.NumericCalc.define_field_aperture(main_aperture, self.apertures)
            field_aperture = list(field_tan_dict.keys())[0]
            field_ray = obj.NumericFieldRay(self, main_aperture, field_aperture)


    def define_aperture_ray(self):
        for point in self.points:
            aperture_tan_dict = alg.NumericCalc.define_main_aperture(point, self.apertures)
            aperture_ray = obj.NumericApertureRay(self, point, list(aperture_tan_dict.keys())[0])
    

    def place_point(self, event):
        self.place_object_button.config(background="white")
        self.canv.unbind('<ButtonRelease-1>')
        self.points.append(obj.NumericPoint(event.x, event.y, self))


    def create_aperture(self):
        self.place_aperture_button.config(background="red")
        self.canv.bind('<ButtonRelease-1>', self.place_aperture)


    def move_distance_label(self, event):
        self.canv.unbind('<ButtonRelease-1>')
        self.canv.bind('<ButtonRelease-1>', self.place_aperture)

    
    def place_aperture(self, event):
        self.place_aperture_button.config(background="white")
        self.canv.unbind('<ButtonRelease-1>')
        return CreateApertureWindow(event.x, event.y, self.master, self)


    def place_lens(self, event):
        self.place_lens_button.config(background="white")
        self.canv.unbind('<ButtonRelease-1>')
        return CreateLensWindow(event.x, event.y, self.master, self)


    def show_data(self):
        print(len(self.apertures))



class NumericEntry():

    def __init__(self, x, y, sketch):
        self.x = x
        self.y = y
        print(f"{x}, {y}")
        self.entry = tk.Entry(master=sketch.canv, width=5,  bd=3)
        self.entry.place(x=self.x, y=self.y)


    @staticmethod
    def temp_text(e, entry, text):
        entry.delete(text, "end")


class NumericDiameterEntry(NumericEntry):

    def __init__(self, x, y, sketch) -> None:
        super().__init__(x, y, sketch)
        self.set_diameter_value(sketch)

    def process_diameter_entry_value(self, entry, sketch, window):
        diameter = abs(float(entry.get()))
        sketch.canv.delete(window)
        sketch.apertures.append(obj.NumericAperture(self.x, self.y, sketch, diameter))


    def set_diameter_value(self, sketch):
        diameter = 30
        print("SETTING DIAMETER VALUE")
        self.entry.insert(0, f"{diameter}")
        window = sketch.canv.create_window(self.y, self.y, window=self.entry, anchor=tk.NW)
        self.entry.bind("<FocusIn>", lambda event: NumericEntry.temp_text(event, self.entry, diameter))
        self.entry.bind("<Return>", lambda event: self.process_diameter_entry_value(self.entry, sketch, window))



class NumericEntry2():

    def __init__(self, x, y, master):
        self.entry = tk.Entry(master=master, width=40, bd=3)
        self.entry.pack()


    @staticmethod
    def temp_text(e, entry, text):
        entry.delete(text, "end")



class NumericDiameterEntry2(NumericEntry2):

    def __init__(self, x, y, master) -> None:
        super().__init__(x, y, master)
        self.set_diameter_value(master)

    def process_diameter_entry_value(self, entry, sketch, window):
        diameter = abs(float(entry.get()))

        sketch.apertures.append(obj.NumericAperture(self.x, self.y, sketch, diameter))


    def set_diameter_value(self, sketch):
        diameter = 30
        print("SETTING DIAMETER VALUE")
        self.entry.insert(0, f"{diameter}")

        self.entry.bind("<FocusIn>", lambda event: NumericEntry.temp_text(event, self.entry, diameter))
        self.entry.bind("<Return>", lambda event: self.process_diameter_entry_value(self.entry, sketch))


class NumericFocalEntry(NumericEntry):

    def __init__(self, x, y, sketch) -> None:
        super().__init__(x, y, sketch)
        self.set_focal_value(sketch)

    def process_focal_entry_value(self, entry, sketch, window):
        diameter = float(entry.get())
        sketch.canv.delete(window)
        sketch.apertures.append(obj.NumericAperture(self.x, self.y, sketch, diameter))


    def set_focal_value(self, sketch):
        focal = 50
        print("SETTING FOCAL VALUE")
        self.entry.insert(0, f"{focal}")
        window = sketch.canv.create_window(self.y, self.y, window=self.entry, anchor=tk.NW)
        self.entry.bind("<FocusIn>", lambda event: NumericEntry.temp_text(event, self.entry, focal))
        self.entry.bind("<Return>", lambda event: self.process_focal_entry_value(self.entry, sketch, window))


class NumericWindow:

    def __init__(self, x, y, master) -> None:
        self.window = tk.Toplevel(master)
        
        self.x = x
        self.y = y
        

    def __del__(self):
        ...


    def delete_window(self):
        print("DELETED WINDOW")
        self.window.destroy()


class CreateApertureWindow(NumericWindow):

    def __init__(self, x, y, master, sketch) -> None:
        super().__init__(x, y, master)
        self.sketch = sketch
        self.window.title("Create aperture")
        self.diameter_label = tk.Label(self.window, text="SET DIAMETER VALUE:")
        self.diameter_label.pack()
        self.diameter_entry = NumericEntry2(10, 10, self.window)
        self.button = tk.Button(self.window, text="OK", command = self.process_values)
        self.button.pack()


    def process_values(self):
        diameter = abs(float(self.diameter_entry.entry.get()))
        self.sketch.apertures.append(obj.NumericAperture(self.x, self.y, self.sketch, diameter))
        print(diameter)
        self.delete_window()
        


class CreateLensWindow(NumericWindow):

    def __init__(self, x, y, master, sketch) -> None:
        super().__init__(x, y, master)
        self.window.title("Create lens")
        self.sketch = sketch
        self.diameter_label = tk.Label(self.window, text="SET DIAMETER VALUE:")
        self.diameter_label.pack()
        self.diameter_entry = NumericEntry2(10, 10, self.window)

        self.focal_label = tk.Label(self.window, text="SET FOCAL VALUE:")
        self.focal_label.pack()
        self.focal_entry = NumericEntry2(10, 10, self.window)

        self.button = tk.Button(self.window, text="OK", command = self.process_values)
        self.button.pack()


    def process_values(self):
        diameter = abs(float(self.diameter_entry.entry.get()))
        focal = float(self.focal_entry.entry.get())
        new_lens = obj.NumericLensObject2(self.x, self.y, self.sketch, diameter, focal)
        if len(self.sketch.lenses) == 0:
            self.sketch.lens = new_lens
        self.sketch.lenses.append(new_lens)
        self.sketch.apertures.append(new_lens)
        print(diameter)
        print(focal)
        self.delete_window()



if __name__ == "__main__":

    app = MainWindow()
    app.root.mainloop()
