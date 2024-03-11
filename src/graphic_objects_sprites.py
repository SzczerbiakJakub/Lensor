import tkinter as tk




class Axis:

    def __init__(self, sketch, x1, y1, x2, y2, color="grey", width=3):
        self.sketch = sketch
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.width = width
        self.image = self.draw_axis_image()

    def draw_axis_image(self):
        return self.sketch.create_line(
            self.x1, self.y1, self.x2, self.y2, fill=self.color, width=self.width
        )


    def delete_axis_image(self):
        self.sketch.delete(self.image)

    def render(self):
        self.delete_axis_image()
        self.image = self.draw_axis_image()









class GraphicLens:

    def __init__(self, sketch, focal, pos, y, space, type="positive", in_out_factor=1):
        self.sketch = sketch
        self.focal = focal
        self.pos = pos
        self.y = y
        self.space = space
        self.in_out_factor = in_out_factor
        self.type = type

        self.draw_lens(sketch, pos, space)

        self.draw_focus(sketch, pos, space, focal)

    def draw_lens(self, sketch, pos, space):
        if self.type == "positive":
            self.real_imaginary_boundary = pos - space / 2
            return self.draw_positive_lens(sketch, pos, space)
        elif self.type == "negative":
            self.real_imaginary_boundary = pos + space / 2
            return self.draw_negative_lens(sketch, pos, space)

    def draw_positive_lens(self, sketch, pos, space):
        font = "Helvetica 12 bold"
        self.lens_xpos = [pos - space / 2, pos + space / 2]

        self.lens_img = (
            (
                sketch.create_line(
                    self.lens_xpos[0], 20, self.lens_xpos[0], self.y*2 - 20, fill="black", width=2
                ),
                sketch.create_text(
                    self.lens_xpos[0], 10, text="H", fill="black", font=font
                ),
            ),
            (
                sketch.create_line(
                    self.lens_xpos[1], 20, self.lens_xpos[1], self.y*2 - 20, fill="black", width=2
                ),
                sketch.create_text(
                    self.lens_xpos[1], 10, text="H'", fill="black", font=font
                ),
            ),
        )

    def draw_negative_lens(self, sketch, pos, space):
        font = "Helvetica 12 bold"
        self.lens_xpos = [pos + space / 2, pos - space / 2]

        self.lens_img = (
            (
                sketch.create_line(
                    self.lens_xpos[0], 20, self.lens_xpos[0], self.y*2 - 20, fill="black", width=2
                ),
                sketch.create_text(
                    self.lens_xpos[0], 10, text="H", fill="black", font=font
                ),
            ),
            (
                sketch.create_line(
                    self.lens_xpos[1], 20, self.lens_xpos[1], self.y*2 - 20, fill="black", width=2
                ),
                sketch.create_text(
                    self.lens_xpos[1], 10, text="H'", fill="black", font=font
                ),
            ),
        )


    def draw_focus(self, sketch, pos, space, focal):
        if self.type == "positive":
            return self.draw_positive_focus(sketch, pos, space, focal)
        elif self.type == "negative":
            return self.draw_negative_focus(sketch, pos, space, focal)


    def draw_positive_focus(self, sketch, pos, space, focal):
        font = "Helvetica 12 bold"
        focus_pos = [
            [pos - space / 2 - focal, self.y],
            [pos + space / 2 + focal, self.y],
        ]

        self.focus_img = (
            (
                sketch.create_line(
                    focus_pos[0][0],
                    self.y - 10,
                    focus_pos[0][0],
                    self.y + 10,
                    fill="red",
                    width=3,
                ),
                sketch.create_text(
                    focus_pos[0][0], self.y - 20, text="F", fill="red", font=font
                ),
            ),
            (
                sketch.create_line(
                    focus_pos[1][0],
                    self.y - 10,
                    focus_pos[1][0],
                    self.y + 10,
                    fill="red",
                    width=3,
                ),
                sketch.create_text(
                    focus_pos[1][0], self.y - 20, text="F'", fill="red", font=font
                ),
            ),
        )

    def draw_negative_focus(self, sketch, pos, space, focal):
        font = "Helvetica 12 bold"
        self.focus_pos = [
            [pos + space / 2 - focal, self.y],
            [pos - space / 2 + focal, self.y],
        ]

        self.focus_img = (
            (
                sketch.create_line(
                    self.focus_pos[0][0],
                    self.y - 10,
                    self.focus_pos[0][0],
                    self.y + 10,
                    fill="red",
                    width=3,
                ),
                sketch.create_text(
                    self.focus_pos[0][0], self.y - 20, text="F", fill="red", font=font
                ),
            ),
            (
                sketch.create_line(
                    self.focus_pos[1][0],
                    self.y - 10,
                    self.focus_pos[1][0],
                    self.y + 10,
                    fill="red",
                    width=3,
                ),
                sketch.create_text(
                    self.focus_pos[1][0], self.y - 20, text="F'", fill="red", font=font
                ),
            ),
        )


    def erase_image(self):
        self.erase_lens_img()
        self.erase_focus_img()

    def erase_lens_img(self):
        for side in self.lens_img:
            for image in side:
                self.sketch.delete(image)

    def erase_focus_img(self):
        for side in self.focus_img:
            for image in side:
                self.sketch.delete(image)


    def render_lens(self):
        self.erase_image()
        self.draw_lens(self.sketch, self.pos, self.space)
        self.draw_focus(
            self.sketch, self.pos, self.space, self.focal
        )




























class Point:

    radius = 3
    font = "Helvetica 8 bold"

    def __init__(self, item, sketch, type, color="black") -> None:
        self.item = item
        self.sketch = sketch
        self.type = type
        self.color = color
        self.image = self.draw_image()
        self.bind_point_methods()



    def draw_image(self):

        radius = Point.radius

        self.item.label_sprite = self.draw_label()

        if self.type == "user_defined" or self.type == "focus_boundary":
            return self.sketch.create_oval(
                self.item.x - radius,
                self.item.y - radius,
                self.item.x + radius,
                self.item.y + radius,
                outline="black",
                fill="white",
            )
        elif self.type == "resulting":
            return self.sketch.create_oval(
                self.item.x - radius,
                self.item.y - radius,
                self.item.x + radius,
                self.item.y + radius,
                outline="green",
                fill="white",
            )
        
        


    def bind_point_methods(self):
        self.sketch.tag_bind(
                    self.image,
                    "<Enter>",
                    lambda event: self.item.sketch.cursor_over_point(self.item),
                )
        self.sketch.tag_bind(
                    self.image, "<Leave>", lambda event: self.item.sketch.cursor_left_point()
                )
        self.sketch.tag_bind(
                    self.image,
                    "<Button-2>",
                    lambda event: self.toggle_rays(),
                )
        if self.type == "user_defined":
            self.sketch.tag_bind(
                        self.image,
                        "<ButtonRelease-1>",
                        self.item.select_point
                    )
                         

    def render_before_drawing(self):
        if self.type == "user_defined":
            Axis.render_axis(self.sketch)
            GraphicLens.render_lens(self.sketch)

        if self.type == "user_defined":
            Point.hide_last_points_rays(self.sketch)
            Point.render_points(self.sketch)
            Shape.render_shapes(self.sketch)



    def delete_point(self):
        self.delete_label()
        self.item.sketch.delete(self.image)

    def draw_label(self):
        text_x = self.item.x
        text_y = self.item.y+Point.radius+6
        text_input = self.item.label_id
        print("CREATED LABEL")
        return self.sketch.create_text(text_x, text_y, text=text_input, font=Point.font, fill="black")


    def delete_label(self):
        self.item.sketch.delete(self.item.label_sprite)


    def redraw_point(self):
        self.delete_point()
        self.image = self.draw_image()
        self.bind_point_methods()
        

    
        """if self.type == "user_defined":
            return self.sketch.create_oval(
                self.item.x - Point.r,
                self.item.y - Point.r,
                self.item.x + Point.r,
                self.item.y + Point.r,
                outline="black",
                fill="white",
            )
        elif self.type == "resulting":
            return sketch.create_oval(
                self.x - 2 * Point.r,
                self.y - 2 * Point.r,
                self.x + 2 * Point.r,
                self.y + 2 * Point.r,
                outline="green",
                fill="blue",
            )"""


    def render_point(self):
        self.redraw_point()



    def hide_rays(self):
        self.item.show_rays = False
        for main_ray in self.item.rays:
            for ray in main_ray.elementary_rays:
                self.sketch.itemconfig(ray.sprite.image, fill="white")



    def unhide_rays(self):
        self.item.show_rays = True
        for main_ray in self.item.rays:
            for ray in main_ray.elementary_rays:
                if ray.type == "real":
                    self.sketch.itemconfig(ray.sprite.image, fill="black")
                elif ray.type == "imaginary":
                    self.sketch.itemconfig(ray.sprite.image, fill="light grey")

    
    def toggle_rays(self):
        if self.item.show_rays:
            self.hide_rays()
        else:
            self.unhide_rays()

    @staticmethod
    def hide_last_points_rays(point):
        if len(point.sketch.points) > 0:
            processed_point = point.sketch.project.points[-1]
            point.sketch.itemconfig(processed_point.sprite.image, fill="red")
            Point.hide_rays(processed_point)



    @staticmethod
    def render_points(sketch):
        if len(sketch.points) > 0:
            for point in sketch.points:
                point.redraw_point(sketch)



class Line:
    def __init__(self, point_1, point_2, line_boundary_1, line_boundary_2, sketch, type, color, width=3):
        self.point_1 = point_1
        self.point_2 = point_2
        self.line_boundary_1 = line_boundary_1
        self.line_boundary_2 = line_boundary_2       
        self.sketch = sketch
        self.type = type
        self.color = color
        self.width = width

        self.image = self.draw()

    """def __del__(self):
        self.sketch.delete(self.image)"""


    def draw(self):
        image = []
        if self.line_boundary_1 is not None or self.line_boundary_2 is not None:
            image.append(self.sketch.create_line(
                        self.point_1.x, self.point_1.y, self.line_boundary_1.x, self.line_boundary_1.y, fill=self.color, width=self.width
                    ))
            image.append(self.sketch.create_line(
                        self.line_boundary_2.x, self.line_boundary_2.y, self.point_2.x, self.point_2.y, fill=self.color, width=self.width
                    ))
        else:
            image.append(self.sketch.create_line(
                        self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y, fill=self.color, width=self.width
                    ))
            
        self.point_1.render_point()
        self.point_2.render_point()

        return image
        
    def redraw(self):
        self.delete_image()
        self.image = self.draw()

    def delete_image(self):
        for id in self.image:
            self.sketch.delete(id)

    def render_line(self):
        self.redraw()

        



class Shape:

    def __init__(
        self, points: list, lines: list, sketch, type="user_defined", color="black"
    ) -> None:
        self.color = color
        self.points = points.copy()
        self.lines = lines
        self.sketch = sketch
        self.type = type
        #self.image = self.build_shape()
        
        #self.resulting_shape = self.build_resulting_shape(sketch)

        """for point in self.points:
            point.redraw_point(sketch)"""


    def build_shape(self):
        lines = []
        for index, element in enumerate(self.points[:-1]):
            x1 = self.points[index].x
            y1 = self.points[index].y
            x2 = self.points[index + 1].x
            y2 = self.points[index + 1].y
            new_line = Line(x1, y1, x2, y2, self.sketch, self.type, self.color)
            lines.append(new_line)

        if len(self.points) > 2:
            index = len(self.points) - 1
            print("JEST OSTATNI INDEKSIOR")
            #if len(self.points) > 2:
            x1 = self.points[index].x
            y1 = self.points[index].y
            x2 = self.points[0].x
            y2 = self.points[0].y
            
            new_line = Line(x1, y1, x2, y2, self.sketch, self.type, self.color)
            lines.append(new_line)

        print(f"SHAPE'S SIZE: {len(lines)}")

        for x in self.points:
            try:
                print(f"{x} -> {self.sketch.project.resulting_points[x]}")
            except KeyError:
                print(f"{x} -> NONE")
                self.sketch.itemconfig(x.sprite.image, fill="orange")

        return lines
    
    def draw(self):
        ...

    """def build_resulting_shape(self, sketch):
        width = 1
        lines = []
        for line in self.shape:
            if line.focus_intersection == True:
                new_line = Line(
                    sketch.resulting_points[line.point_1],
                    sketch.resulting_points[line.boundary_points[line.point_1]],
                    sketch,
                    "shape_res",
                )
                lines.append(new_line)
                new_line = Line(
                    sketch.resulting_points[line.point_2],
                    sketch.resulting_points[line.boundary_points[line.point_2]],
                    sketch,
                    "shape_res",
                )
                lines.append(new_line)
            else:
                new_line = Line(
                    sketch.resulting_points[line.point_1],
                    sketch.resulting_points[line.point_2],
                    sketch,
                    "shape_res",
                )
                lines.append(new_line)

        return lines"""


    def delete_shape(self):
        self.erase_shape_points()
        del self

    def erase_shape_points(self):
        for point in self.points:
            point.delete_point()


    def render_shape(self):
        self.erase_shape_lines()

        self.shape = []
        self.shape = self.build_shape()

        for line in self.resulting_shape:
            line.delete_image()

        self.resulting_shape = []
        self.resulting_shape = self.build_resulting_shape()

        for point in self.points:
            point.redraw_point()




class Ray:
    def __init__(self, x1, y1, x2, y2, function, sketch, type="real"):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.function = function
        self.type = type
        self.sketch = sketch

        self.image = self.draw()

    def __del__(self):
        print("Deleted ray sprite")

    def draw(self):
        if self.type == "real":
            return self.draw_real_ray()
        
        elif self.type == "imaginary":
            return self.draw_imaginary_ray()


    def draw_real_ray(self):
        sketch = self.sketch
        ray_color = "black"
        return sketch.create_line(
                self.x1,
                self.y1,
                self.x2,
                self.function["a"] * (self.x2 - self.x1) + self.y1,
                fill=ray_color,
            )
    

    def draw_imaginary_ray(self):
        sketch = self.sketch
        ray_color = "light grey"
        return sketch.create_line(
                self.x1,
                self.y1,
                self.x2,
                self.function["a"] * (self.x2 - self.x1) + self.y1,
                fill=ray_color,
            )


    def erase(self):
        self.sketch.delete(self.image)


    def render_ray(self):
        self.erase()
        self.image = self.draw()