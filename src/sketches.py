import tkinter as tk
import algorithm as alg
import graphic_objects_logic as graphic_obj
import numeric_objects_logic as numeric_obj


class GraphicSketch(tk.Canvas):
    
    def __init__(self, project, master) -> None:
        super().__init__(
            master,
            width=project.width-6,
            height=project.height,
            highlightbackground="black",
            highlightthickness=2,
            background="white",
            )
        self.height=int(self.cget("height"))
        self.width=int(self.cget("width"))
        self.pack()
        self.project = project
        self.master = master
        self.building_shape = False
        self.bind("<ButtonRelease-3>", self.create_point)

        self.axis = self.create_axis()
        self.lens = self.create_lens()
        

    def create_axis(self):
        return graphic_obj.Axis(self, 0, self.width, self.height/2)

    def create_lens(self, focal=100):
        new_lens = graphic_obj.GraphicLens(self, focal, self.width/2, self.height/2)
        self.project.lenses.append(new_lens)
        return new_lens

    def check_point_presence(self, x, y):
        if len(self.project.points) > 0:
            for point in self.project.points:
                if x == point.x and y == point.y:
                    return True
            return False
        else:
            return False

    def create_point(self, event):
        point_presence = self.check_point_presence(event.x, event.y)
        if point_presence is False:
            self.project.points_coords.append((event.x, event.y))
            point = self.new_point(event.x, event.y)
            if self.project.building_line:
                self.project.line_initial_points.append(point)
                if len(self.project.line_initial_points) > 1:
                    self.create_graphic_line()
            elif self.project.building_shape:
                self.project.line_initial_points.append(point)
                if len(self.project.line_initial_points) > 1:
                    self.create_graphic_line(building_shape=True)
                    self.project.shape_initial_lines.append(self.project.lines[-2])

            self.render_sketch()

    def new_point(self, x, y):
        return graphic_obj.Point(x, y, self)

    def cursor_over_point(self, point: graphic_obj.Point):
        self.project.processed_point = point

    def cursor_left_point(self):
        self.project.processed_point = None


    def clear_sketch(self):
        for shape in self.project.shapes:
            shape.delete_shape()
        self.project.shapes.clear()
        self.project.resulting_shapes.clear()
        for line in self.project.lines:
            line.delete_line()
        self.project.lines.clear()
        self.project.resulting_lines.clear()

        points_list_len = len(self.project.points)
        for point in self.project.points:
            point.delete_point()
        
        self.project.points.clear()
        self.project.resulting_points.clear()
        self.render_sketch()


    def hide_all_rays(self):
        for point in self.project.points:
            point.sprite.hide_rays()


    def show_data(self):
        for x in range(0, len(list(self.resulting_points.keys()))):
            keys = list(self.resulting_points.keys())

    def toggle_type(self):
        focal = self.lens.focal * -1
        pos = self.lens.pos
        space = self.lens.space
        self.lens.delete_lens()
        del self.lens
        self.lens = self.create_lens(focal)
        graphic_obj.lens_toggle_render(self, self.lens)

    def unhide_all_rays(self):
        for point in self.project.points:
            point.sprite.unhide_rays()

    def create_graphic_line(self, building_shape=False):
        point_1, point_2 = self.project.line_initial_points[0], self.project.line_initial_points[1]
        line = graphic_obj.Line(point_1, point_2, self, "user_defined", color="black")
        if building_shape:
            self.project.line_initial_points.pop(0)
        else:
            self.project.line_initial_points.clear()
        self.project.building_line = False
        self.render_sketch()

    def stop_creating_line(self):
        for point in self.project.line_initial_points:
            point.delete_point()
            self.project.resulting_points.pop(point)
            self.project.points.remove(point)
        
        self.project.line_initial_points.clear()

        self.project.building_line = False
        


    def create_shape(self):
        shape = graphic_obj.Shape(self.project.shape_initial_lines, self, "user_defined")
        self.project.shape_initial_lines.clear()
        self.project.line_initial_points.clear()
        self.project.building_shape = False
        self.unbind("<ButtonRelease-1>")
        self.render_sketch()
        

    def stop_creating_shape(self):
        if len(self.project.line_initial_points) > 0:
            for point in self.project.line_initial_points:
                point.delete_point()
                self.project.resulting_points.pop(point)
                self.project.points.remove(point)
            
            self.project.line_initial_points.clear()

        for line in self.project.shape_initial_lines:
            point_1 = line.point_1
            point_1.delete_point()
            self.project.resulting_points.pop(point_1)
            self.project.points.remove(point_1)
            point_2 = line.point_2
            point_2.delete_point()
            self.project.resulting_points.pop(point_2)
            self.project.points.remove(point_2)
            line.its_image_line.delete_line()
            line.delete_line()
            self.project.resulting_lines.pop(line)
            self.project.lines.remove(line)
        
        self.project.shape_initial_lines.clear()

        self.project.building_line = False


    def render_sketch(self):
        graphic_obj.render_all_objects(self.project)


class NumericSketch(tk.Canvas):
    
    def __init__(self, project, master, lenses=1):
        super().__init__(
            master,
            width=1100,
            height=project.window.screen_height,
            highlightbackground="black",
            highlightthickness=2,
            background="white",
            )
        self.height=int(self.cget("height"))
        self.width=int(self.cget("width"))
        self.pack(side=tk.LEFT)
        self.project = project
        self.master = master
        self.bind("<ButtonRelease-3>", self.create_object)

        self.axis = self.create_axis()
        self.lens = None
        self.place_lens()
        

    def create_axis(self):
        return numeric_obj.Axis(self, 0, self.width, self.height/2)

    def create_lens(self, focal, diameter, pos):
        return numeric_obj.NumericLens(self, focal, diameter, pos)
    

    def create_lens2(self):
        self.bind("<ButtonRelease-1>", self.place_lens)


    def create_object(self, event):
        return LensConversionCheckbox(self, event, creating_point=True)

    def create_aperture(self):
        self.bind("<ButtonRelease-1>", self.place_aperture)


    def place_aperture(self, event):
        self.unbind("<ButtonRelease-1>")
        self.unbind("<ButtonRelease-3>")
        return LensConversionCheckbox(self, event, creating_aperture=True)
    
    def place_lens(self, event=None):
        self.unbind("<ButtonRelease-1>")
        if event == None:
            self.unbind("<ButtonRelease-3>")
            return CreateLensWindow(self.width/2, self.axis.y, self.master, self)
        else:
            self.unbind("<ButtonRelease-3>")
            return LensConversionCheckbox(self, event, creating_lens=True)
    

    def clear_rays_lists(self, project):
        for ray in project.aperture_rays:
            ray.delete_ray()
        for ray in project.field_rays:
            ray.delete_ray()
        project.aperture_rays.clear()
        project.field_rays.clear()


    def define_rays(self, project):
        self.clear_rays_lists(project)
        lenses = self.project.user_defined_lenses
        for point in project.user_defined_points:
            real_plane_point = point.get_real_plane_object(project.user_defined_lenses[0])
            aperture_tan_dict = alg.NumericCalc.define_main_aperture(
                real_plane_point, project.real_plane_apertures
            )
            main_aperture = list(aperture_tan_dict.keys())[0]
            aperture_ray = numeric_obj.NumericApertureRay(self, real_plane_point, main_aperture, right_object=lenses[0])
            field_tan_dict = alg.NumericCalc.define_field_aperture(
                main_aperture, project.real_plane_apertures
            )
            if field_tan_dict is not None:
                field_aperture = list(field_tan_dict.keys())[0]
                if isinstance(main_aperture, numeric_obj.NumericLensObject2) and main_aperture.object_type=="user_defined":
                    field_ray = numeric_obj.NumericFieldRay(self, main_aperture, field_aperture, right_object=main_aperture)
                    aperture_ray.bound_field_ray = field_ray
                    field_ray.bound_aperture_ray = aperture_ray
                else:
                    field_ray = numeric_obj.NumericFieldRay(self, main_aperture, field_aperture, right_object=lenses[0])
                    aperture_ray.bound_field_ray = field_ray
                    field_ray.bound_aperture_ray = aperture_ray


class NumericEntry2:
    def __init__(self, x, y, master):
        self.entry = tk.Entry(master=master, width=40, bd=3)
        self.entry.pack()

    @staticmethod
    def temp_text(e, entry, text):
        entry.delete(text, "end")


class NumericWindow:
    def __init__(self, x, y, master) -> None:
        self.window = tk.Toplevel(master)
        self.master = master

        self.x = x
        self.y = y

    def __del__(self):
        ...

    def delete_window(self):
        self.window.destroy()

    def create_proceed_button(self):
        button = tk.Button(self.window, text="OK", command=self.process_values)
        button.pack()
        button.focus_set()
        return button


class CheckboxOptionRow(tk.Frame):
    
    lens_options_list = {}
    conversion_options_list = ["Item", "Image"]
     

    def __init__(self, window):
        super().__init__(master=window)
        self.window = window
        self.generate_lens_option_list()
        
        self.lens_option_menu = self.create_lens_option_menu()
        self.conversion_option_menu = self.create_conversion_option_menu()
        self.distance_value_input = self.create_distance_value_input()
        

    def create_label(self):
        label_text = "Lens no. "
        label = tk.Label(master=self, text=label_text)
        label.pack(side=tk.LEFT)
        return label
    
    def generate_lens_option_list(self):
        CheckboxOptionRow.lens_options_list.clear()
        for i, item in enumerate(self.window.sketch.project.user_defined_lenses):
            CheckboxOptionRow.lens_options_list.update({item.number : item})

    def get_conversion_option_value(self):
        conversion_option_value = tk.StringVar(self)
        conversion_option_value.set(CheckboxOptionRow.conversion_options_list[0])
        return conversion_option_value
    
    def get_lens_option_value(self):
        self.generate_lens_option_list()
        lens_option_value = tk.StringVar(self)
        lens_option_value.set(list(CheckboxOptionRow.lens_options_list.keys())[0])
        return lens_option_value

    def create_distance_value_input(self):
        label_text = "Distance from selected lens: "
        label = tk.Label(master=self, text=label_text)
        label.pack(side=tk.LEFT)
        distance_entry = tk.Entry(self, width=10)
        distance_value = self.window.event.x - CheckboxOptionRow.lens_options_list[int(self.lens_option_value.get())].x
        distance_entry.insert(0, f"{distance_value}")
        distance_entry.pack(side=tk.LEFT)
        return distance_entry
    

    @staticmethod
    def temp_text(e, entry, text):
        entry.delete(text, "end")


    def create_conversion_option_menu(self):
        label_text = "Object-to-lens relation: "
        label = tk.Label(master=self, text=label_text)
        label.pack(side=tk.LEFT)
        self.conversion_option_value = self.get_conversion_option_value()
        options = tk.OptionMenu(self, self.conversion_option_value, *CheckboxOptionRow.conversion_options_list)
        options.pack(side=tk.LEFT)
        return options

    def create_lens_option_menu(self):
        label_text = "Lens no. "
        label = tk.Label(master=self, text=label_text)
        label.pack(side=tk.LEFT)
        self.lens_option_value = self.get_lens_option_value()
        options = tk.OptionMenu(self, self.lens_option_value, *list(CheckboxOptionRow.lens_options_list.keys()))
        options.pack(side=tk.LEFT)
        return options
    
    def get_option_values(self):
        lens_number_option = int(self.lens_option_value.get())
        lens_option = CheckboxOptionRow.lens_options_list[lens_number_option]
        conversion_option = self.conversion_option_value.get()
        distance_input_value = float(self.distance_value_input.get()) + lens_option.x
        return lens_option, conversion_option, distance_input_value
    
    def delete_option_row(self):
        self.conversion_option_menu.destroy()
        self.lens_option_menu.destroy()
        self.label.destroy()
        self.destroy()




class LensConversionCheckbox(tk.Toplevel):

    def __init__(self, sketch, event, creating_point=False, creating_aperture=False, creating_lens=False):
        super().__init__(master=sketch.master)
        self.sketch = sketch
        self.event = event
        self.creating_point = creating_point
        self.creating_aperture = creating_aperture
        self.creating_lens = creating_lens

        self.option_rows = []
        self.input = {}
        self.distance_input = {}
        self.button = self.create_proceed_button()
        self.option_row = self.create_option_row()
        
        

    def create_option_row(self):
        if len(self.sketch.project.lenses) == 0:
            self.delete_checkbox()
            return self.create_object()
        else:
            option_row = CheckboxOptionRow(self)
            option_row.pack(side=tk.TOP)
            return option_row


    def create_proceed_button(self):
        button = tk.Button(master=self, text="OK", command=self.process_input)
        button.pack(side=tk.BOTTOM)
        button.focus_set()
        return button
    
    def process_input(self):
        lens_input, conversion_input, distance_input = self.option_row.get_option_values()
        self.input.update({lens_input : conversion_input})
        self.distance_input = distance_input
        self.delete_checkbox()
        self.create_object()


    def create_object(self):
        if self.creating_point:
            return numeric_obj.NumericPoint(self.distance_input, self.sketch.axis.y, self.sketch, lens_conversion_type=self.input)
        elif self.creating_aperture:
            return CreateApertureWindow(self.distance_input, self.sketch.axis.y, self.master, self.sketch, lens_conversion_type=self.input)
        elif self.creating_lens:
            if len(self.sketch.project.user_defined_lenses) > 0:
                return CreateLensWindow(self.distance_input, self.sketch.axis.y, self.master, self.sketch, lens_conversion_type=self.input)
            else:
                return CreateLensWindow(self.event.x, self.sketch.axis.y, self.master, self.sketch)


    def delete_checkbox(self):
        for option_row in self.option_rows:
            option_row.delete_option_row()
        self.button.destroy()
        self.destroy()



class CreateApertureWindow(NumericWindow):
    def __init__(self, x, y, master, sketch, lens_conversion_type) -> None:
        super().__init__(x, y, master)
        self.sketch = sketch
        self.lens_conversion_type = lens_conversion_type
        self.window.title("Create aperture")
        self.diameter_label = tk.Label(self.window, text="SET DIAMETER VALUE:")
        self.diameter_label.pack()
        self.diameter_entry = NumericEntry2(10, 10, self.window)
        self.button = self.create_proceed_button()

    def process_values(self):
        diameter = abs(float(self.diameter_entry.entry.get()))
        new_aperture = numeric_obj.NumericAperture(self.x, self.y, self.sketch, diameter, lens_conversion_type=self.lens_conversion_type)
        self.delete_window()
        self.sketch.bind("<ButtonRelease-3>", self.sketch.create_object)



class CreateLensWindow(NumericWindow):
    def __init__(self, x, y, master, sketch, lens_conversion_type=None) -> None:
        super().__init__(x, y, master)
        self.window.title("Create lens")
        self.sketch = sketch
        self.lens_conversion_type = lens_conversion_type
        self.diameter_label = tk.Label(self.window, text="SET DIAMETER VALUE:")
        self.diameter_label.pack()
        self.diameter_entry = NumericEntry2(10, 10, self.window)

        self.focal_label = tk.Label(self.window, text="SET FOCAL VALUE:")
        self.focal_label.pack()
        self.focal_entry = NumericEntry2(10, 10, self.window)

        self.button = self.create_proceed_button()


    def process_values(self):
        diameter = abs(float(self.diameter_entry.entry.get()))
        focal = float(self.focal_entry.entry.get())
        new_lens = numeric_obj.NumericLensObject2(self.x, self.y, self.sketch, diameter, focal, lens_conversion_type=self.lens_conversion_type)
        self.delete_window()
        self.sketch.bind("<ButtonRelease-3>", self.sketch.create_object)