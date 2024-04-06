import tkinter as tk


class Axis:

    def __init__(self, sketch, x1, y1, x2, y2, color="grey", width=3):
        self.color = color
        self.width = width
        self.img = self.draw(sketch, x1, y1, x2, y2)

    def draw(self, sketch, x1, y1, x2, y2):
        return sketch.create_line(
            x1, y1, x2, y2, fill=self.color, width=self.width
        )

    def render_axis(self, sketch):
        self.img = self.draw(sketch)




class NumericLens:
    def __init__(self, item, sketch, focal, diameter, pos):
        self.item = item
        self.sketch = sketch
        self.diameter = diameter
        self.image = self.draw_lens(sketch)
        self.lens_info = self.draw_lens_info(sketch)
        self.draw_focus()

    def draw_lens(self, sketch):
        center = sketch.axis.y
        main_line = sketch.create_line(
            self.item.pos,
            center - self.diameter / 2,
            self.item.pos,
            center + self.diameter / 2,
            fill="black",
            width=3,
        )
        edges = self.draw_lens_edges(
            center - self.diameter / 2, center + self.diameter / 2, sketch
        )

        id = []
        id.append(main_line)
        id.extend(edges)
        return id

    def draw_lens_edges(self, upper_end, lower_end, sketch):
        edges = []
        if self.item.type == "positive":
            edges.append(
                sketch.create_line(
                    self.item.pos,
                    upper_end,
                    self.item.pos - 5,
                    upper_end + 8,
                    fill="black",
                    width=3,
                )
            )
            edges.append(
                sketch.create_line(
                    self.item.pos,
                    upper_end,
                    self.item.pos + 5,
                    upper_end + 8,
                    fill="black",
                    width=3,
                )
            )
            edges.append(
                sketch.create_line(
                    self.item.pos,
                    lower_end,
                    self.item.pos - 5,
                    lower_end - 8,
                    fill="black",
                    width=3,
                )
            )
            edges.append(
                sketch.create_line(
                    self.item.pos,
                    lower_end,
                    self.item.pos + 5,
                    lower_end - 8,
                    fill="black",
                    width=3,
                )
            )
        else:
            edges.append(
                sketch.create_line(
                    self.item.pos,
                    upper_end,
                    self.item.pos - 5,
                    upper_end - 8,
                    fill="black",
                    width=3,
                )
            )
            edges.append(
                sketch.create_line(
                    self.item.pos,
                    upper_end,
                    self.item.pos + 5,
                    upper_end - 8,
                    fill="black",
                    width=3,
                )
            )
            edges.append(
                sketch.create_line(
                    self.item.pos,
                    lower_end,
                    self.item.pos - 5,
                    lower_end + 8,
                    fill="black",
                    width=3,
                )
            )
            edges.append(
                sketch.create_line(
                    self.item.pos,
                    lower_end,
                    self.item.pos + 5,
                    lower_end + 8,
                    fill="black",
                    width=3,
                )
            )
        return edges

    def draw_lens_info(self, sketch):
        font = "Helvetica 8 bold"
        focal_info_height = sketch.axis.y + self.diameter / 2 + 16
        diameter_info_height = focal_info_height + 16
        focal_info = sketch.create_text(
            self.item.pos, focal_info_height, text=f"f' = {self.item.focal}", font=font
        )
        diameter_info = sketch.create_text(
            self.item.pos, diameter_info_height, text=f"o = {self.item.diameter}", font=font
        )

        return [focal_info, diameter_info]

    def draw_focus(self):
        font = "Helvetica 12 bold"
        focus_pos = [self.item.pos - self.item.focal, self.item.pos + self.item.focal]

        self.focus_img = (
            (
                self.sketch.create_line(
                    focus_pos[0],
                    self.sketch.axis.y - 10,
                    focus_pos[0],
                    self.sketch.axis.y + 10,
                    fill="red",
                    width=3,
                ),
                self.sketch.create_text(
                    focus_pos[0], self.sketch.axis.y - 20, text="F", fill="red", font=font
                ),
            ),
            (
                self.sketch.create_line(
                    focus_pos[1],
                    self.sketch.axis.y - 10,
                    focus_pos[1],
                    self.sketch.axis.y + 10,
                    fill="red",
                    width=3,
                ),
                self.sketch.create_text(
                    focus_pos[1], self.sketch.axis.y - 20, text="F'", fill="red", font=font
                ),
            ),
        )


class Point:

    height = 3
    width = 3

    def __init__(self, item, color="black") -> None:
        self.item = item
        self.color = color
        self.image = self.draw()


    def draw(self):
        if self.item.object_type == "user_defined":
            self.color = "red"
        return self.item.sketch.create_line(
            self.item.x, self.item.y - Point.height, self.item.x, self.item.y + Point.height, fill=self.color, width=Point.width
        )
    
    def redraw(self):
        self.delete_sprite()
        self.image = self.draw()

    def delete_sprite(self):
        self.item.sketch.delete(self.image)

    def bind_delete_object(self):
        self.item.sketch.tag_unbind(self.image, "<Button-1>")
        self.item.sketch.tag_bind(
            self.image, "<Button-1>", lambda event: self.item.delete_object_manually()
        )

    def bind_select_object(self):
        #self.item.sketch.tag_unbind(self.image, "<Button-1>")
        self.item.sketch.tag_bind(
            self.image, "<Button-1>", lambda event: self.item.select_object()
        )

    def unbind_all(self):
        self.item.sketch.tag_bind(
            id, "<Button-1>"
        )
            

class NumericAperture:

    width = 3

    def __init__(self, item, color="black") -> None:
        self.item = item
        self.color = color

        self.image = self.draw()


    def draw(self):
        if self.item.object_type == "resulting":
            return self.draw_resulting_aperture()
        else:
            upper_limit = 0
            lower_limit = self.item.sketch.height
            center = self.item.sketch.axis.y
            upper_end = center - self.item.diameter / 2
            lower_end = center + self.item.diameter / 2
            id = []
            id.append(
                self.item.sketch.create_line(
                    self.item.x - 3,
                    upper_end,
                    self.item.x + 4,
                    upper_end,
                    fill=self.color,
                    width=NumericAperture.width
                )
            )
            id.append(
                self.item.sketch.create_line(
                    self.item.x - 3,
                    lower_end,
                    self.item.x + 4,
                    lower_end,
                    fill=self.color,
                    width=NumericAperture.width
                )
            )
            id.append(
                self.item.sketch.create_line(
                    self.item.x, upper_end, self.item.x, upper_limit, fill=self.color, width=NumericAperture.width
                )
            )
            id.append(
                self.item.sketch.create_line(
                    self.item.x, lower_end, self.item.x, lower_limit, fill=self.color, width=NumericAperture.width
                )
            )
            return id
        

    def draw_resulting_aperture(self):
        center = self.item.sketch.axis.y
        upper_end = center - self.item.diameter / 2
        upper_limit = 0
        lower_end = center + self.item.diameter / 2
        lower_limit = self.item.sketch.height
        id = []
        id.append(
            self.item.sketch.create_line(
                self.item.x - 3,
                upper_end,
                self.item.x + 4,
                upper_end,
                fill=self.color,
                width=NumericAperture.width
            )
        )
        id.append(
            self.item.sketch.create_line(
                self.item.x - 3,
                lower_end,
                self.item.x + 4,
                lower_end,
                fill=self.color,
                width=NumericAperture.width
            )
        )

        #   MAKING CEASED LINE
        lines_space = 40

        starting_value = upper_end
        while starting_value > upper_limit:
            id.append(
                self.item.sketch.create_line(
                    self.item.x,
                    starting_value,
                    self.item.x,
                    starting_value - lines_space,
                    fill=self.color,
                    width=NumericAperture.width
                )
            )
            starting_value = starting_value - 1.5 * lines_space

        starting_value = lower_end
        while starting_value < lower_limit:
            id.append(
                self.item.sketch.create_line(
                    self.item.x,
                    starting_value,
                    self.item.x,
                    starting_value + lines_space,
                    fill=self.color,
                    width=NumericAperture.width
                )
            )
            starting_value = starting_value + 1.5 * lines_space

        return id
    
    def delete_sprite(self):
        for id in self.image:
            self.item.sketch.delete(id)


    def redraw(self):
        self.delete_sprite()
        self.image = self.draw()


    def bind_delete_object(self):
        for id in self.image:
            self.item.sketch.tag_unbind(id, "<Button-1>")
            self.item.sketch.tag_bind(
                id, "<Button-1>", lambda event: self.item.delete_object_manually()
            )

    def bind_select_object(self):
        for id in self.image:
            #self.item.sketch.tag_unbind(id, "<Button-1>")
            self.item.sketch.tag_bind(
                id, "<Button-1>", lambda event: self.item.select_object()
            )

    def unbind_all(self):
        for id in self.image:
            self.item.sketch.tag_bind(
                id, "<Button-1>"
            )




class NumericLensObject:

    def __init__(self, item, color="black") -> None:
        self.item = item
        self.color = color
        self.image = self.draw_lens()
        self.focus_image = self.draw_focus()
        #self.bind_select_object()



    def draw_lens(self):
        sketch = self.item.sketch
        center = sketch.axis.y
        if self.item.object_type == "user_defined":
            main_line = sketch.create_line(
                self.item.x,
                center - self.item.diameter / 2,
                self.item.x,
                center + self.item.diameter / 2,
                fill="black",
                width=3,
            )
            edges = self.draw_lens_edges(
                center - self.item.diameter / 2, center + self.item.diameter / 2, sketch
            )
            id = []
            id.append(main_line)
            id.extend(edges)
            return id
        elif self.item.object_type == "resulting":
            return self.draw_resulting_lens()

    def draw_lens_edges(self, upper_end, lower_end, sketch):
        edges = []
        if self.item.focal > 0:
            edges.append(
                sketch.create_line(
                    self.item.x, upper_end, self.item.x - 5, upper_end + 8, fill="black", width=3
                )
            )
            edges.append(
                sketch.create_line(
                    self.item.x, upper_end, self.item.x + 5, upper_end + 8, fill="black", width=3
                )
            )
            edges.append(
                sketch.create_line(
                    self.item.x, lower_end, self.item.x - 5, lower_end - 8, fill="black", width=3
                )
            )
            edges.append(
                sketch.create_line(
                    self.item.x, lower_end, self.item.x + 5, lower_end - 8, fill="black", width=3
                )
            )
        else:
            edges.append(
                sketch.create_line(
                    self.item.x, upper_end, self.item.x - 5, upper_end - 8, fill="black", width=3
                )
            )
            edges.append(
                sketch.create_line(
                    self.item.x, upper_end, self.item.x + 5, upper_end - 8, fill="black", width=3
                )
            )
            edges.append(
                sketch.create_line(
                    self.item.x, lower_end, self.item.x - 5, lower_end + 8, fill="black", width=3
                )
            )
            edges.append(
                sketch.create_line(
                    self.item.x, lower_end, self.item.x + 5, lower_end + 8, fill="black", width=3
                )
            )
        return edges

    def draw_focus(self):
        if self.item.object_type == "resulting":
            return None
        else:
            font = "Helvetica 10 bold"
            sketch = self.item.sketch
            focus_position = [self.item.x - self.item.focal, self.item.x + self.item.focal]

            focus_image = (
                (
                    sketch.create_line(
                        focus_position[0], sketch.axis.y - 5, focus_position[0], sketch.axis.y + 5, fill="red", width=3
                    ),
                    sketch.create_text(
                        focus_position[0], sketch.axis.y - 10, text="F", fill="red", font=font
                    ),
                ),
                (
                    sketch.create_line(
                        focus_position[1], sketch.axis.y - 5, focus_position[1], sketch.axis.y + 5, fill="red", width=3
                    ),
                    sketch.create_text(
                        focus_position[1], sketch.axis.y - 10, text="F'", fill="red", font=font
                    ),
                ),
            )

            return focus_image
    

    def delete_focus_image(self):
        for pair in self.focus_image:
            for id in pair:
                self.item.sketch.delete(id)


    def delete_sprite(self):
        if self.focus_image is not None:  
            self.delete_focus_image()
        for id in self.image:
            self.item.sketch.delete(id)

    
    def redraw(self):
        #self.delete_focus_image()
        self.delete_sprite()
        self.image = self.draw_lens()
        self.focus_image = self.draw_focus()



    def bind_delete_object(self):
        for id in self.image:
            self.item.sketch.tag_unbind(id, "<Button-1>")
            self.item.sketch.tag_bind(
                id, "<Button-1>", lambda event: self.item.delete_object_manually()
            )

    def bind_select_object(self):
        for id in self.image:
            #self.item.sketch.tag_unbind(id, "<Button-1>")
            self.item.sketch.tag_bind(
                id, "<Button-1>", lambda event: self.item.select_object()
            )

    def unbind_all(self):
        for id in self.image:
            self.item.sketch.tag_bind(
                id, "<Button-1>"
            )


    def draw_resulting_lens(self):
        center = self.item.sketch.axis.y
        upper_end = center - self.item.diameter / 2
        upper_limit = 0
        lower_end = center + self.item.diameter / 2
        lower_limit = self.item.sketch.height
        id = []
        id.append(
            self.item.sketch.create_line(
                self.item.x - 3,
                upper_end,
                self.item.x + 4,
                upper_end,
                fill=self.color,
                width=NumericAperture.width
            )
        )
        id.append(
            self.item.sketch.create_line(
                self.item.x - 3,
                lower_end,
                self.item.x + 4,
                lower_end,
                fill=self.color,
                width=NumericAperture.width
            )
        )

        #   MAKING CEASED LINE
        lines_space = 40

        starting_value = upper_end
        while starting_value > upper_limit:
            id.append(
                self.item.sketch.create_line(
                    self.item.x,
                    starting_value,
                    self.item.x,
                    starting_value - lines_space,
                    fill=self.color,
                    width=NumericAperture.width
                )
            )
            starting_value = starting_value - 1.5 * lines_space

        starting_value = lower_end
        while starting_value < lower_limit:
            id.append(
                self.item.sketch.create_line(
                    self.item.x,
                    starting_value,
                    self.item.x,
                    starting_value + lines_space,
                    fill=self.color,
                    width=NumericAperture.width
                )
            )
            starting_value = starting_value + 1.5 * lines_space

        return id
    

class NumericRay:

    def delete(self):
        self.item.sketch.delete(self.image)

    def bind_delete_ray(self):
        self.item.sketch.tag_unbind(self.image, "<Button-1>")
        self.item.sketch.tag_bind(
            self.image, "<Button-1>", lambda event: self.item.delete_ray_manually()
        )

    def bind_select_ray(self):
        self.item.sketch.tag_unbind(self.image, "<Button-1>")
        self.item.sketch.tag_bind(
            self.image, "<Button-1>", lambda event: self.item.select_ray()
        )


class NumericApertureRay(NumericRay):

    def __init__(self, item) -> None:
        self.item = item
        self.image = self.draw()
        self.bind_select_ray()

    def draw(self):
        x1, y1 = self.item.ray_coords[0][0], self.item.ray_coords[0][1]
        x2, y2 = self.item.ray_coords[1][0], self.item.ray_coords[1][1]
        return self.item.sketch.create_line(x1, y1, x2, y2, fill="red", width=2)

    

class NumericFieldRay(NumericRay):

    def __init__(self, item) -> None:
        self.item = item
        self.image = self.draw()
        self.bind_select_ray()

    def draw(self):
        x1, y1 = self.item.ray_coords[0][0], self.item.ray_coords[0][1]
        x2, y2 = self.item.ray_coords[1][0], self.item.ray_coords[1][1]

        return self.item.sketch.create_line(x1, y1, x2, y2, fill="blue", width=2)