import numpy as np

import graphic_objects_sprites as sprites



def lens_toggle_render(sketch, lens):
    Point.redefine_after_toggling_lens(sketch, lens)
    Line.redefine_after_toggling_lens(sketch)
    sketch.render_sketch()



def temp_text(e, entry):
    entry.delete(0, "end")


def delete_object(object):
    del object







class Axis:
    main_axis = None

    def __init__(self, sketch, x1, x2, y):
        self.sketch = sketch
        self.y = y
        self.sprite = sprites.Axis(sketch, x1, y, x2, y, color="grey", width=3)
        Axis.main_axis = self


    def render_axis(self):
        self.sprite.render()



class Lens:
    lens = None

    def __init__(self, focal, pos, y):
        self.pos = pos
        self.x = pos
        self.y = y
        self.focal = focal
        self.type = self.determine_type()

    def determine_type(self):
        return "positive" if self.focal > 0 else "negative"



class GraphicLens(Lens):
    
    lens = None

    def __init__(self, sketch, focal, pos, y, space = 30, in_out_factor=1):
        super().__init__(focal, pos, y)
        self.sketch = sketch
        self.space = space
        self.in_out_factor = in_out_factor

        self.relative_zero_point = self.determine_relative_zero_point()
        self.real_imaginary_boundary = self.determine_real_imaginary_boundary()
        self.focus_pos = self.determine_focus_pos()

        self.sprite = sprites.GraphicLens(sketch, focal, pos, y, space, self.type)


        GraphicLens.lens = self


    def determine_relative_zero_point(self):
        return self.pos + self.space / 2 if self.type == "positive" else self.pos - self.space / 2
        
    def determine_real_imaginary_boundary(self):
        return self.pos - self.space / 2 if self.type == "positive" else self.pos + self.space / 2
        
    def determine_focus_pos(self):
        if self.type == "positive":
            return (self.x - self.space / 2 - self.focal, self.x + self.space / 2 + self.focal)
        elif self.type == "negative":
            return (self.x + self.space / 2 - self.focal, self.x - self.space / 2 + self.focal)

    def delete_lens(self):
        self.sprite.erase_image()


    def render_lens(self):
        self.sprite.render_lens()


    @staticmethod
    def render_after_toggling(sketch):
        GraphicLens.render_lens(sketch.lens)
        Point.render_points(sketch.project.points)



class Object:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y



class Point(Object):
    r = 2
    label_letters_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W',
                          'X','Y','Z']

    def __init__(self, x, y, sketch, type="user_defined", on_axis=False, on_real_imaginary_boundary=False, in_lines=None, in_shape=None) -> None:
        super().__init__(x, y)
        self.sketch = sketch
        self.type = type
        self.rays = []
        self.show_rays = True
        self.on_axis = on_axis
        self.on_real_imaginary_boundary = on_real_imaginary_boundary
        self.in_lines = self.check_lines(in_lines)
        self.in_shape = in_shape
        self.its_item_point = None
        self.its_image_point = None
        self.label_id = self.create_label_id()
        self.sketch.project.points.append(self)

        if type == "user_defined" or type == "focus_boundary":
            self.define_rays(GraphicLens.lens)
            render_lens_and_axis(self.sketch.project)
            self.define_resulting_point(sketch.lens)
            if self.on_axis:
                self.place_point_on_axis()

        self.sprite = sprites.Point(self, sketch, type=type)



    def check_lines(self, in_lines):
        if isinstance(in_lines, list):
            return in_lines
        else:
            return list()
        
    def create_label_id(self):
        points_number = len(self.sketch.project.resulting_points)
        label_letters_number = len(Point.label_letters_list)
        label = ""
        while points_number > label_letters_number:
            label = label + Point.label_letters_list[0]
            points_number -= label_letters_number
        label = label + Point.label_letters_list[points_number]

        if self.type == "resulting":
            label = label + "'"

        return label


    def define_positive_lens_rays(self, lens):
        self.rays.append(ParallelRay(self, lens, self.sketch))
        self.rays.append(MiddleRay(self, lens, self.sketch))


    def define_negative_lens_rays(self, lens):

        self.rays.append(ParallelRay(self, lens, self.sketch))
        self.rays.append(MiddleRay(self, lens, self.sketch))


    def define_rays(self, lens):
        
        if self.y == self.sketch.axis.y:
            self.on_axis = True
            self.y -= 10

        if self.x == lens.real_imaginary_boundary:
            self.on_real_imaginary_boundary = True
        
        
        return self.define_positive_lens_rays(lens) if lens.type == "positive" else self.define_negative_lens_rays(lens)



    def define_resulting_point(self, lens):
        if self.on_real_imaginary_boundary:
            self.its_image_point = Point(
                lens.relative_zero_point, self.y, self.sketch, type="resulting", on_axis=self.on_axis
            )
        else:
            new_point_coords = rays_intersection(
                self.rays[0].elementary_rays[1], self.rays[1].elementary_rays[1], lens
            )
            self.its_image_point = Point(
                    new_point_coords[0], new_point_coords[1], self.sketch, type="resulting", on_axis=self.on_axis
                )
      
        self.its_image_point.its_item_point = self
        self.sketch.project.resulting_points.update({self: self.its_image_point})


    def place_point_on_axis(self):
        if self.its_image_point is not None:
            self.its_image_point.place_point_on_axis()
        self.y = self.sketch.axis.y


    def delete_point(self):
        self.erase_rays()
        self.sprite.delete_point()
        if self.type == "user_defined":
            self.its_image_point.delete_point()


    def delete_point_manually(self, sketch):
        self.delete_point(sketch)


    def erase_rays(self):
        for ray in self.rays:
            ray.delete_ray()
            del ray

        self.rays.clear()


    def erase_resulting_point(self):
        self.sketch.project.points.remove(self.its_image_point)
        self.its_image_point.delete_point()
        
    def select_point(self, event):
        self.sketch.bind("<ButtonRelease-1><ButtonRelease-1>", self.move_point)
        

    def move_point(self, event):
        self.sketch.unbind("<ButtonRelease-1><ButtonRelease-1>")
        self.its_image_point.delete_point()
        self.sketch.project.points.remove(self.its_image_point)
        self.delete_point()
        self.sketch.project.resulting_points.pop(self)
        self.sketch.project.points.remove(self)
        new_point = Point(event.x, event.y, self.sketch, type=self.type, in_lines=self.in_lines, in_shape=self.in_shape)
        self.replace_point_in_lines(new_point)
        new_point.redefine_point_lines()
        


    def redefine_point_lines(self):
        if self.in_lines is not None:
            for line in self.in_lines:
                line.redefine_line_after_moving_point()


    def replace_point_in_lines(self, point):
        if self.in_lines is not None:
            for line in self.in_lines:
                if line.point_1 is self:
                    line.point_1 = point
                if line.point_2 is self:
                    line.point_2 = point


    def redefine_rays(self, lens):
        self.erase_rays()
        self.define_rays(lens)

    def redefine_resulting_point(self, lens):
        self.erase_resulting_point()
        self.define_resulting_point(lens)

    def render_point(self):
        self.sprite.render_point()

    @staticmethod
    def delete_rays(point, sketch):
        for main_ray in point.rays:
            for ray in main_ray:
                sketch.canv.delete(ray.img_id)

    

    @staticmethod
    def redefine_after_toggling_lens(sketch, lens):
        for point in sketch.project.resulting_points:
            point.redefine_rays(lens)
            point.redefine_resulting_point(lens)
            if point.on_axis:
                point.place_point_on_axis()

    @staticmethod
    def render_points(points):
        if len(points) > 0:
            for point in points:
                point.render_point()


    @staticmethod
    def delete_points(list_of_points: list):
        for i, point in enumerate(list_of_points):
            list_of_points[-1].delete_point()



class Line:
    def __init__(self, point_1: Point, point_2: Point, sketch, type, color, line_boundary_1: Point = None, line_boundary_2: Point = None):
        self.point_1 = point_1
        point_1.in_lines.append(self)
        self.point_2 = point_2
        point_2.in_lines.append(self)
        self.sketch = sketch
        self.type = type
        self.color = color
        self.line_boundary_1 = line_boundary_1
        self.line_boundary_2 = line_boundary_2
        self.in_shape = None
        self.its_item_line = None
        self.its_image_line = None

        self.sketch.project.lines.append(self)

        self.boundary_points = {point_1 : None, point_2 : None}
        self.focus_intersection = None

        self.sprite = sprites.Line(point_1, point_2, line_boundary_1, line_boundary_2, sketch, type, color=self.color)
        

        if self.type == "user_defined":
            
            self.linear_function = self.define_linear_function()
            self.focus_intersection = self.check_focus_intersection()         
            self.its_image_line = self.define_resulting_line()
            self.sketch.project.resulting_lines.update({self : self.its_image_line})

        
    def define_resulting_line(self):
        resulting_point_1 = self.sketch.project.resulting_points[self.point_1]
        resulting_point_2 = self.sketch.project.resulting_points[self.point_2]
        if self.focus_intersection:
            resulting_line_boundary_1 = self.sketch.project.resulting_points[self.boundary_points[self.point_1]]
            resulting_line_boundary_2 = self.sketch.project.resulting_points[self.boundary_points[self.point_2]]
        else:
            resulting_line_boundary_1, resulting_line_boundary_2 = None, None

        new_line = Line(resulting_point_1, resulting_point_2, self.sketch, "resulting", "red", resulting_line_boundary_1,
                        resulting_line_boundary_2)
        new_line.its_item_line = self

        return new_line

    
    def define_linear_function(self):
        linear_function = {}
        try:
            linear_function.update({
                "a": (self.point_2.y - self.point_1.y) / (self.point_2.x - self.point_1.x),
                "carthesian_zero": (self.point_1.x, self.point_1.y),
            }
            )
        except ZeroDivisionError:  #   RATHER RETURN "A" COEFFICIENT AS NONE
            linear_function.update({"a": None, "carthesian_zero": (self.point_1.x, self.point_1.y)})
        
        return linear_function


    def check_focus_intersection(self) -> bool:
        if self.point_1.x < self.point_2.x:
            if (
                self.sketch.lens.focus_pos[0] >= self.point_1.x
                and self.sketch.lens.focus_pos[0] <= self.point_2.x
            ):
                self.points_nearby_focus()
                return True
            else:
                return False
        else:
            if (
                self.sketch.lens.focus_pos[0] >= self.point_2.x
                and self.sketch.lens.focus_pos[0] <= self.point_1.x
            ):
                self.points_nearby_focus()
                return True
            else:
                return False

    def points_nearby_focus(self):
        x = self.sketch.lens.focus_pos[0] - 1
        y = self.linear_function["carthesian_zero"][1] + self.linear_function["a"] * (
            x - self.linear_function["carthesian_zero"][0]
        )
        new_boundary_point_1 = Point(x, y, self.sketch, type="focus_boundary")
        

        x = self.sketch.lens.focus_pos[0] + 1
        y = self.linear_function["carthesian_zero"][1] + self.linear_function["a"] * (
            x - self.linear_function["carthesian_zero"][0]
        )
        new_boundary_point_2 = Point(x, y, self.sketch, type="focus_boundary")

        if self.point_1.x < self.point_2.x:
            self.boundary_points.update({self.point_1: new_boundary_point_1})
            self.boundary_points.update({self.point_2: new_boundary_point_2})
        else:
            self.boundary_points.update({self.point_2: new_boundary_point_1})
            self.boundary_points.update({self.point_1: new_boundary_point_2})
        

    def unmark_boundary_points(self):
        self.boundary_points = {self.point_1 : None, self.point_2 : None}

    def delete_boundary_points(self):
        points = list(self.boundary_points.values())
        for point in points:
            if point is not None:
                point.its_image_point.delete_point()
                self.sketch.project.points.remove(point.its_image_point)
                point.delete_point()
                self.sketch.project.points.remove(point)
                self.sketch.project.resulting_points.pop(point)
        self.unmark_boundary_points()

    def delete_line(self):
        if self.type == "user_defined":
            self.delete_boundary_points()
        self.sprite.delete_image()


    def redefine_line_after_moving_point(self):
        self.sketch.project.lines.remove(self.its_image_line)
        self.its_image_line.delete_line()
        self.delete_boundary_points()
        self.delete_line()
        self.sprite = sprites.Line(self.point_1, self.point_2, self.line_boundary_1, self.line_boundary_2, self.sketch, self.type, color=self.color)
        self.linear_function = self.define_linear_function()
        self.focus_intersection = self.check_focus_intersection()
        self.its_image_line = self.define_resulting_line()
        self.sketch.project.resulting_lines.update({self : self.its_image_line})
                  

    def redefine_resulting_line(self):
        self.sketch.project.lines.remove(self.its_image_line)
        self.its_image_line.delete_line()
        self.its_image_line = self.define_resulting_line()    


    def redefine_line_after_toggling_lens(self):
        self.sketch.project.lines.remove(self.its_image_line)
        self.its_image_line.delete_line()
        self.delete_boundary_points()
        self.focus_intersection = self.check_focus_intersection()
        self.its_image_line = self.define_resulting_line()
        self.sketch.project.resulting_lines.update({self : self.its_image_line})


    def render_line(self): 
        self.sprite.render_line()


    @staticmethod
    def redefine_after_toggling_lens(sketch):
        for line in sketch.project.resulting_lines:
            line.redefine_line_after_toggling_lens()
        ...

    @staticmethod
    def render_lines(lines):
        if len(lines) > 0:
            for line in lines:
                line.render_line()



class Shape:

    def __init__(self, lines: list, sketch, type="user_defined", color="black"):
        self.lines = lines
        self.sketch = sketch
        self.type = type
        self.color = color
        self.its_item_shape = None
        self.its_image_shape = None
        self.sketch.project.shapes.append(self)

        self.mark_lines()
        if self.type == "user_defined":
            resulting_lines = []
            for line in self.lines:
                resulting_lines.append(line.its_image_line)
            self.its_item_shape = Shape(resulting_lines, self.sketch, type="resulting")
            self.sketch.project.resulting_shapes.update({self : self.its_item_shape})

        self.mark_resulting()

    def mark_lines(self):
        for line in self.lines:
            line.in_shape = self

    def mark_resulting(self):
        its_item = self.lines[0].its_item_line
        if its_item is not None:
            self.its_item_shape = its_item.in_shape
        its_image = self.lines[0].its_image_line
        if its_image is not None:
            self.its_image_shape = its_image.in_shape


    def delete_shape(self):
        if self.its_image_shape != None:
            self.its_image_shape.its_item_shape = None
            self.its_image_shape.delete_shape()
        if self.its_item_shape != None:
            self.its_item_shape.its_image_shape = None
            self.its_item_shape.delete_shape()
        for line in self.lines:
            line.delete_line()


    @staticmethod
    def redefine_after_toggling_lens(sketch, lens):
        ...




class Ray:
    def __init__(self, x1, y1, x2, y2, lens, sketch, type="real"):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.lens = lens
        self.sketch = sketch
        self.type = type

        self.linear_function = self.linear_function_of_ray()

        self.sprite = sprites.Ray(x1, y1, x2, y2, self.linear_function, sketch, self.type)


    def linear_function_of_ray(self):
        try:
            return {"a": (self.y2 - self.y1) / (self.x2 - self.x1), "b": self.y1 - self.lens.y}
        except ZeroDivisionError:
            return {"a": float("inf"), "b": self.y1 - self.lens.y}
    

    def delete_ray(self):
        self.sprite.erase()
        del self.sprite

    def render_ray(self):
        self.sprite.render_ray()

    
    @staticmethod
    def render_rays(rays):
        if len(rays) > 0:
            for ray in rays:
                ray.render_ray()



class ParallelRay:

    def __init__(self, point, lens, sketch):
        self.point = point
        self.lens = lens
        self.sketch = sketch
        self.type = type
        self.elementary_rays = self.define_elementary_rays()

    def define_elementary_rays(self):
        sketch = self.sketch
        if self.lens.type == "positive":
            elementary_rays = [
                                Ray(0, self.point.y, self.lens.real_imaginary_boundary, self.point.y, self.lens, sketch),
                                Ray(
                                    self.lens.relative_zero_point,
                                    self.point.y,
                                    self.lens.focus_pos[1]
                                    + 3
                                    * (
                                        self.lens.focus_pos[1]
                                        - self.lens.relative_zero_point
                                    ),
                                    self.lens.y
                                    + 3 * (self.lens.y - self.point.y),
                                    self.lens,
                                    sketch,
                                ),
                            ]
            
        elif self.lens.type == "negative":
            elementary_rays = [
                                Ray(0, self.point.y, self.lens.real_imaginary_boundary, self.point.y, self.lens, sketch),
                                Ray(
                                    self.lens.relative_zero_point,
                                    self.point.y,
                                    self.lens.relative_zero_point
                                    + 3
                                    * (
                                        self.lens.relative_zero_point
                                        - self.lens.focus_pos[1]
                                    ),
                                    self.point.y + 3 * (self.point.y - self.lens.y),
                                    self.lens,
                                    sketch,
                                ),
                            ]
        
        return elementary_rays



            

    def delete_ray(self):
        for ray in self.elementary_rays:
            ray.delete_ray()
            del ray





    def positive_lens_elementary_rays(self):
        if self.point.x <= self.lens.real_imaginary_boundary:
            if 1:
                ...
            else:
                ...
        else:
            ...


    def negative_lens_elementary_rays(self):
        if self.point.x <= self.lens.real_imaginary_boundary:
            if 1:
                ...
            else:
                ...
        else:
            ...

    def before_plane_boundary_rays(self):
        ...
    
    def after_plane_boundary_rays(self):
        ...

    def render_parallel_ray(self):
        Ray.render_rays(self.elementary_rays)


class MiddleRay:

    def __init__(self, point, lens, sketch):
        self.point = point
        self.lens = lens
        self.sketch = sketch
        self.type = type
        self.elementary_rays = self.define_elementary_rays()


    def define_elementary_rays(self):
        sketch = self.sketch
        # second real
        if self.lens.type == "positive":
            if self.point.x <= self.lens.real_imaginary_boundary:
                elementary_rays = [
                                    Ray(
                                        self.lens.real_imaginary_boundary
                                        - 3 * (self.lens.real_imaginary_boundary - self.point.x),
                                        self.lens.y - 3 * (self.lens.y - self.point.y),
                                        self.lens.real_imaginary_boundary,
                                        self.lens.y,
                                        self.lens,
                                        sketch,
                                    ),
                                    Ray(
                                        self.lens.relative_zero_point,
                                        self.lens.y,
                                        self.lens.relative_zero_point
                                        + 3 * (self.lens.real_imaginary_boundary - self.point.x),
                                        self.lens.y + 3 * (self.lens.y - self.point.y),
                                        self.lens,
                                        sketch,
                                    ),
                                ]
            else:
                elementary_rays = [
                                    Ray(
                                        self.lens.real_imaginary_boundary
                                        + 3 * (self.lens.real_imaginary_boundary - self.point.x),
                                        self.lens.y + 3 * (self.lens.y - self.point.y),
                                        self.lens.real_imaginary_boundary,
                                        self.lens.y,
                                        self.lens,
                                        sketch,
                                    ),
                                    Ray(
                                        self.lens.relative_zero_point,
                                        self.lens.y,
                                        self.lens.relative_zero_point
                                        - 3 * (self.lens.real_imaginary_boundary - self.point.x),
                                        self.lens.y - 3 * (self.lens.y - self.point.y),
                                        self.lens,
                                        sketch,
                                    ),
                                ]
       
        elif self.lens.type == "negative":
            if self.point.x <= self.lens.real_imaginary_boundary:
                elementary_rays = [
                                    Ray(
                                        self.lens.real_imaginary_boundary
                                        - 3 * (self.lens.real_imaginary_boundary - self.point.x),
                                        self.lens.y - 3 * (self.lens.y - self.point.y),
                                        self.lens.real_imaginary_boundary,
                                        self.lens.y,
                                        self.lens,
                                        sketch,
                                    ),
                                    Ray(
                                        self.lens.relative_zero_point,
                                        self.lens.y,
                                        self.lens.relative_zero_point
                                        + 3 * (self.lens.real_imaginary_boundary - self.point.x),
                                        self.lens.y + 3 * (self.lens.y - self.point.y),
                                        self.lens,
                                        sketch,
                                    ),
                                ]
            else:
                elementary_rays = [
                                    Ray(
                                        self.lens.real_imaginary_boundary
                                        + 3 * (self.lens.real_imaginary_boundary - self.point.x),
                                        self.lens.y + 3 * (self.lens.y - self.point.y),
                                        self.lens.real_imaginary_boundary,
                                        self.lens.y,
                                        self.lens,
                                        sketch,
                                    ),
                                    Ray(
                                        self.lens.relative_zero_point,
                                        self.lens.y,
                                        self.lens.relative_zero_point
                                        - 3 * (self.lens.real_imaginary_boundary - self.point.x),
                                        self.lens.y - 3 * (self.lens.y - self.point.y),
                                        self.lens,
                                        sketch,
                                    ),
                                ]
                
        return elementary_rays


    def delete_ray(self):
        for ray in self.elementary_rays:
            ray.delete_ray()
            del ray


    def render_middle_ray(self):
        Ray.render_rays(self.elementary_rays)



class FocalRay:

    def __init__(self, point, lens, sketch):
        self.point = point
        self.lens = lens
        self.sketch = sketch
        self.type = type
        self.elementary_rays = self.define_elementary_rays()


    def define_elementary_rays(self):
        sketch = self.sketch
        if self.lens.type == "positive":
            elementary_rays = [
                                """Ray(0, self.point.y, self.lens.real_imaginary_boundary, self.point.y, sketch),
                                Ray(
                                    self.lens.relative_zero_point,
                                    self.point.y,
                                    self.lens.focus_pos[1]
                                    + 3
                                    * (
                                        self.lens.focus_pos[1]
                                        - self.lens.relative_zero_point
                                    ),
                                    self.lens.y
                                    + 3 * (self.lens.y - self.point.y),
                                    sketch,
                                ),"""
                            ]
            
        elif self.lens.type == "negative":
            elementary_rays = [
                                """Ray(0, self.point.y, self.lens.real_imaginary_boundary, self.point.y, sketch),
                                Ray(
                                    self.lens.relative_zero_point,
                                    self.point.y,
                                    self.lens.relative_zero_point
                                    + 3
                                    * (
                                        self.lens.relative_zero_point
                                        - self.lens.focus_pos[1]
                                    ),
                                    self.point.y + 3 * (self.point.y - self.lens.y),
                                    sketch,
                                ),"""
                            ]
        
        return elementary_rays

    def delete_ray(self):
        for ray in self.elementary_rays:
            ray.delete_ray()
            del ray

    
    def render_focal_ray(self):
        Ray.render_rays(self.elementary_rays)


    

def rays_intersection(ray_1: Ray, ray_2: Ray, lens: GraphicLens):
    # IF A_1 == A_2 -> they never intersect

    main_matrix = np.array([[ray_1.linear_function["a"], -1], [ray_2.linear_function["a"], -1]])

    x_matrix = np.array([[-1 * ray_1.linear_function["b"], -1], [-1 * ray_2.linear_function["b"], -1]])

    y_matrix = np.array(
        [
            [ray_1.linear_function["a"], -1 * ray_1.linear_function["b"]],
            [ray_2.linear_function["a"], -1 * ray_2.linear_function["b"]],
        ]
    )

    x = np.linalg.det(x_matrix) / np.linalg.det(main_matrix)
    y = np.linalg.det(y_matrix) / np.linalg.det(main_matrix)

    try:
        shared_x = int(x) + 415
    except OverflowError:
        shared_x = float("inf")
    except ValueError:  # THAT MEANS A POINT ON AXIS
        ...

    try:
        shared_y = int(y) + 200
    except OverflowError:
        shared_y = float("inf")


    if lens.type == "positive":
        x_coord_compensation = lens.x + lens.space/2
    else:
        x_coord_compensation = lens.x - lens.space/2

    y_coord_compensation = lens.y

    return (x + x_coord_compensation, y + y_coord_compensation)


def render_lens_and_axis(project):
    project.canv.axis.render_axis()

    
def render_all_objects(project):
    project.canv.axis.render_axis()
    project.canv.lens.render_lens()
    Line.render_lines(project.lines)
    Point.render_points(project.points)