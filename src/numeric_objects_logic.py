import numeric_objects_sprites as sprites
import tkinter as tk
import algorithm as alg



def temp_text(e, entry):
    entry.delete(0, "end")


class Axis:
    main_axis = None

    def __init__(self, sketch, x1, x2, y):
        self.sketch = sketch
        self.y = y
        Axis.main_axis = self
        self.sprite = sprites.Axis(sketch, x1, y, x2, y)


class NumericObject:
    selected = None

    def __init__(self, x, sketch, object_type, item_of, image_of, resulting_of, lens_conversion_type, is_in_infinity) -> None:
        self.x = x
        self.y = sketch.axis.y
        self.sketch = sketch
        self.image_of = image_of
        self.item_of = item_of
        self.resulting_of = resulting_of
        self.resulting_object = None
        self.lens_conversion_type = lens_conversion_type
        self.is_in_infinity = is_in_infinity
        print(lens_conversion_type)
        if lens_conversion_type is not None:
            lens = list(lens_conversion_type.keys())[0]
            if lens is not None:
                lens_index = self.sketch.project.user_defined_lenses.index(lens)
                self.set_object_postfix(lens_index, lens_conversion_type[lens])
            else:
                self.postfix = ""
        else:
            self.postfix = ""
        self.object_type = object_type
        self.type_per_lens = {}
        self.parameters_per_lens = {}
        self.parameters_per_lens2 = {"Item" : None, "Image" : None}
        self.real_object = None
        self.in_real_plane = False
        self.already_converted_by = set()
        self.bound_objects = []
        self.previous = None
        self.next = None
        self.converted_by = None
        self.distance_value = None
        
        #self.is_in_negative_infinity = False
        self.distance_labels = {"left" : None, "right" : None}
        

        self.sprite = None
        self.distance_label = None
        self.object_label = None

        if object_type == "user_defined":
            self.real_object = self

        self.insert_into_list(self.sketch.project.objects)
        self.define_type_per_lenses(sketch.project.user_defined_lenses)

        if len(sketch.project.user_defined_lenses) > 0:
            self.check_real_plane_presence(sketch.project.user_defined_lenses)
            self.get_distance_labels()

        
    def get_distance_labels(self):
        previous_object = self.get_previous_object(self.sketch.project.objects)
        next_object = self.get_next_object(self.sketch.project.objects)

        if previous_object is not None:
            if previous_object.distance_labels["right"] is not None:
                previous_object.distance_labels["right"].delete_label()
                previous_object.distance_labels["right"] = None
                self.distance_labels["left"] = None
            if self.sketch.project.objects.index(previous_object) == 0:
                if previous_object.distance_labels["left"] is not None:
                    previous_object.distance_labels["left"].delete_label()
                    previous_object.distance_labels["left"] = None
            previous_object.distance_labels["right"] = previous_object.draw_distance_label2(self)
            self.distance_labels["left"] = previous_object.distance_labels["right"]

        if next_object is not None:
            if next_object.distance_labels["left"] is not None:
                next_object.distance_labels["left"].delete_label()
                next_object.distance_labels["left"] = None
                self.distance_labels["right"] = None
            if self.sketch.project.objects.index(next_object) == len(self.sketch.project.objects)-1:
                if next_object.distance_labels["right"] is not None:
                    next_object.distance_labels["right"].delete_label()
                    next_object.distance_labels["right"] = None
            next_object.distance_labels["left"] = next_object.draw_distance_label2(self)
            self.distance_labels["right"] = next_object.distance_labels["left"]


    def get_previous_object(self, list):
        current_object = self
        for i, item in enumerate(list):
            if current_object == item:
                if i == 0:
                    return None
                else:
                    return list[i - 1]
        #return list[-2]
    
    def get_next_object(self, list):
        current_object = self
        for i, item in enumerate(list):
            if current_object == item:
                if i == len(list) - 1:
                    return None
                else:
                    return list[i+1]

    def get_nearby_object(self, list):
        current_object = self
        for i, item in enumerate(list):
            if current_object == item:
                if i < len(list) - 1:
                    return list[i+1]
        return list[-2]


    def insert_into_list(self, list):
        #list = self.sketch.project.objects
        for i, list_item in enumerate(list):
            if self.x < list_item.x:
                return list.insert(i, self)
        return list.append(self)


    def check_real_plane_presence(self, lenses):
        if len(lenses) > 0:
            lens = lenses[0]
            if self.x < lens.x:
                return True
            else:
                return False

    def define_parameters_per_lenses(self, lenses):
        for lens in lenses:
            self.define_parameters_per_lens(lens)
    
    def define_parameters_per_lens2(self, lens, conversion_type, position=None):
        values = {}

        if conversion_type == "Item" or conversion_type == "item":
            if self.is_in_infinity:
                values.update({"x": float("inf")})
                values.update({"s": float("inf")})
                values.update({"x'": 0})
                values.update({"s'": lens.focal})
                values.update({"zoom": 0})

                self.parameters_per_lens2.update({"Item": {"Lens": lens, "Values": values}})
            else:
                optical_x = self.x - (lens.x - lens.focal)
                if position is None:
                    optical_s = self.x - lens.x
                else:
                    optical_s = position
                optical_x_prime = alg.NumericCalc.newton_algorithm_x_prime(
                    lens.focal, optical_x
                )
                optical_s_prime = alg.NumericCalc.carthesian_algorithm_s_prime(
                    lens.focal, optical_s
                )
                zoom = alg.NumericCalc.carthesian_zoom(optical_s, optical_s_prime)

                values.update({"x": optical_x})
                values.update({"s": optical_s})
                values.update({"x'": optical_x_prime})
                values.update({"s'": optical_s_prime})
                values.update({"zoom": zoom})

                self.parameters_per_lens2.update({"Item": {"Lens": lens, "Values": values}})


        elif conversion_type == "Image" or conversion_type == "image":
            if self.is_in_infinity:
                values.update({"x": 0})
                values.update({"s": -1*lens.focal})
                values.update({"x'": float("inf")})
                values.update({"s'": float("inf")})
                values.update({"zoom": -1*float("inf")})

                self.parameters_per_lens2.update({"Item": {"Lens": lens, "Values": values}})
            else:
                optical_x_prime = self.x - (lens.x + lens.focal)
                if position is None:
                    optical_s_prime = self.x - lens.x
                else:
                    optical_s_prime = position
                optical_x = alg.NumericCalc.newton_algorithm_x(lens.focal, optical_x_prime)
                optical_s = alg.NumericCalc.carthesian_algorithm_s(
                    lens.focal, optical_s_prime
                )
                zoom = alg.NumericCalc.carthesian_zoom(optical_s, optical_s_prime)

                values.update({"x": optical_x})
                values.update({"s": optical_s})
                values.update({"x'": optical_x_prime})
                values.update({"s'": optical_s_prime})
                values.update({"zoom": zoom})

                self.parameters_per_lens2.update({"Image": {"Lens": lens, "Values": values}})

        self.parameters_per_lens.update({lens: values})

    def redefine_parameters_per_lenses(self, lenses, value):
        for lens in lenses:
            self.define_parameters_per_lens2(self, lens, self.type_per_lens[lens], position=value)

    def define_type_per_lens(self, lens):
        if self.x <= lens.x:
            self.type_per_lens.update({lens: "item"})
        else:
            self.type_per_lens.update({lens: "image"})

    def define_type_per_lenses(self, lenses):
        for lens in lenses:
            self.define_type_per_lens(lens)

    def draw_distance_label(self, sketch, lens):
        if self.type_per_lens[lens] == "item":
            value = abs(self.parameters_per_lens[lens]["s"])

        elif self.type_per_lens[lens] == "image":
            value = abs(self.parameters_per_lens[lens]["s'"])

        label = NumericDistanceLabel(self, lens, self.y - 50, value, sketch)

        return label
    
    def draw_distance_label2(self, object):
        value = abs(self.x - object.x)
        self.distance_value = value
        label = NumericDistanceLabel(self, object, self.y - 50, value, self.sketch)

        return label
    
    def delete_object_manually(self):
        NumericObject.selected = None
        self.delete_object()
        rest_of_objects = self.sketch.project.objects
        for index, item in enumerate(rest_of_objects[1:]):
            if index % 2 == 0:
                item.get_distance_labels()

    def delete_bound_rays(self):
        if isinstance(self, NumericPoint):
            if self.bound_field_ray is not None:
                self.bound_field_ray.delete_ray()
                self.bound_field_ray = None
            
            if self.bound_aperture_ray is not None:
                self.bound_aperture_ray.delete_ray()
                self.bound_aperture_ray = None

        elif isinstance(self, NumericAperture) or isinstance(self, NumericLensObject2):
            if len(self.bound_field_rays) > 0:
                for ray in self.bound_field_rays:
                    ray.delete_ray()
                self.bound_field_rays.clear()
            
            if len(self.bound_aperture_rays) > 0:
                for ray in self.bound_aperture_rays:
                    ray.delete_ray()
                self.bound_aperture_rays.clear()


    def delete_bound_objects(self):
        if self.item_of is not None:
            self.item_of.image_of = None
            self.item_of.delete_object()
            self.item_of = None
        if self.image_of is not None:
            self.image_of.item_of = None
            self.image_of.delete_object()
            self.image_of = None


    def delete_object(self):
        if self.item_of is not self and self.image_of is not self:
            self.delete_bound_objects()
        self.sprite.delete_sprite()

        if self.distance_labels["left"] is not None:
            self.distance_labels["left"].delete_label()
            previous_object = self.get_previous_object(self.sketch.project.objects)
            previous_object.distance_labels["right"] = None
        if self.distance_labels["right"] is not None:
            self.distance_labels["right"].delete_label()
            next_object = self.get_next_object(self.sketch.project.objects)
            next_object.distance_labels["left"] = None
                
        previous_object = self.get_previous_object(self.sketch.project.objects)
        if self.object_label is not None:
            self.object_label.delete_label()
        self.sketch.project.objects.remove(self)
        if previous_object is not None:
            if previous_object.distance_label is not None:
                previous_object.distance_label.delete_label()
                previous_object.get_distance_labels()

        self.delete_bound_rays()
            

        if isinstance(self, NumericAperture):
            if self in self.sketch.project.user_defined_apertures:
                self.sketch.project.user_defined_apertures.remove(self)
            if self in self.sketch.project.apertures:
                self.sketch.project.apertures.remove(self)
            if self in self.sketch.project.resulting_apertures:
                self.sketch.project.resulting_apertures.pop(self)
        if isinstance(self, NumericLensObject2):
            if self in self.sketch.project.user_defined_lenses:
                self.sketch.project.user_defined_lenses.remove(self)
            if self in self.sketch.project.lenses:
                self.sketch.project.lenses.remove(self)
            if self in self.sketch.project.resulting_lenses:
                self.sketch.project.resulting_lenses.pop(self)
            if self in self.sketch.project.user_defined_apertures:
                self.sketch.project.user_defined_apertures.remove(self)
            if self in self.sketch.project.apertures:
                self.sketch.project.apertures.remove(self)
            if self in self.sketch.project.resulting_apertures:
                self.sketch.project.resulting_apertures.pop(self)
        if isinstance(self, NumericPoint):
            if self in self.sketch.project.user_defined_points:
                self.sketch.project.user_defined_points.remove(self)
            if self in self.sketch.project.points:
                self.sketch.project.points.remove(self)
            if self in self.sketch.project.resulting_points:
                self.sketch.project.resulting_points.pop(self)
        
        self.sketch.project.object_properties.remove_properties_row(self)
        #self.sketch.project.objects.remove(self)


    def get_object_label(self):
        if isinstance(self, NumericPoint):
            return NumericPointLabel(
                self, self.sketch, self.type_per_lens[self.sketch.lens]
            )
        elif isinstance(self, NumericAperture):
            return NumericApertureLabel(self, self.sketch, self.type_per_lens[self.sketch.lens])
        elif isinstance(self, NumericLensObject2):
            return NumericLensLabel(
                self, self.sketch, self.type_per_lens[self.sketch.lens]
            )


    def change_distance(self, value=150):
        lens = list(self.lens_conversion_type.keys())[0]
        lens_conversion_type = self.lens_conversion_type
        self.delete_object()
        self.delete_bound_objects()
        self.x = lens.x + value
        self.lens_conversion_type = lens_conversion_type
        
        self.define_type_per_lens(lens)
        self.sprite.redraw()
        self.object_label = self.get_object_label()
        #self.define_parameters_per_lens2(self.sketch.lens, self.type_per_lens[self.sketch.lens], position=value)
        self.define_parameters_per_lens2(lens, self.type_per_lens[lens], position=value)
        
        self.insert_into_list(self.sketch.project.objects)
        self.convert_object_per_lens()
        if isinstance(self, NumericAperture) or isinstance(self, NumericLensObject2):
            if isinstance(self, NumericLensObject2):
                self.insert_into_list(self.sketch.project.user_defined_lenses)
            self.insert_into_list(self.sketch.project.user_defined_apertures)
        self.get_distance_labels()
        self.bind_select_object()
        self.sketch.project.object_properties.create_properties_row(self)

    def set_distance_value(self, distance_label, sketch, lens):
        frame = tk.Frame(master=sketch.master, width=100)
        entry = tk.Entry(master=frame, width=5, bd=3)
        entry.pack()
        value = str(self.x - lens.x)
        entry.insert(0, value)
        window = sketch.create_window(
            (distance_label.object_1.x + distance_label.object_2.x) / 2, distance_label.y, window=frame
        )
        entry.bind("<FocusIn>", lambda event: temp_text(event, entry))
        entry.bind(
            "<Return>",
            lambda event: self.process_distance_entry_value(entry, sketch, window),
        )

    def process_distance_entry_value(self, entry, sketch, window):
        try:
            value = float(entry.get())
            self.change_distance(value)
            sketch.delete(window)
        except ValueError:
            sketch.delete(window)
    

    def bind_select_object(self):
        self.sprite.bind_select_object()

    def bind_delete_object(self):
        self.sprite.bind_delete_object()

    def unbind_all(self):
        self.sprite.unbind_all()

    def select_object(self):
        if NumericObject.selected != None:
            NumericObject.selected.bind_select_object()
        NumericObject.selected = self
        self.unbind_all()
        self.bind_delete_object()


    def set_object_postfix(self, lens_index, conversion_type):
        if conversion_type == "Image":
            postfix = "'"
        else:
            postfix = ""
        for i in range(lens_index):

            postfix += "'"
        self.postfix = postfix


    def convert_object_per_lens(self):
        lens = list(self.lens_conversion_type.keys())[0]
        if lens is None:
            return
        else:
            conversion_type = self.lens_conversion_type[lens]
            print(f"{lens} -> {conversion_type}")
            lens_index = self.sketch.project.user_defined_lenses.index(lens)
            self.set_object_postfix(lens_index, conversion_type)
            #if conversion_type == "Item":
            self.define_parameters_per_lens2(lens, conversion_type)        
            self_resulting_object = self.convert_object(lens, conversion_type)
            
            if conversion_type == "Item" or conversion_type == "item":
                resulting_object = self_resulting_object
            elif conversion_type == "Image" or conversion_type == "image":
                resulting_object = self
            for next_lens in self.sketch.project.user_defined_lenses[lens_index+1:]:
                resulting_object.define_parameters_per_lens2(next_lens, "Item")
                resulting_object = resulting_object.convert_object(next_lens, "Item")

            rest_of_list = self.sketch.project.user_defined_lenses[:lens_index]
            rest_of_list.reverse()

            #   TO POD SPODEM WAZNE BO MUSZA BYC PARAMETRY DLA ODWROTNYCH OPERACJI
            #if len(rest_of_list) > 0:
            if conversion_type == "Item" or conversion_type == "item":
                resulting_object = self
            elif conversion_type == "Image" or conversion_type == "image":
                resulting_object = self_resulting_object

                #self.define_parameters_per_lens2(rest_of_list[0], "Image")
            for previous_lens in rest_of_list:
                resulting_object.define_parameters_per_lens2(previous_lens, "Image")        
                resulting_object = resulting_object.convert_object(previous_lens, "Image")


    def convert_object(self, lens, conversion_type):
        sketch = self.sketch
        if lens not in self.real_object.already_converted_by:
            self.real_object.already_converted_by.add(lens)
        if conversion_type == "Item":
            self.item_of = self.determine_image(sketch, lens)
            self.resulting_object = self.item_of
            self.item_of.real_object = self.real_object
            if isinstance(self, NumericPoint):
                self.update_resulting_list(self.item_of)
            
            lens.converted_user_defined_objects.update({self.real_object: {"Item": self, "Image": self.item_of}})

            return self.item_of

        elif conversion_type == "Image":
            self.image_of = self.determine_item(sketch, lens)
            self.resulting_object = self.item_of
            self.image_of.real_object = self.real_object
            if isinstance(self, NumericPoint):
                self.update_resulting_list(self.image_of)

            lens.converted_user_defined_objects.update({self.real_object: {"Image": self, "Item": self.image_of}})

            return self.image_of


    def get_real_plane_object(self, boundary_lens):
        current_object = self
        if isinstance(self, NumericPoint):
            while current_object.image_of is not None:
                current_object = current_object.image_of
            self.sketch.project.real_plane_points.append(current_object)
            return current_object
        elif isinstance(self, NumericLensObject2):
            if current_object is boundary_lens:
                self.sketch.project.real_plane_lenses.append(current_object)
                self.sketch.project.real_plane_apertures.append(current_object)
            else:
                while current_object.image_of is not None:
                    current_object = current_object.image_of
                self.sketch.project.real_plane_lenses.append(current_object)
                self.sketch.project.real_plane_apertures.append(current_object)
        elif isinstance(self, NumericAperture):
            while current_object.image_of is not None:
                current_object = current_object.image_of
            self.sketch.project.real_plane_apertures.append(current_object)

    
    def get_real_plane_point(self, boundary_lens):
        current_object = self

    def get_real_plane_aperture(self, boundary_lens):
        current_object = self
        while current_object.x > boundary_lens.x:
            current_object = current_object.image_of
            if current_object is None:
                return
        self.sketch.project.real_plane_apertures.append(current_object)

    def get_real_plane_lens(self, boundary_lens):
        current_object = self
        if current_object is boundary_lens:
            self.sketch.project.real_plane_lenses.append(current_object)
        else:
            while current_object.x > boundary_lens.x:
                current_object = current_object.image_of
                if current_object is None:
                    return
            self.sketch.project.real_plane_lenses.append(current_object)



class NumericPoint(NumericObject):
    selected = None

    def __init__(
        self,
        x,
        y,
        sketch,
        color="black",
        object_type="user_defined",
        item_of=None,
        image_of=None,
        resulting_of = None,
        lens_conversion_type={},
        is_in_infinity = False
    ) -> None:
        super().__init__(x, sketch, object_type, item_of, image_of, resulting_of, lens_conversion_type, is_in_infinity)
        # self.y = sketch.axis.y - 5
        self.color = color
        self.bound_aperture_ray = None
        self.bound_field_ray = None

        self.number = len(sketch.project.user_defined_points) + 1
        
        self.sprite = sprites.Point(self)
        #self.sprite.image = self.draw(sketch)

        self.object_label = NumericPointLabel(
            self, sketch, self.type_per_lens[sketch.lens]
        )
        #self.distance_label = self.draw_distance_label(sketch, sketch.lens)
        self.bind_select_object()

        self.add_to_lists()

        if self.real_object is not None:
            print(self.real_object.already_converted_by)

    def __del__(self):
        ...

    def __str__(self) -> str:
        return f"Point no. {self.number}{self.postfix}"

    def add_to_lists(self):
        if self.object_type == "user_defined":
            self.convert_object_per_lens()
            self.sketch.project.user_defined_points.append(self)

        self.sketch.project.points.append(self)
        self.sketch.project.object_properties.create_properties_row(self)


    def update_resulting_list(self, resulting_point):
        self.sketch.project.resulting_points.update({self : resulting_point})


    def determine_image(self, sketch, lens):
        determined_x = self.parameters_per_lens[lens]["s'"] + lens.x
        determined_y = (
            sketch.axis.y
            + (self.y - sketch.axis.y) * self.parameters_per_lens[lens]["zoom"]
        )

        print(f"determined x of {self}: {determined_x}")
        print(determined_x == float("-inf") or determined_x == float("inf"))
        # determined_diameter = self.diameter * abs(self.parameters_per_lens[lens]["zoom"])
        #if determined_x == "-inf" or
        if determined_x == float("-inf") or determined_x == float("inf"):
            image = NumericPoint(
                determined_x, determined_y, sketch, self.color, object_type="resulting", image_of = self, resulting_of=self,
                lens_conversion_type={lens.get_next_object(self.sketch.project.user_defined_lenses) : "Item"},
                is_in_infinity=True
            )
        else:
            image = NumericPoint(
                determined_x, determined_y, sketch, self.color, object_type="resulting", image_of = self, resulting_of=self,
                lens_conversion_type={lens.get_next_object(self.sketch.project.user_defined_lenses) : "Item"}
            )
        image.number = self.number
        lens_index = self.sketch.project.user_defined_lenses.index(lens)
        image.set_object_postfix(lens_index, "Image")
        image.object_label.update_label_text()

        return image

    def determine_item(self, sketch, lens):
        if self.is_in_infinity:
            determined_x = lens.x - lens.focal
            determined_y = self.y
        else:
            determined_x = self.parameters_per_lens[lens]["s"] + lens.x
            if self.parameters_per_lens[lens]["zoom"] == 0:
                determined_y = float("inf")
            else:
                determined_y = (
                    sketch.axis.y
                    + (self.y - sketch.axis.y) / self.parameters_per_lens[lens]["zoom"]
                )
        # determined_diameter = self.diameter * abs(self.parameters_per_lens[lens]["zoom"])
        if determined_x == float("-inf") or determined_x == float("inf"):
            item = NumericPoint(
                determined_x, determined_y, sketch, self.color, object_type="resulting", item_of = self, resulting_of=self,
                lens_conversion_type={lens.get_previous_object(self.sketch.project.user_defined_lenses) : "Image"},
                is_in_infinity=True
            ) 
        else:
            item = NumericPoint(
                determined_x, determined_y, sketch, self.color, object_type="resulting", item_of = self, resulting_of=self,
                lens_conversion_type={lens.get_previous_object(self.sketch.project.user_defined_lenses) : "Image"}
            )   
        """item = NumericPoint(
            determined_x, determined_y, sketch, self.color, object_type="resulting", item_of = self, resulting_of=self,
            lens_conversion_type={lens.get_previous_object(self.sketch.project.user_defined_lenses) : "Image"}
        )  """ 
        item.number = self.number
        lens_index = self.sketch.project.user_defined_lenses.index(lens)
        item.set_object_postfix(lens_index, "Item")
        item.object_label.update_label_text()

        return item

    @staticmethod
    def erase_point(point):
        print("ERASING POINT")
        del point



class NumericDistanceLabel:
    selected = None

    def __init__(self, object_1, object_2, y, value, sketch):
        self.object_1 = object_1
        self.object_2 = object_2
        self.y = y
        self.value = value
        self.distance = NumericDistance(object_1.x, object_2.x, y, sketch)

        # self.text = NumericText(object_1.x, object_2.x, y, f"{ "%.1f" % value}", sketch)
        self.text = NumericText(object_1.x, object_2.x, y, f"{value:0,.1f}", sketch)
        self.bind_select_option(sketch)

    def __del__(self):
        print("DELETED DISTANCE LABEL")

    def bind_select_option(self, sketch):
        self.distance.canvas.unbind("<Button-1>")
        self.distance.canvas.bind("<Button-1>", lambda event: self.select_label(sketch))

    def delete_label(self):
        self.distance.delete_distance()
        #del self.distance
        self.text.delete_text()
        #del self.text

    def select_label(self, sketch):
        NumericDistanceLabel.selected = self
        print(f"SELECTED {NumericDistanceLabel.selected}")
        sketch.unbind("<ButtonRelease-1>")
        sketch.bind(
            "<ButtonRelease-1>", lambda event: self.move_label(event, sketch)
        )

    def move_label(self, event, sketch):
        self.distance.canvas.unbind("<ButtonRelease-1>")
        sketch.unbind("<ButtonRelease-1>")
        print(f"MOVED {NumericDistanceLabel.selected} FROM {self.y} TO {event.y}")
        self.y = event.y
        NumericDistanceLabel.selected = None
        self.distance.place_canvas(self.object_1.x, self.object_2.x, self.y)
        self.text.place_canvas(self.object_1.x, self.object_2.x, self.y)
        print(f"SELECTED {NumericDistanceLabel.selected}")

    def bind_change_distance(self, numeric_object):
        self.text.canvas.tag_bind(
                    self.text.text_id,
                    "<Button-1>",
                    lambda event: numeric_object.set_distance_value(self, numeric_object.sketch, lens = list(numeric_object.lens_conversion_type.keys())[0]),
                )


class NumericDistance:
    def __init__(self, x1, x2, y, sketch):
        self.sketch = sketch
        self.canvas = tk.Canvas(
            master=sketch,
            width=abs(x1 - x2) - 3,
            height=3,
            background="white",
            highlightthickness=0,
        )
        self.line_2 = self.draw_line(x1, x2)
        self.place_canvas(x1, x2, y)

    def __del__(self):
        ...

    def draw_line(self, x1, x2):
        if x1 <= x2:
            return self.canvas.create_line(
                0, 1, abs(x2 - x1), 1, fill="dark green", width=1
            )
        else:
            return self.canvas.create_line(
                0, 1, abs(x2 - x1), 1, fill="dark green", width=1
            )

    def place_canvas(self, x1, x2, y):
        if x1 <= x2:
            self.canvas.place(x=x1 + 2, y=y)
        else:
            self.canvas.place(x=x2 + 2, y=y)

    def delete_distance(self):
        self.canvas.destroy()


class NumericText:
    def __init__(self, x1, x2, y, text, sketch, bd=0):
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.text = text
        self.sketch = sketch
        self.canvas = tk.Canvas(
            master=sketch,
            width=self.determine_width(text),
            height=12,
            background="white",
            highlightthickness=bd,
            highlightbackground="black",
        )
        self.text_id = self.draw_text()
        self.place_canvas(x1, x2, y)

    def __del__(self):
        ...

    def draw_text(self):
        return self.canvas.create_text(
            self.determine_width(self.text) / 2,
            6,
            text=self.text,
            fill="black",
            font=("Helvetica 8"),
            anchor=tk.CENTER,
        )

    def determine_width(self, text):
        return 7 * len(str(text))

    def place_canvas(self, x1, x2, y):
        self.canvas.place(
            x=(x2 + x1) / 2 - self.determine_width(self.text) / 2, y=y - 5
        )
        self.y = y

    def delete_text(self):
        self.canvas.destroy()

    def update_text(self):
        self.canvas.delete(self.text_id)
        self.text_id = self.draw_text()



class NumericPointLabel:
    def __init__(self, point: NumericPoint, sketch, type="image"):
        self.point = point
        self.sketch = sketch
        self.type = type
        self.y = self.define_number_y_position()
        self.number_label = self.define_point_number_label()
        # self.diameter_label = self.define_aperture_diameter_label(point, sketch)
        # self.value = NumericText(x1, x2, y, f"{value}", sketch)

    def __del__(self):
        print("DELETED APERTURE LABEL")

    def define_number_y_position(self):
        return self.point.y - 15

    def define_point_number_label(self):
        point = self.point
        sketch = self.sketch
        # if self.type == "image":
        # return NumericText(point.x, point.x, self.y, f"P{len(self.sketch.project.points)}'", sketch, bd=1)
        # if self.type == "item":
        # return NumericText(point.x, point.x, self.y, f"P{len(self.sketch.project.points)}", sketch, bd=1)
        return NumericText(
            point.x, point.x, self.y, f"P{point.number}{point.postfix}", sketch, bd=1
        )

    # def define_aperture_diameter_label(self, aperture, sketch):
    # return NumericText(aperture.x-1, aperture.x+2, self.number_label.y-15, f"Ø: {aperture.diameter}'", sketch, bd=1)

    def delete_label(self):
        self.number_label.delete_text()
        # self.diameter_label.delete_text()
        del self

    def update_label_text(self):
        self.number_label.delete_text()
        self.number_label = self.define_point_number_label()













class NumericAperture(NumericObject):
    selected = None

    def __init__(
        self,
        x,
        y,
        sketch,
        diameter,
        object_type="user_defined",
        item_of=None,
        image_of=None,
        resulting_of = None,
        color="black",
        lens_conversion_type={},
        is_in_infinity = False
    ) -> None:
        super().__init__(x, sketch, object_type, item_of, image_of, resulting_of, lens_conversion_type, is_in_infinity)
        self.diameter = diameter
        self.color = color
        self.bound_aperture_rays = []
        self.bound_field_rays = []
        
        self.number = len(sketch.project.user_defined_apertures) + 1

        #self.sprite = self.draw(sketch)
        self.sprite = sprites.NumericAperture(self)
        self.object_label = NumericApertureLabel(
            self, sketch, self.type_per_lens[sketch.lens]
        )
        #self.distance_label = self.draw_distance_label(sketch, sketch.lens)

        """self.image = self.define_image(sketch)"""
        self.bind_select_object()

        self.add_to_lists()
    

    def __del__(self):
        print("deleted aperture")


    def __str__(self) -> str:
        return f"Aperture no. {self.number}{self.postfix}"

    def add_to_lists(self):
        if self.object_type == "user_defined":
            self.convert_object_per_lens()
            self.sketch.project.resulting_apertures.update({self : self.item_of})
            self.insert_into_list(self.sketch.project.user_defined_apertures)
            NumericAperture.get_real_plane_apertures(self.sketch.project)

        self.sketch.project.apertures.append(self)
        self.sketch.project.object_properties.create_properties_row(self)


    def update_resulting_list(self, resulting_aperture):
        self.sketch.project.resulting_apertures.update({self : resulting_aperture})


    def convert(self, lens):
        if self.x < lens.x:
            self.item_of = self.determine_image(self.sketch, lens)
            self.item_of.image_of = self
            self.item_of.real_object = self
            self.item_of.postfix = alg.NumericCalc.determine_object_postfix(
                self.item_of
            )
            self.item_of.number = self.number
            self.item_of.object_label.update_label_text()
            self.postfix = alg.NumericCalc.determine_object_postfix(self)
            self.object_label.update_label_text()

        else:
            self.image_of = self.determine_item(self.sketch, lens)
            self.image_of.item_of = self
            self.image_of.real_object = self
            self.image_of.postfix = alg.NumericCalc.determine_object_postfix(
                self.image_of
            )
            self.image_of.number = self.number
            self.image_of.object_label.update_label_text()
            self.postfix = alg.NumericCalc.determine_object_postfix(self)
            self.object_label.update_label_text()
            # self.postfix += "'"

    def convert_per_lens(self):
        for lens in self.sketch.project.lenses:
            print(lens)
            self.convert(lens)

    def determine_image(self, sketch, lens):
        determined_x = self.parameters_per_lens[lens]["s'"] + lens.x
        determined_y = self.y
        determined_diameter = self.diameter * abs(
            self.parameters_per_lens[lens]["zoom"]
        )
        if determined_x == float("-inf") or determined_x == float("inf"):
            image = NumericAperture(
                determined_x,
                determined_y,
                sketch,
                determined_diameter,
                object_type="resulting",
                image_of = self,
                resulting_of=self,
                lens_conversion_type={lens : "Image"},
                is_in_infinity=True
            )
        else:
            image = NumericAperture(
                determined_x,
                determined_y,
                sketch,
                determined_diameter,
                object_type="resulting",
                image_of = self,
                resulting_of=self,
                lens_conversion_type={lens : "Image"}
            )
        image.number = self.number
        image.object_label.update_label_text()
        return image

    def determine_item(self, sketch, lens):
        determined_x = self.parameters_per_lens[lens]["s"] + lens.x
        determined_y = self.y
        determined_diameter = self.diameter / abs(
            self.parameters_per_lens[lens]["zoom"]
        )
        if determined_x == float("-inf") or determined_x == float("inf"):
            item = NumericAperture(
                determined_x,
                determined_y,
                sketch,
                determined_diameter,
                object_type="resulting",
                item_of = self,
                resulting_of=self,
                lens_conversion_type={lens : "Item"},
                is_in_infinity=True
            )
        else:
            item = NumericAperture(
                determined_x,
                determined_y,
                sketch,
                determined_diameter,
                object_type="resulting",
                item_of = self,
                resulting_of=self,
                lens_conversion_type={lens : "Item"}
            )
        item.number = self.number
        item.object_label.update_label_text()
        return item

    """def delete_object_manually(self):
        NumericAperture.selected = None
        self.delete_bound_objects()
        self.delete_object()
        NumericAperture.erase_aperture(self)"""

    """def redraw(self, sketch):
        return self.draw(sketch)"""

    def select_aperture(self):
        print(f"SELECTED {self}")
        if NumericAperture.selected != None:
            NumericAperture.selected.bind_select_object()
        NumericAperture.selected = self
        self.bind_delete_object()


    @staticmethod
    def get_real_plane_apertures(project):
        user_defined_apertures = project.user_defined_apertures
        real_plane_apertures = project.real_plane_apertures
        real_plane_apertures.clear()
        boundary_lens = project.user_defined_lenses[0]
        print(f"BOUNDARY LENS: {boundary_lens}")
        #real_plane_apertures.append(boundary_lens)
        if len(user_defined_apertures) >= 1:
            for aperture in user_defined_apertures:
                aperture.get_real_plane_aperture(boundary_lens)

    @staticmethod
    def erase_aperture(aperture):
        del aperture




class NumericApertureLabel:
    def __init__(self, aperture: NumericAperture, sketch, type="image"):
        self.aperture = aperture
        self.sketch = sketch
        self.type = type
        self.y = self.define_number_y_position()
        self.number_label = self.define_aperture_number_label()
        #self.diameter_label = self.define_aperture_diameter_label()
        # self.value = NumericText(x1, x2, y, f"{value}", sketch)

    def __del__(self):
        print("DELETED APERTURE LABEL")

    def define_number_y_position(self):
        return self.sketch.axis.y - self.aperture.diameter / 2 - 15

    def define_aperture_number_label(self):
        aperture = self.aperture
        sketch = self.sketch
        # if self.type == "image":
        # return NumericText(aperture.x, aperture.x, self.y, f"{len(sketch.project.apertures)+1}'", sketch, bd=1)
        # if self.type == "item":
        # return NumericText(aperture.x, aperture.x, self.y, f"{len(sketch.project.apertures)+1}", sketch, bd=1)
        return NumericText(
            aperture.x,
            aperture.x,
            self.y,
            f"{aperture.number}{aperture.postfix}",
            sketch,
            bd=1,
        )

    def define_aperture_diameter_label(self):
        aperture = self.aperture
        sketch = self.sketch
        return NumericText(
            aperture.x - 1,
            aperture.x + 2,
            self.number_label.y - 15,
            f"Ø: {aperture.diameter}'",
            sketch,
            bd=1,
        )

    def delete_label(self):
        self.number_label.delete_text()
        #self.diameter_label.delete_text()
        del self

    def update_label_text(self):
        self.number_label.delete_text()
        self.number_label = self.define_aperture_number_label()



class NumericRay:

    selected = None

    def __init__(self, sketch, middle_point_object, edge_point_object, left_object, right_object, factor, former_linear_factor, former_ray_end, object_type):
        self.sketch = sketch
        self.middle_point_object = middle_point_object
        self.edge_point_object = edge_point_object
        self.left_object = left_object
        self.right_object = right_object
        self.factor = factor
        self.former_linear_factor = former_linear_factor
        self.former_ray_end = former_ray_end
        self.object_type = object_type
        self.bound_aperture_ray = None
        self.bound_field_ray = None

        self.linear_function = self.linear_function_of_ray()
        self.ray_coords = self.get_ray_coords()


    def linear_function_of_ray(self):
        if self.middle_point_object.x == float("inf"):
            x1 = self.left_object.x
            y1 = self.former_ray_end[1]
        elif self.middle_point_object.x == float("-inf"):
            x1 = self.left_object.x
            y1 = self.former_ray_end[1]
        else:
            x1 = self.middle_point_object.x
            y1 = self.middle_point_object.y
        if self.edge_point_object.x == float("inf"):
            x2 = self.left_object.x
            y2 = self.former_ray_end[1]
        elif self.edge_point_object.x == float("-inf"):
            x2 = self.left_object.x
            y2 = self.former_ray_end[1]
        else:
            x2 = self.edge_point_object.x
            if isinstance(self, NumericApertureRay):
                if self.former_ray_end is not None:
                    print(f"{self.former_ray_end[1]} vs {self.edge_point_object.y + self.factor*self.edge_point_object.diameter/2}")
                    if self.former_ray_end[1] == self.edge_point_object.y + self.factor*self.edge_point_object.diameter/2:
                        y2 = self.edge_point_object.y + self.factor*self.edge_point_object.diameter/2
                    elif self.former_ray_end[1] == self.edge_point_object.y - self.factor*self.edge_point_object.diameter/2:
                        y2 = self.edge_point_object.y - self.factor*self.edge_point_object.diameter/2
                    elif self.former_ray_end[1] > y1:
                        if self.left_object is not None:
                            if self.left_object.x > self.middle_point_object.x:
                                if self.edge_point_object.x > self.middle_point_object.x:
                                    y2 = self.edge_point_object.y + self.factor*self.edge_point_object.diameter/2
                                else:
                                    y2 = self.edge_point_object.y - self.factor*self.edge_point_object.diameter/2
                            else:
                                if self.edge_point_object.x > self.middle_point_object.x:
                                    y2 = self.edge_point_object.y - self.factor*self.edge_point_object.diameter/2
                                else:
                                    y2 = self.edge_point_object.y + self.factor*self.edge_point_object.diameter/2
                        else:
                            y2 = self.edge_point_object.y + self.factor*self.edge_point_object.diameter/2
                    else:
                        if self.left_object is not None:
                            if self.left_object.x > self.middle_point_object.x:
                                if self.edge_point_object.x > self.middle_point_object.x:
                                    y2 = self.edge_point_object.y - self.factor*self.edge_point_object.diameter/2
                                else:
                                    y2 = self.edge_point_object.y + self.factor*self.edge_point_object.diameter/2
                            else:
                                if self.edge_point_object.x > self.middle_point_object.x:
                                    y2 = self.edge_point_object.y + self.factor*self.edge_point_object.diameter/2
                                else:
                                    y2 = self.edge_point_object.y - self.factor*self.edge_point_object.diameter/2
                        else:
                            y2 = self.edge_point_object.y + self.factor*self.edge_point_object.diameter/2
                    
                else:
                    y2 = self.edge_point_object.y + self.factor*self.edge_point_object.diameter/2

            elif isinstance(self, NumericFieldRay):
                if self.former_ray_end is not None:
                    if self.former_ray_end[1] == self.edge_point_object.y + self.factor*self.edge_point_object.diameter/2:
                        y2 = self.edge_point_object.y + self.factor*self.edge_point_object.diameter/2
                    elif self.former_ray_end[1] == self.edge_point_object.y - self.factor*self.edge_point_object.diameter/2:
                        y2 = self.edge_point_object.y - self.factor*self.edge_point_object.diameter/2
                    elif self.former_ray_end[1] == self.middle_point_object.y:
                        y2 = self.edge_point_object.y - self.factor*self.edge_point_object.diameter/2
                    else:
                        y2 = self.edge_point_object.y - self.factor*self.edge_point_object.diameter/2
                else:
                    y2 = self.edge_point_object.y + self.factor*self.edge_point_object.diameter/2
        
        divider = x2 - x1
        if divider != 0:
            if self.former_ray_end is not None:
                object_in_infinity = self.edge_point_object.x == float("inf") or self.edge_point_object.x == float("-inf")
                if y1 == self.former_ray_end[1] and self.right_object is None and object_in_infinity:
                    return {"a": 1, "b": y1}
                else:
                    return {"a": (y2 - y1) / (x2 - x1), "b": y1}
            else:
                return {"a": (y2 - y1) / (x2 - x1), "b": y1}
        else:
            return {"a": float("inf"), "b": y1}

        
    
    def get_ray_coords(self):
        coords = []
        if self.left_object is None:
            x1 = 0
        else:
            x1 = self.left_object.x
        print(self.linear_function['a'])
        """if self.linear_function['a'] == 0:
            #self.former_ray_end[1]
        else:"""
        #if self.edge_point_object.x == float("inf") or self.edge_point_object.x == float("-inf"):
        if self.linear_function['a'] == 1:
            coords.append((x1, self.linear_function['b']))
        else:
            coords.append((x1, self.linear_function['a']*(x1-self.middle_point_object.x) + self.linear_function['b']))
        if self.right_object is None:
            x2 = self.sketch.width
        else:
            x2 = self.right_object.x
        
        #if self.edge_point_object.x == float("inf") or self.edge_point_object.x == float("-inf"):
        if self.linear_function['a'] == 1:
            coords.append((x2, self.linear_function['b']))
        else:
            coords.append((x2, self.linear_function['a']*(x2-self.middle_point_object.x) + self.linear_function['b']))

        return coords
    

    def delete_bound_rays(self):
        if self.bound_aperture_ray is not None:
            self.bound_aperture_ray.bound_field_ray = None
            self.bound_aperture_ray.delete_ray()
            self.bound_aperture_ray = None
        if self.bound_field_ray is not None:
            self.bound_field_ray.bound_aperture_ray = None
            self.bound_field_ray.delete_ray()
            self.bound_field_ray = None


    def delete_ray(self):
        self.delete_bound_rays()
        for ray in self.complementary_rays:
            ray.sprite.delete()
        self.sprite.delete()


    def delete_ray_manually(self):
        NumericRay.selected = None
        self.delete_ray()

    def select_ray(self):
        print(f"SELECTED {self}")
        if NumericRay.selected != None:
            NumericRay.selected.sprite.bind_select_ray()
        NumericRay.selected = self
        self.sprite.bind_delete_ray()

"""class NumericRay:
    def __init__(self, sketch, object_1, object_2):
        self.sketch = sketch
        self.object_1 = object_1
        self.object_2 = object_2"""


class NumericApertureRay(NumericRay):
    def __init__(self, sketch, point, aperture, left_object=None, right_object=None, factor=1, former_linear_factor=None, former_ray_end=None, object_type="user_defined"):
        super().__init__(sketch, point, aperture, left_object, right_object, factor, former_linear_factor, former_ray_end, object_type)
        self.sketch = sketch
        self.point = point
        print(f"POINT: {self.point}")
        self.aperture = aperture
        print(f"APERTURE: {self.aperture}")
        
        self.complementary_rays = []

        self.sprite = sprites.NumericApertureRay(self)
        
        if self.object_type == "user_defined":
            #self.extend_ray()
            self.middle_point_object.bound_aperture_ray = self
            self.edge_point_object.bound_aperture_rays.append(self)
            self.get_complete_ray()
            self.sketch.project.aperture_rays.append(self)

            print(f"ITS MEMBERS: {self.middle_point_object} -> {self.middle_point_object.bound_aperture_ray}, {self.edge_point_object} -> {self.edge_point_object.bound_aperture_rays}")
        
        
    def __str___(self):
        print("Aperture ray")

    
    def extend_ray(self, point_image, aperture_image, linear_factor, ray_end, left_object=None, right_object=None):
        new_ray = NumericApertureRay(self.sketch, point_image, aperture_image, left_object=left_object, right_object=right_object, former_linear_factor=linear_factor, former_ray_end=ray_end, object_type="resulting")
        self.complementary_rays.append(new_ray)


    def get_complete_ray(self):
        point = self.point
        aperture = self.aperture
        lenses_list = self.sketch.project.user_defined_lenses
        if len(lenses_list) > 0:
            for lens in lenses_list:
                point = point.item_of
                print(point)
                print(point.x)
                if lens is not aperture:
                    aperture = aperture.item_of
                print(aperture)
                print(aperture.x)
                if len(self.complementary_rays) == 0:
                    linear_factor = self.linear_function["a"]
                    ray_end = self.ray_coords[1]
                    print(f"FIRST RAY CORDS: {ray_end} vs POINT Y: {point.y}")
                    print(f"FIRST LINEAR FACTOR: {linear_factor}")
                else:
                    linear_factor = self.complementary_rays[-1].linear_function["a"]
                    ray_end = self.complementary_rays[-1].ray_coords[1]
                    print(f"RAY CORDS: {ray_end} vs POINT Y: {point.y}")
                    print(f"LINEAR FACTOR: {linear_factor}")
                self.extend_ray(point, aperture, linear_factor, ray_end, left_object=lens, right_object=lens.get_next_object(lenses_list))



class NumericFieldRay(NumericRay):
    def __init__(self, sketch, middle_point_aperture, edge_point_aperture, left_object=None, right_object=None, factor=1, former_ray_end=None, object_type="user_defined"):
        super().__init__(sketch, middle_point_aperture, edge_point_aperture, left_object, right_object, factor, former_linear_factor=None, former_ray_end=former_ray_end, object_type=object_type)
        self.sketch = sketch
        self.middle_point_aperture = middle_point_aperture
        print(f"APERTURE 1: {self.middle_point_aperture}")
        self.edge_point_aperture = edge_point_aperture
        print(f"APERTURE 2: {self.edge_point_aperture}")
        self.factor = factor
        self.complementary_rays = []
        
        self.sprite = sprites.NumericFieldRay(self)

        if self.object_type == "user_defined":
            #self.extended = self.extend_ray()
            self.middle_point_object.bound_field_rays.append(self)
            self.edge_point_object.bound_field_rays.append(self)
            self.get_complete_ray()
            self.sketch.project.field_rays.append(self)
        
            print(f"ITS MEMBERS: {self.middle_point_object} -> {self.middle_point_object.bound_field_rays}, {self.edge_point_object} -> {self.edge_point_object.bound_field_rays}")
    

    def __str___(self):
        print("Field ray")


    def extend_ray(self, middle_point_aperture, edge_point_aperture, ray_end, left_object=None, right_object=None):
        if isinstance(left_object, NumericLensObject2):
            inverted_factor = self.factor * -1
        else:
            inverted_factor = self.factor
        new_ray = NumericFieldRay(self.sketch, middle_point_aperture, edge_point_aperture, left_object=left_object, right_object=right_object, factor=inverted_factor, former_ray_end=ray_end, object_type="resulting")
        self.complementary_rays.append(new_ray)

    def get_complete_ray(self):
        middle_point_aperture = self.middle_point_aperture
        edge_point_aperture = self.edge_point_aperture
        lenses_list = self.sketch.project.user_defined_lenses
        if len(lenses_list) > 0:
            for lens in lenses_list:
                #next_lens = NumericLensObject2.get_next_lens(lens, lenses_list)
                if middle_point_aperture.item_of is not None and lens is not middle_point_aperture:
                    middle_point_aperture = middle_point_aperture.item_of
                if lens is not edge_point_aperture:
                    edge_point_aperture = edge_point_aperture.item_of
                if len(self.complementary_rays) == 0:
                    ray_end = self.ray_coords[1]
                    print(f"FIRST MIDDLE POINT: {middle_point_aperture}")
                    print(f"FIRST RAY CORDS: {ray_end} vs MIDDLE POINT X: {middle_point_aperture.x}")
                else:
                    print(f"MIDDLE POINT: {middle_point_aperture}")
                    print(f"RAY CORDS: {ray_end} vs MIDDLE POINT X: {middle_point_aperture.x}")
                    ray_end = self.complementary_rays[-1].ray_coords[1]
                #aperture = aperture.item_of
                self.extend_ray(middle_point_aperture, edge_point_aperture, ray_end, left_object=lens, right_object=lens.get_next_object(lenses_list))


class NumericLensObject2(NumericObject):
    selected = None

    def __init__(
        self,
        x,
        y,
        sketch,
        diameter,
        focal,
        object_type="user_defined",
        item_of=None,
        image_of=None,
        resulting_of = None,
        lens_conversion_type={},
        is_in_infinity = False
    ) -> None:
        super().__init__(x, sketch, object_type, item_of, image_of, resulting_of, lens_conversion_type, is_in_infinity)
        self.diameter = diameter
        self.focal = focal
        self.bound_aperture_rays = []
        self.bound_field_rays = []
        self.converted_user_defined_objects = {}
        
        self.number = len(sketch.project.user_defined_apertures) + 1

        self.sprite = sprites.NumericLensObject(self)

        if len(sketch.project.user_defined_lenses) == 0:
            if self.object_type == "user_defined":
                self.sketch.lens = self
                self.object_label = NumericLensLabel(self, sketch, "none")
                self.lens_conversion_type = {self : "Image"}
                self.item_of = self.determine_image(self.sketch, self)
        else:
            self.object_label = NumericLensLabel(
                self, sketch, self.type_per_lens[sketch.lens]
            )
            #self.distance_label = self.draw_distance_label(sketch, sketch.lens)
            if self.object_type == "user_defined" and len(self.sketch.project.lenses) > 0:
                self.convert_object_per_lens()

        self.bind_select_object()
        self.add_to_lists()
        self.render_lenses_labels()
        if len(self.sketch.project.points) > 0 and self.object_type == "user_defined":
            self.convert_objects_via_self()

    def __del__(self):
        print("deleted aperture")

    def __str__(self) -> str:
        return f"Lens no. {self.number}{self.postfix}"

    def convert_objects_via_self(self):
        list_of_points = self.sketch.project.user_defined_points
        index_of_self = self.sketch.project.user_defined_lenses.index(self)
        if index_of_self == 0:
            next_lens = self.get_next_object(self.sketch.project.user_defined_lenses)
            if next_lens is not None:
                for point in list_of_points:
                    last_point = next_lens.converted_user_defined_objects[point]["Item"]
                    last_point.define_parameters_per_lens2(self, "Image") 
                    last_point.convert_object(self, "Image")
        elif index_of_self == len(self.sketch.project.user_defined_lenses) - 1:
            previous_lens = self.get_previous_object(self.sketch.project.user_defined_lenses)
            if previous_lens is not None:
                for point in list_of_points:
                    last_point = previous_lens.converted_user_defined_objects[point]["Image"]
                    last_point.define_parameters_per_lens2(self, "Item") 
                    last_point.convert_object(self, "Item")
        else:
            if index_of_self < len(self.sketch.project.user_defined_lenses) - index_of_self - 1:
                #   FROM LENS INDEX TO THE START OF LIST
                for point in list_of_points:
                    current_lens = self
                    previous_lens = current_lens.get_previous_object(self.sketch.project.user_defined_lenses)
                    while previous_lens is not None:
                        previous_lens.converted_user_defined_objects[point]["Item"].sprite.delete_sprite()
                        previous_lens.converted_user_defined_objects[point].update({"Item": None})
                        previous_lens = previous_lens.get_previous_object(self.sketch.project.user_defined_lenses)
                        
                    next_lens = current_lens.get_next_object(self.sketch.project.user_defined_lenses)

                    while current_lens is not None:
                        last_point = next_lens.converted_user_defined_objects[point]["Item"]
                        last_point.define_parameters_per_lens2(self, "Image") 
                        last_point.convert_object(self, "Image")
                        current_lens = current_lens.get_previous_object(self.sketch.project.user_defined_lenses)
            else:
                #   FROM LENS INDEX TO THE END OF LIST
                for point in list_of_points:
                    current_lens = self
                    next_lens = current_lens.get_next_object(self.sketch.project.user_defined_lenses)

                    while current_lens is not None:
                        
                        last_point = next_lens.converted_user_defined_objects[point]["Item"]
                        last_point.define_parameters_per_lens2(current_lens, "Image") 
                        last_point.convert_object(current_lens, "Image")
                        current_lens = current_lens.get_previous_object(self.sketch.project.user_defined_lenses)



                for point in list_of_points:
                    current_lens = self
                    next_lens = current_lens.get_next_object(self.sketch.project.user_defined_lenses)
                    while next_lens is not None:
                        next_lens.converted_user_defined_objects[point]["Image"].sprite.delete_sprite()
                        next_lens.converted_user_defined_objects[point].update({"Image": None})
                        next_lens = next_lens.get_next_object(self.sketch.project.user_defined_lenses)
                        
                    previous_lens = current_lens.get_previous_object(self.sketch.project.user_defined_lenses)

                    while current_lens is not None:
                        last_point = previous_lens.converted_user_defined_objects[point]["Image"]
                        last_point.define_parameters_per_lens2(current_lens, "Item") 
                        last_point.convert_object(current_lens, "Item")
                        current_lens = current_lens.get_next_object(self.sketch.project.user_defined_lenses)


    #def clasify_objects(self):



    def render_lenses_labels(self):
        for i, lens in enumerate(self.sketch.project.user_defined_lenses):
            lens.number = i + 1
            lens.object_label.update_label_text()
            lens.update_lens_number_dictionary()

            for row in self.sketch.project.object_properties.list_of_rows:
                if lens is row.numeric_object:
                    row.update_row()
                    break
            
            if lens.resulting_object is not None:
                lens.resulting_object.number = i + 1
                lens.resulting_object.object_label.update_label_text()

                for row in self.sketch.project.object_properties.list_of_rows:
                    if lens.resulting_object is row.numeric_object:
                        row.update_row()
                        break


    def update_lens_number_dictionary(self):
        self.sketch.project.lens_numbers_dictionary.update({self: self.number})

    def add_to_lists(self):
        if self.object_type == "user_defined":
            self.sketch.project.lens_numbers_dictionary.update({str(self.number) : self})
            self.sketch.project.resulting_lenses.update({self : self.item_of})
            self.sketch.project.resulting_apertures.update({self : self.item_of})
            self.insert_into_list(self.sketch.project.user_defined_lenses)
            self.insert_into_list(self.sketch.project.user_defined_apertures)
            self.convert_nearby_lenses()
            NumericLensObject2.get_real_plane_lenses(self.sketch.project)
            NumericAperture.get_real_plane_apertures(self.sketch.project)
        else:
            self.focal = None
            
        self.sketch.project.lenses.append(self)
        self.sketch.project.apertures.append(self)
        self.sketch.project.object_properties.create_properties_row(self)

    
    def update_resulting_list(self, resulting_lens):
        self.sketch.project.resulting_lenses.update({self : resulting_lens})
        self.sketch.project.resulting_apertures.update({self : resulting_lens})

    def convert_nearby_lenses(self):
        list_of_lenses = self.sketch.project.user_defined_lenses
        next_lens = self.get_next_object(list_of_lenses)
        if next_lens is not None:
            next_lens.define_parameters_per_lens2(self, "Image")
            next_lens.convert_object(self, "Image")
        previous_lens = self.get_previous_object(list_of_lenses)
        if previous_lens is not None:
            previous_lens.define_parameters_per_lens2(self, "Item")
            previous_lens.convert_object(self, "Item")

    def determine_image(self, sketch, lens):
        if lens is self:
            image = self
            image.image_of = self
        else:  
            determined_x = self.parameters_per_lens[lens]["s'"] + lens.x
            determined_y = self.y
            determined_diameter = self.diameter * abs(
                self.parameters_per_lens[lens]["zoom"]
            )
            if determined_x == float("-inf") or determined_x == float("inf"):
                image = NumericLensObject2(
                    determined_x,
                    determined_y,
                    sketch,
                    determined_diameter,
                    self.focal,
                    object_type="resulting",
                    image_of=self,
                    resulting_of=self,
                    lens_conversion_type={lens : "Image"},
                    is_in_infinity=True
                )
            else:
                image = NumericLensObject2(
                    determined_x,
                    determined_y,
                    sketch,
                    determined_diameter,
                    self.focal,
                    object_type="resulting",
                    image_of=self,
                    resulting_of=self,
                    lens_conversion_type={lens : "Image"}
                )
            image.number = self.number
            image.object_label.update_label_text()

        return image

    def determine_item(self, sketch, lens):
        if lens is self:
            item = self
            item.item_of = self
        else:
            determined_x = self.parameters_per_lens[lens]["s"] + lens.x
            # print(f"PRINTUJE IKSA: {determined_x}")
            determined_y = self.y
            if self.parameters_per_lens[lens]["zoom"] == 0:
                determined_diameter = float("inf")
            elif self.parameters_per_lens[lens]["zoom"] == float("inf"):
                determined_diameter = 0
            else:
                determined_diameter = self.diameter / abs(
                    self.parameters_per_lens[lens]["zoom"]
                )
            if determined_x == float("-inf") or determined_x == float("inf"):
                item = NumericLensObject2(
                    determined_x,
                    determined_y,
                    sketch,
                    determined_diameter,
                    self.focal,
                    object_type="resulting",
                    item_of=self,
                    resulting_of=self,
                    lens_conversion_type={lens : "Item"},
                    is_in_infinity=True
                )
            else:
                item = NumericLensObject2(
                    determined_x,
                    determined_y,
                    sketch,
                    determined_diameter,
                    self.focal,
                    object_type="resulting",
                    item_of=self,
                    resulting_of=self,
                    lens_conversion_type={lens : "Item"}
                )
            item.number = self.number
            item.object_label.update_label_text()

        return item

    def draw(self, sketch):
        if self.object_type == "resulting":
            return self.draw_resulting_lens(sketch)
        else:
            line_width = 3

            center = sketch.axis.y
            upper_end = center - self.diameter / 2
            lower_end = center + self.diameter / 2
            id = []
            id.append(
                sketch.create_line(
                    self.x - 3,
                    upper_end,
                    self.x + 4,
                    upper_end,
                    fill=self.color,
                    width=line_width,
                )
            )
            id.append(
                sketch.create_line(
                    self.x - 3,
                    lower_end,
                    self.x + 4,
                    lower_end,
                    fill=self.color,
                    width=line_width,
                )
            )
            id.append(
                sketch.create_line(
                    self.x, upper_end, self.x, 0, fill=self.color, width=line_width
                )
            )
            id.append(
                sketch.create_line(
                    self.x, lower_end, self.x, 400, fill=self.color, width=line_width
                )
            )
            return id

    def draw_resulting_lens(self, sketch):
        line_width = 1
        self.color = "grey"

        center = sketch.axis.y
        upper_end = center - self.diameter / 2
        lower_end = center + self.diameter / 2
        id = []
        id.append(
            sketch.create_line(
                self.x - 3,
                upper_end,
                self.x + 4,
                upper_end,
                fill=self.color,
                width=line_width,
            )
        )
        id.append(
            sketch.create_line(
                self.x - 3,
                lower_end,
                self.x + 4,
                lower_end,
                fill=self.color,
                width=line_width,
            )
        )

        #   MAKING CEASED LINE
        lines_space = 40

        starting_value = upper_end
        while starting_value > 0:
            id.append(
                sketch.create_line(
                    self.x,
                    starting_value,
                    self.x,
                    starting_value - lines_space,
                    fill=self.color,
                    width=line_width,
                )
            )
            starting_value = starting_value - 1.5 * lines_space

        starting_value = lower_end
        while starting_value < 800:
            id.append(
                sketch.create_line(
                    self.x,
                    starting_value,
                    self.x,
                    starting_value + lines_space,
                    fill=self.color,
                    width=line_width,
                )
            )
            starting_value = starting_value + 1.5 * lines_space

        return id


    @staticmethod
    def get_real_plane_lenses(project):
        user_defined_lenses = project.user_defined_lenses
        real_plane_lenses = project.real_plane_lenses
        real_plane_lenses.clear()
        boundary_lens = user_defined_lenses[0]
        if len(user_defined_lenses) > 1:
            for lens in user_defined_lenses:
                lens.get_real_plane_lens(boundary_lens)

    def render(self):
        self.sprite.redraw()

    def select_lens(self):
        print(f"SELECTED {self}")
        if NumericLensObject2.selected != None:
            NumericLensObject2.selected.sprite.bind_select_object()
        NumericLensObject2.selected = self
        self.sprite.bind_delete_object()



class NumericLensLabel:
    def __init__(self, lens: NumericLensObject2, sketch, type="image"):
        self.lens = lens
        self.sketch = sketch
        self.type = type
        self.y = self.define_number_y_position()
        self.number_label = self.define_aperture_number_label()

    def __del__(self):
        print("DELETED LENS LABEL")

    def define_lens_focal_label(self):
        aperture = self.lens
        sketch = self.sketch
        return NumericText(
            aperture.x,
            aperture.x,
            self.y,
            f"f{aperture.number}' = {aperture.focal}",
            sketch,
            bd=1,
        )

    def define_number_y_position(self):
        return self.sketch.axis.y - self.lens.diameter / 2 - 15

    def define_aperture_number_label(self):
        aperture = self.lens
        sketch = self.sketch
        return NumericText(
            aperture.x,
            aperture.x,
            self.y,
            f"{aperture.number}{aperture.postfix}",
            sketch,
            bd=1,
        )

    def define_aperture_diameter_label(self):
        aperture = self.lens
        sketch = self.sketch
        return NumericText(
            aperture.x - 1,
            aperture.x + 2,
            self.number_label.y - 15,
            f"Ø: {aperture.diameter}",
            sketch,
            bd=1,
        )

    def delete_label(self):
        self.number_label.delete_text()

    def update_label_text(self):
        self.delete_label()
        self.number_label = self.define_aperture_number_label()


