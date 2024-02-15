import numpy as np
from PIL import ImageTk, Image
import tkinter as tk
import algorithm as alg


def lens_toggle_render(sketch):
    #Axis.render_axis(sketch)
    #Point.hide_last_points_rays(sketch)
    #Point.render_points(sketch)
    Point.redefine_after_toggling_lens(sketch)
    GraphicLens.render_after_toggling(sketch)


def temp_text(e, entry):
   entry.delete(0,"end")


def delete_object(object):
    del object
    


class Axis:

    main_axis = None

    def __init__(self, sketch, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.img = self.draw(sketch)
        Axis.main_axis = self


    def draw(self, sketch, color="grey", width=3):
        return sketch.canv.create_line(self.x1, self.y1, self.x2, self.y2, fill=color, width=width)


    def render_axis(sketch):
        Axis.main_axis.img = Axis.main_axis.draw(sketch)



class Lens:

    lens = None
    
    def __init__(self, focal, pos):
        self.pos = pos
        self.x = pos
        self.focal = focal
        self.type = self.determine_type()

    def determine_type(self):
        if self.focal > 0:
            print("positive")
            return "positive"
        else:
            print("negative")
            return "negative"

    



class GraphicLens(Lens):

    lens = None
    
    def __init__(self, sketch, focal, pos, space, in_out_factor=1):
        super().__init__(focal, pos)
        self.space = space
        self.in_out_factor = in_out_factor
        

        self.draw_lens(sketch, pos, space)

        self.draw_focus(sketch, pos, space, focal)

        self.relative_zero_point = self.determine_relative_zero_point()

        GraphicLens.lens = self

        print(f"F: {self.focus_pos[0][0]}x{self.focus_pos[0][1]}")
        print(f"F': {self.focus_pos[1][0]}x{self.focus_pos[1][1]}")
        print(self.space)

    
    def __del__(self):
        print("Deleted the lens")

    def determine_relative_zero_point(self):
        if self.type == "positive":
            return [self.pos+self.space/2, 200]
        elif self.type == "negative":
            return [self.pos-self.space/2, 200]
        

    def draw_lens(self, sketch, pos, space):
        if self.type == "positive":
            self.real_imaginary_boundary = pos-space/2
            return self.draw_positive_lens(sketch, pos, space)
        elif self.type == "negative":
            self.real_imaginary_boundary = pos+space/2
            return self.draw_negative_lens(sketch, pos, space)


    def draw_positive_lens(self, sketch, pos, space):
        font = ('Helvetica 12 bold')
        self.lens_xpos = [pos-space/2, pos+space/2]

        self.lens_img = ((sketch.canv.create_line(self.lens_xpos[0], 20, self.lens_xpos[0], 380, fill="black", width=2),
                         sketch.canv.create_text(self.lens_xpos[0], 10, text="H", fill="black", font=font)),
                        (sketch.canv.create_line(self.lens_xpos[1], 20, self.lens_xpos[1], 380, fill="black", width=2),
                         sketch.canv.create_text(self.lens_xpos[1], 10, text="H'", fill="black", font=font)))


    def draw_negative_lens(self, sketch, pos, space):
        font = ('Helvetica 12 bold')
        self.lens_xpos = [pos+space/2, pos-space/2]

        self.lens_img = ((sketch.canv.create_line(self.lens_xpos[0], 20, self.lens_xpos[0], 380, fill="black", width=2),
                         sketch.canv.create_text(self.lens_xpos[0], 10, text="H", fill="black", font=font)),
                        (sketch.canv.create_line(self.lens_xpos[1], 20, self.lens_xpos[1], 380, fill="black", width=2),
                         sketch.canv.create_text(self.lens_xpos[1], 10, text="H'", fill="black", font=font)))
        

    def draw_focus(self, sketch, pos, space, focal):
        if self.type == "positive":
            return self.draw_positive_focus(sketch, pos, space, focal)
        elif self.type == "negative":
            return self.draw_negative_focus(sketch, pos, space, focal)
        

    def draw_positive_focus(self, sketch, pos, space, focal):
        font = ('Helvetica 12 bold')
        self.focus_pos = [[pos-space/2-focal, 200], [pos+space/2+focal, 200]]

        self.focus_img = ((sketch.canv.create_line(self.focus_pos[0][0], 190, self.focus_pos[0][0], 210, fill="red", width=3),
                         sketch.canv.create_text(self.focus_pos[0][0], 180, text="F", fill="red", font=font)),
                        (sketch.canv.create_line(self.focus_pos[1][0], 190, self.focus_pos[1][0], 210, fill="red", width=3),
                         sketch.canv.create_text(self.focus_pos[1][0], 180, text="F'", fill="red", font=font)))


    def draw_negative_focus(self, sketch, pos, space, focal):
        font = ('Helvetica 12 bold')
        self.focus_pos = [[pos+space/2-focal, 200], [pos-space/2+focal, 200]]

        self.focus_img = ((sketch.canv.create_line(self.focus_pos[0][0], 190, self.focus_pos[0][0], 210, fill="red", width=3),
                         sketch.canv.create_text(self.focus_pos[0][0], 180, text="F", fill="red", font=font)),
                        (sketch.canv.create_line(self.focus_pos[1][0], 190, self.focus_pos[1][0], 210, fill="red", width=3),
                         sketch.canv.create_text(self.focus_pos[1][0], 180, text="F'", fill="red", font=font)))
    
    def erase_image(self, sketch):
        self.erase_lens_img(sketch)
        self.erase_focus_img(sketch)

    def erase_lens_img(self, sketch):
        for side in self.lens_img:
            for image in side:
                sketch.canv.delete(image)
        
    def erase_focus_img(self, sketch):
        for side in self.focus_img:
            for image in side:
                sketch.canv.delete(image)

            
    @staticmethod
    def render_lens(sketch):
        GraphicLens.lens.erase_image(sketch)
        GraphicLens.lens.draw_lens(sketch, GraphicLens.lens.pos, GraphicLens.lens.space)
        GraphicLens.lens.draw_focus(sketch, GraphicLens.lens.pos, GraphicLens.lens.space, GraphicLens.lens.focal)

    @staticmethod
    def render_after_toggling(sketch):
        Axis.render_axis(sketch)
        GraphicLens.render_lens(sketch)
        Point.render_points(sketch)
        Shape.render_shapes(sketch)



class NumericLens(Lens):
    
    def __init__(self, sketch, focal=100, diameter=50, pos=400):
        super().__init__(focal, pos)
        self.diameter = diameter
        self.id = self.draw_lens(sketch)
        self.lens_info = self.draw_lens_info(sketch)
        print(self.id)
        self.draw_focus(sketch, pos, focal)

    def draw_lens(self, sketch):

        center = sketch.axis.y1
        main_line = sketch.canv.create_line(self.pos, center-self.diameter/2, self.pos, center+self.diameter/2, fill="black", width=3)
        edges = self.draw_lens_edges(center-self.diameter/2, center+self.diameter/2, sketch)

        id = []
        id.append(main_line)
        id.extend(edges)
        return id
    
    def draw_lens_edges(self, upper_end, lower_end, sketch):
        edges = []
        if self.type == "positive":
            edges.append(sketch.canv.create_line(self.pos, upper_end, self.pos - 5, upper_end + 8, fill="black", width=3))
            edges.append(sketch.canv.create_line(self.pos, upper_end, self.pos + 5, upper_end + 8, fill="black", width=3))
            edges.append(sketch.canv.create_line(self.pos, lower_end, self.pos - 5, lower_end - 8, fill="black", width=3))
            edges.append(sketch.canv.create_line(self.pos, lower_end, self.pos + 5, lower_end - 8, fill="black", width=3))
        else:
            edges.append(sketch.canv.create_line(self.pos, upper_end, self.pos - 5, upper_end - 8, fill="black", width=3))
            edges.append(sketch.canv.create_line(self.pos, upper_end, self.pos + 5, upper_end - 8, fill="black", width=3))
            edges.append(sketch.canv.create_line(self.pos, lower_end, self.pos - 5, lower_end + 8, fill="black", width=3))
            edges.append(sketch.canv.create_line(self.pos, lower_end, self.pos + 5, lower_end + 8, fill="black", width=3))
        return edges
    
    def draw_lens_info(self, sketch):
        font = ('Helvetica 8 bold')
        focal_info_height = sketch.axis.y1 + self.diameter/2 + 16
        diameter_info_height = focal_info_height + 16
        focal_info = sketch.canv.create_text(self.pos, focal_info_height, text=f"f' = {self.focal}", font=font)
        diameter_info = sketch.canv.create_text(self.pos, diameter_info_height, text=f"o = {self.diameter}", font=font)

        return [focal_info, diameter_info]

    def draw_focus(self, sketch, pos, focal):
        font = ('Helvetica 12 bold')
        self.focus_pos = [[pos-focal, 200], [pos+focal, 200]]

        self.focus_img = ((sketch.canv.create_line(self.focus_pos[0][0], 190, self.focus_pos[0][0], 210, fill="red", width=3),
                         sketch.canv.create_text(self.focus_pos[0][0], 180, text="F", fill="red", font=font)),
                        (sketch.canv.create_line(self.focus_pos[1][0], 190, self.focus_pos[1][0], 210, fill="red", width=3),
                         sketch.canv.create_text(self.focus_pos[1][0], 180, text="F'", fill="red", font=font)))



class Object:

    def __init__(self, x, y, color="black") -> None:
        self.x = x
        self.y = y
        self.color = color




class Point(Object):

    r = 2
    points = []
    resulting_points = {}


    def __init__(self, x, y, sketch, type="user_defined", in_shape = None) -> None:
        super().__init__(x, y)
        self.type = type
        self.rays = []
        self.show_rays = True
        self.in_shape = in_shape

        

        if type == "user_defined":
            if y == sketch.axis.y1:
                y = y - 10
                self.y = y
                self.define_rays(sketch, x)
                self.point_img = self.place(sketch, x, y)
                sketch.canv.tag_bind(self.point_img, "<Enter>",  lambda event: sketch.cursor_over_point(self))
                sketch.canv.tag_bind(self.point_img, "<Leave>",  lambda event: sketch.cursor_left_point())
                sketch.canv.tag_bind(self.point_img, "<Button-1>",  self.print_out)
                sketch.canv.tag_bind(self.point_img, "<Button-2>",  lambda event: Point.toggle_rays(self, sketch))
                sketch.canv.tag_bind(self.point_img, "<ButtonRelease-1>", lambda event: self.move_point(event, sketch))
                sketch.points.append(self)
                self.define_resulting_point(sketch)
                self.place_point_on_axis(sketch)
                self.its_image_point.place_point_on_axis(sketch)
            else:
                self.define_rays(sketch, x)
                self.point_img = self.place(sketch, x, y)
                sketch.canv.tag_bind(self.point_img, "<Enter>",  lambda event: sketch.cursor_over_point(self))
                sketch.canv.tag_bind(self.point_img, "<Leave>",  lambda event: sketch.cursor_left_point())
                sketch.canv.tag_bind(self.point_img, "<Button-1>",  self.print_out)
                sketch.canv.tag_bind(self.point_img, "<Button-2>",  lambda event: Point.toggle_rays(self, sketch))
                sketch.canv.tag_bind(self.point_img, "<ButtonRelease-1>", lambda event: self.move_point(event, sketch))
                sketch.points.append(self)
                self.define_resulting_point(sketch)    
            

        elif type == "resulting":
            self.point_img = self.place(sketch, x, y)
            sketch.canv.tag_bind(self.point_img, "<Button-2>",  lambda event: Point.toggle_rays(list(sketch.resulting_points.keys())[list(sketch.resulting_points.values()).index(self)], sketch))
            sketch.resulting_points.update({sketch.points[-1]: self})

        elif type == "line":
            if y == sketch.axis.y1:
                y = y - 10
                self.y = y
                self.define_rays(sketch, x)
                self.point_img = self.place(sketch, x, y)
                sketch.canv.tag_bind(self.point_img, "<Enter>",  lambda event: sketch.cursor_over_point(self))
                sketch.canv.tag_bind(self.point_img, "<Leave>",  lambda event: sketch.cursor_left_point())
                sketch.canv.tag_bind(self.point_img, "<Button-1>",  self.print_out)
                sketch.canv.tag_bind(self.point_img, "<Button-2>",  lambda event: Point.toggle_rays(self, sketch))
                sketch.points.append(self)
                self.define_resulting_point(sketch)
                self.place_point_on_axis(sketch)
                self.its_image_point.place_point_on_axis(sketch)
            else:
                self.define_rays(sketch, x)
                self.point_img = self.place(sketch, x, y)
                sketch.canv.tag_bind(self.point_img, "<Enter>",  lambda event: sketch.cursor_over_point(self))
                sketch.canv.tag_bind(self.point_img, "<Leave>",  lambda event: sketch.cursor_left_point())
                sketch.canv.tag_bind(self.point_img, "<Button-1>",  self.print_out)
                sketch.canv.tag_bind(self.point_img, "<Button-2>",  lambda event: Point.toggle_rays(self, sketch))
                sketch.points.append(self)
                self.define_resulting_point(sketch)
            
            Point.hide_rays(self, sketch)
            
        elif type == "line_res":
            self.point_img = self.place(sketch, x, y)
            sketch.resulting_points.update({sketch.points[-1]: self})
            
        
        print (f"COORDS: {self.x} x {self.y}")

        print(f"POINTS AMMOUNT: {len(sketch.points)}")
        print(f"RESULTING POINTS AMMOUNT: {len(sketch.resulting_points)}")


    def __del__(self):
        ...
        

    def place(self, sketch, x, y):

        if self.type == "user_defined" or self.type == "line":
            Axis.render_axis(sketch)
            GraphicLens.render_lens(sketch)

        if self.type == "user_defined":
            Point.hide_last_points_rays(sketch)
            Point.render_points(sketch)
            Shape.render_shapes(sketch)

        if self.type == "user_defined":
            return sketch.canv.create_oval(x - Point.r, y - Point.r, x + Point.r, y + Point.r, outline="black", fill="white")
        elif self.type == "resulting":
            return sketch.canv.create_oval(x - 2*Point.r, y - 2*Point.r, x + 2*Point.r, y + 2*Point.r, outline="green", fill="blue")
        elif self.type == "line":
            return sketch.canv.create_oval(x - Point.r, y - Point.r, x + Point.r, y + Point.r, outline="red", fill="red")
        elif self.type == "line_res":
            return sketch.canv.create_oval(x - 2*Point.r, y - 2*Point.r, x + 2*Point.r, y + 2*Point.r, outline="orange", fill="orange")
        

    def define_rays(self, sketch, x):

        if sketch.lens.type == "positive":
            if x <= GraphicLens.lens.real_imaginary_boundary:
                #first real
                self.rays.append([Ray(0, self.y, sketch.lens.lens_xpos[0], self.y, sketch),
                                Ray(sketch.lens.relative_zero_point[0], self.y, sketch.lens.focus_pos[1][0]+3*(sketch.lens.focus_pos[1][0]-sketch.lens.relative_zero_point[0]), sketch.lens.focus_pos[1][1]+3*(sketch.lens.focus_pos[1][1]-self.y), sketch)
                                ])

                #second real
                self.rays.append([Ray(sketch.lens.lens_xpos[0]-3*(sketch.lens.lens_xpos[0]-self.x), 200-3*(200-self.y), sketch.lens.lens_xpos[0], 200, sketch),
                                Ray(sketch.lens.relative_zero_point[0], 200, sketch.lens.relative_zero_point[0]+3*(sketch.lens.lens_xpos[0]-self.x), 200+3*(200-self.y), sketch)
                                ])

                if x > GraphicLens.lens.focus_pos[0][0]:
                    #first imaginary
                    self.rays.append([#Ray(sketch.lens.lens_xpos[0], self.y, 800, self.y, sketch, num=0),
                                    Ray(sketch.lens.focus_pos[1][0]-3*(sketch.lens.focus_pos[1][0]-sketch.lens.relative_zero_point[0]), sketch.lens.focus_pos[1][1]-3*(sketch.lens.focus_pos[1][1]-self.y), sketch.lens.relative_zero_point[0], self.y, sketch, type='im')
                                    ])
                    
                    #second imaginary
                    self.rays.append([#Ray(sketch.lens.lens_xpos[0], 200, sketch.lens.lens_xpos[0]+3*(sketch.lens.lens_xpos[0]-self.x), 200+3*(200-self.y), sketch, num=0),
                                    Ray(sketch.lens.relative_zero_point[0]-3*(sketch.lens.lens_xpos[0]-self.x), 200-3*(200-self.y), sketch.lens.relative_zero_point[0], 200, sketch, type='im')
                                    ])

            else:
                
                self.rays.append([Ray(0, self.y, sketch.lens.lens_xpos[0], self.y, sketch),
                                Ray(sketch.lens.relative_zero_point[0], self.y, sketch.lens.focus_pos[1][0]+3*(sketch.lens.focus_pos[1][0]-sketch.lens.relative_zero_point[0]), sketch.lens.focus_pos[1][1]+3*(sketch.lens.focus_pos[1][1]-self.y), sketch)
                                ])
                self.rays.append([Ray(sketch.lens.lens_xpos[0]+3*(sketch.lens.lens_xpos[0]-self.x), 200+3*(200-self.y), sketch.lens.lens_xpos[0], 200, sketch),
                                Ray(sketch.lens.relative_zero_point[0], 200, sketch.lens.relative_zero_point[0]-3*(sketch.lens.lens_xpos[0]-self.x), 200-3*(200-self.y), sketch)
                                ])

            if self.rays[0][1].func['a'] == self.rays[1][1].func['a']:
                print("LINES ARE PARALLEL")

            print(f"RAY 1: {self.rays[0][1].func['a']}, {self.rays[0][1].func['b']}")
            print(f"RAY 2: {self.rays[1][1].func['a']}, {self.rays[1][1].func['b']}")

        elif sketch.lens.type == "negative":
            if x <= GraphicLens.lens.real_imaginary_boundary:
                #first real
                self.rays.append([Ray(0, self.y, sketch.lens.lens_xpos[0], self.y, sketch),
                                #Ray(sketch.lens.relative_zero_point[0], self.y, sketch.lens.focus_pos[1][0]+3*(sketch.lens.focus_pos[1][0]-sketch.lens.relative_zero_point[0]), sketch.lens.focus_pos[1][1]+3*(sketch.lens.focus_pos[1][1]-self.y), sketch)])
                                Ray(sketch.lens.relative_zero_point[0], self.y, sketch.lens.relative_zero_point[0]+3*(sketch.lens.relative_zero_point[0]-sketch.lens.focus_pos[1][0]), self.y+3*(self.y-sketch.lens.focus_pos[1][1]), sketch)
                                ])

                #second real
                self.rays.append([Ray(sketch.lens.lens_xpos[0]-3*(sketch.lens.lens_xpos[0]-self.x), 200-3*(200-self.y), sketch.lens.lens_xpos[0], 200, sketch),
                                Ray(sketch.lens.relative_zero_point[0], 200, sketch.lens.relative_zero_point[0]+3*(sketch.lens.lens_xpos[0]-self.x), 200+3*(200-self.y), sketch)
                                ])
                                #Ray(sketch.lens.relative_zero_point[0], 200, sketch.lens.relative_zero_point[0]+3*(sketch.lens.lens_xpos[0]-self.x), 200+3*(200-self.y), sketch)])
                                

                if x > GraphicLens.lens.focus_pos[0][0]:
                    #first imaginary
                    self.rays.append([#Ray(sketch.lens.lens_xpos[0], self.y, 800, self.y, sketch, num=0),
                                    Ray(sketch.lens.focus_pos[1][0]-3*(sketch.lens.focus_pos[1][0]-sketch.lens.relative_zero_point[0]), sketch.lens.focus_pos[1][1]-3*(sketch.lens.focus_pos[1][1]-self.y), sketch.lens.relative_zero_point[0], self.y, sketch, type='im')
                                    ])
                    
                    #second imaginary
                    self.rays.append([#Ray(sketch.lens.lens_xpos[0], 200, sketch.lens.lens_xpos[0]+3*(sketch.lens.lens_xpos[0]-self.x), 200+3*(200-self.y), sketch, num=0),
                                    Ray(sketch.lens.relative_zero_point[0]-3*(sketch.lens.lens_xpos[0]-self.x), 200-3*(200-self.y), sketch.lens.relative_zero_point[0], 200, sketch, type='im')
                                    ])

            else:
                
                self.rays.append([Ray(0, self.y, sketch.lens.lens_xpos[0], self.y, sketch),
                                Ray(sketch.lens.relative_zero_point[0], self.y, sketch.lens.focus_pos[1][0]+3*(sketch.lens.focus_pos[1][0]-sketch.lens.relative_zero_point[0]), sketch.lens.focus_pos[1][1]+3*(sketch.lens.focus_pos[1][1]-self.y), sketch)
                                ])
                self.rays.append([Ray(sketch.lens.lens_xpos[0]+3*(sketch.lens.lens_xpos[0]-self.x), 200+3*(200-self.y), sketch.lens.lens_xpos[0], 200, sketch),
                                Ray(sketch.lens.relative_zero_point[0], 200, sketch.lens.relative_zero_point[0]-3*(sketch.lens.lens_xpos[0]-self.x), 200-3*(200-self.y), sketch)
                                ])

            if self.rays[0][1].func['a'] == self.rays[1][1].func['a']:
                print("LINES ARE PARALLEL")

            print(f"RAY 1: {self.rays[0][1].func['a']}, {self.rays[0][1].func['b']}")
            print(f"RAY 2: {self.rays[1][1].func['a']}, {self.rays[1][1].func['b']}")




    def define_resulting_point(self, sketch):
        new_point_coords = rays_intersection(self.rays[0][1], self.rays[1][1], sketch.lens)

        if self.type == "line":
            self.its_image_point = Point(new_point_coords[0], new_point_coords[1], sketch, type="line_res")
        else:
            self.its_image_point = Point(new_point_coords[0], new_point_coords[1], sketch, type="resulting")


    def print_out(self, event):
        print(f"COORDS: {self.x} x {self.y}, ID: {self.point_img}")


    def delete_point(self, sketch):
        if self.type == "user_defined" or self.type == "line":
            Point.delete_rays(self, sketch)
            print(self)
            sketch.canv.delete(self.point_img)
            sketch.canv.delete(self.its_image_point.point_img)
            sketch.resulting_points.pop(self)
            sketch.points.remove(self)
            del(self)
            print(f"DELETED POINT, REMAINING: {len(sketch.points)}")
        elif self.type == "resulting" or self.type == "line_res":
            sketch.canv.delete(self.point_img)
            del(self)

    def delete_point_manually(self, sketch):
        self.delete_point(sketch)

    def erase_rays(self, sketch):
        for rays_group in self.rays:
            for ray in rays_group:
                ray.erase(sketch)
        self.rays.clear()

    def erase_resulting_point(self, sketch):
        self.its_image_point.delete_point(sketch)

    def move_point(self, event, sketch):
        print(f"MOVED, COORDS: {event.x} x {event.y}, POINT'S ID: {self.point_img}")
        shape_var = self.in_shape
        new_point = Point(event.x, event.y, sketch, in_shape=shape_var)
        if shape_var is not None:
            self.in_shape.swap_points(self, new_point)
            self.in_shape.render_shape(sketch)
        else:
            print("test")
        self.delete_point(sketch)
        

    def redefine_rays(self, sketch):
        self.erase_rays(sketch)
        self.define_rays(sketch, self.x)
        Point.unhide_rays(self, sketch)


    def redefine_resulting_point(self, sketch):
        self.erase_resulting_point(sketch)
        self.define_resulting_point(sketch)
        
    
    def redraw_point(self, sketch):
        sketch.canv.delete(self.point_img)
        self.point_img = sketch.canv.create_oval(self.x - Point.r, self.y - Point.r, self.x + Point.r, self.y + Point.r, outline="black", fill="white")
        sketch.canv.tag_bind(self.point_img, "<Enter>",  lambda event: sketch.cursor_over_point(self))
        sketch.canv.tag_bind(self.point_img, "<Leave>",  lambda event: sketch.cursor_left_point())
        sketch.canv.tag_bind(self.point_img, "<Button-1>",  self.print_out)
        sketch.canv.tag_bind(self.point_img, "<Button-2>",  lambda event: Point.toggle_rays(self, sketch))
        sketch.canv.tag_bind(self.point_img, "<ButtonRelease-1>", lambda event: self.move_point(event, sketch))
        #sketch.canv.tag_bind(self.point_img, "<ButtonRelease-3>", lambda event: self.delete_point_manually(sketch))
        mirrored = self.its_image_point

        sketch.canv.delete(mirrored.point_img)
        mirrored.point_img = sketch.canv.create_oval(mirrored.x - Point.r, mirrored.y - Point.r, mirrored.x + Point.r, mirrored.y + Point.r, outline="blue", fill="blue")
        sketch.canv.tag_bind(mirrored.point_img, "<Button-2>",  lambda event: Point.toggle_rays(list(sketch.resulting_points.keys())[list(sketch.resulting_points.values()).index(mirrored)], sketch))

    def place_point_on_axis(self, sketch):
        self.y = sketch.axis.y1
        if self.type == "user_defined":
            return sketch.canv.create_oval(self.x - Point.r, self.y - Point.r, self.x + Point.r, self.y + Point.r, outline="black", fill="white")
        elif self.type == "resulting":
            return sketch.canv.create_oval(self.x - 2*Point.r, self.y - 2*Point.r, self.x + 2*Point.r, self.y + 2*Point.r, outline="green", fill="blue")



    @staticmethod
    def delete_rays(point, sketch):
        for main_ray in point.rays:
            for ray in main_ray:
                sketch.canv.delete(ray.img_id)


    @staticmethod
    def hide_rays(point, sketch):
        for main_ray in point.rays:
            for ray in main_ray:
                sketch.canv.itemconfig(ray.img_id, fill="white")
            
    @staticmethod
    def unhide_rays(point, sketch):
        for main_ray in point.rays:
            for ray in main_ray:
                if ray.type == "re":
                    sketch.canv.itemconfig(ray.img_id, fill="black")
                elif ray.type == "im":
                    sketch.canv.itemconfig(ray.img_id, fill="light grey")

    @staticmethod
    def toggle_rays(point, sketch):
        if point.show_rays:
            Point.hide_rays(point, sketch)
            point.show_rays = False
        else:
            Point.unhide_rays(point, sketch)
            point.show_rays = True


    @staticmethod
    def hide_last_points_rays(sketch):
        if len(sketch.points) > 0:
            processed_point = sketch.points[-1]
            sketch.canv.itemconfig(processed_point.point_img, fill="red")
            Point.hide_rays(processed_point, sketch)

    @staticmethod
    def redefine_after_toggling_lens(sketch):

        for point in sketch.points:
            point.redefine_rays(sketch)
            point.redefine_resulting_point(sketch)

        Point.render_points(sketch)
        

    @staticmethod
    def render_points(sketch):
        if len(sketch.points) > 0:

            for point in sketch.points:
                point.redraw_point(sketch)

    


class Line:

    def __init__(self, point_1: Point, point_2: Point, sketch, type="shape"):
        self.point_1 = point_1
        self.point_2 = point_2
        self.x1 = point_1.x
        self.y1 = point_1.y
        self.x2 = point_2.x
        self.y2 = point_2.y
        self.type = type

        self.img_id = self.draw(sketch)

        if self.type == "shape":
            try:
                self.func = {'a': (self.y2-self.y1)/(self.x2-self.x1), "carthesian_coords" : (self.x1, self.y1)}
            except ZeroDivisionError:                       #   RATHER RETURN "A" COEFFICIENT AS NONE
                self.func = {'a': None, "carthesian_coords" : (self.x1, self.y1)}

            self.boundary_points = {}
            self.focus_intersection = self.check_focus_intersection(sketch)

            print(self.func)        
            print(self.focus_intersection)


    def draw(self, sketch):
        if self.type == "shape":
            return sketch.canv.create_line(self.x1, self.y1, self.x2, self.y2, fill="black", width=3)
        elif self.type == "shape_res":
            return sketch.canv.create_line(self.x1, self.y1, self.x2, self.y2, fill="red", width=3)


    def check_focus_intersection(self, sketch) -> bool:
        if self.x1 < self.x2:   
            if sketch.lens.focus_pos[0][0] >= self.x1 and sketch.lens.focus_pos[0][0] <= self.x2:
                self.points_nearby_focus(sketch, self.point_1, self.point_2)
                return True
            else:
                return False
        else:
            if sketch.lens.focus_pos[0][0] >= self.x2 and sketch.lens.focus_pos[0][0] <= self.x1:
                self.points_nearby_focus(sketch, self.point_2, self.point_1)
                return True
            else:
                return False

    def points_nearby_focus(self, sketch, point_1, point_2):
        x = sketch.lens.focus_pos[0][0] - 1
        y = self.func['carthesian_coords'][1] + self.func['a']*(x-self.func['carthesian_coords'][0])
        new_boundary_point = Point(x, y, sketch, "line")
        self.boundary_points.update({point_1 : new_boundary_point})

        x = sketch.lens.focus_pos[0][0] + 1
        y = self.func['carthesian_coords'][1] + self.func['a']*(x-self.func['carthesian_coords'][0])
        new_boundary_point = Point(x, y, sketch, "line")
        self.boundary_points.update({point_2 : new_boundary_point})


    def delete_boundary_points(self, sketch):
        points = list(self.boundary_points.values())
        for point in points:
            point.delete_point(sketch)


    def delete_line(self, sketch):
        if self.type == "shape":
            self.delete_boundary_points(sketch)
        sketch.canv.delete(self.img_id)
        del(self)



class Shape(Object):

    shapes = []
    initial_points = []


    def __init__(self, x, y, points: list, sketch, type="user_defined", color="black") -> None:
        super().__init__(x, y, color)
        self.points = points.copy()
        self.shape = self.build_shape(sketch)
        self.resulting_shape = self.build_resulting_shape(sketch)

        for point in self.points:
            point.redraw_point(sketch)

        self.type = type

        self.mark_points(self.points)
        
        sketch.shapes.append(self)


    def build_shape(self, sketch):
        lines = []
        for index in range(0, len(self.points)-1):
            new_line = Line(self.points[index], self.points[index+1], sketch)
            lines.append(new_line)

        if len(self.points) > 2:
            index = len(self.points)-1
            new_line = Line(self.points[index], self.points[0], sketch)
            lines.append(new_line)

        print(f"SHAPE'S SIZE: {len(lines)}")

        for x in self.points:
            try:
                print(f"{x} -> {sketch.resulting_points[x]}")
            except KeyError:
                print(f"{x} -> NONE")
                sketch.canv.itemconfig(x.point_img, fill="orange")

        return lines


    def build_resulting_shape(self, sketch):
        width = 1
        lines = [] 
        for line in self.shape:
            if line.focus_intersection == True:
                new_line = Line(sketch.resulting_points[line.point_1], sketch.resulting_points[line.boundary_points[line.point_1]], sketch, "shape_res")
                lines.append(new_line)
                new_line = Line(sketch.resulting_points[line.point_2], sketch.resulting_points[line.boundary_points[line.point_2]], sketch, "shape_res")
                lines.append(new_line)
            else:
                new_line = Line(sketch.resulting_points[line.point_1], sketch.resulting_points[line.point_2], sketch, "shape_res")
                lines.append(new_line)
            
        return lines


    def delete_shape(self, sketch):
        self.erase_shape_lines(sketch)
        self.erase_shape_points(sketch)
        del(self)


    def erase_shape_lines(self, sketch):
        for line in self.resulting_shape:
            line.delete_line(sketch)
        self.resulting_shape.clear()

        for line in self.shape: 
            line.delete_line(sketch)
        self.shape.clear()
            
    

    def erase_shape_points(self, sketch):
        for point in self.points:
            point.delete_point(sketch)


    def swap_points(self, point_1, point_2):
        self.points.insert(self.points.index(point_1), point_2)
        self.points.remove(point_1)


    def render_shape(self, sketch): 
        self.erase_shape_lines(sketch)

        self.shape = []
        self.shape = self.build_shape(sketch)

        for line in self.resulting_shape:
            sketch.canv.delete(line)
        self.resulting_shape = []
        self.resulting_shape = self.build_resulting_shape(sketch)

        for point in self.points:
            point.redraw_point(sketch)


    @staticmethod
    def render_shapes(sketch):
        for shape in sketch.shapes:
            shape.render_shape(sketch)
            print(f"RENDERING SHAPE NO. {sketch.shapes.index(shape)+1}")

    
    def mark_points(self, points):
        for point in points:
            self.shape_of_point(point)
            

    def shape_of_point(self, point):
        point.in_shape = self

    

class Ray:

    def __init__(self, x1, y1, x2, y2, sketch, type = "re"):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.type = type
 
        try:
            self.func = {'a': (y2-y1)/(x2-x1), 'b': y1-200}
        except ZeroDivisionError:
            self.func = {'a': float('inf'), 'b': y1-200}

        self.img_id = self.draw(sketch)


    def draw(self, sketch):
        if self.type == "re":
            return sketch.canv.create_line(self.x1, self.y1, self.x2, self.func['a']*(self.x2-self.x1)+self.y1, fill="black")
        elif self.type == "im":
            return sketch.canv.create_line(self.x1, self.y1, self.x2, self.func['a']*(self.x2-self.x1)+self.y1, fill="light grey")

    def erase(self, sketch):
        sketch.canv.delete(self.img_id)



def rays_intersection(ray_1: Ray, ray_2: Ray, lens: GraphicLens):
    
    #IF A_1 == A_2 -> they never intersect
    
    main_matrix = np.array([[ray_1.func['a'], -1], [ray_2.func['a'], -1]])

    x_matrix = np.array([[-1*ray_1.func['b'], -1], [-1*ray_2.func['b'], -1]])

    y_matrix = np.array([[ray_1.func['a'], -1*ray_1.func['b']], [ray_2.func['a'], -1*ray_2.func['b']]])

    print(main_matrix)
    print(x_matrix)
    print(y_matrix)

    x = np.linalg.det(x_matrix)/np.linalg.det(main_matrix)
    y = np.linalg.det(y_matrix)/np.linalg.det(main_matrix)

    try:
        shared_x = int(x)+415
    except OverflowError:
        shared_x = float('inf')
    except ValueError:          # THAT MEANS A POINT ON AXIS
        ...

    try:
        shared_y = int(y)+200
    except OverflowError:
        shared_y = float('inf')

    print(f"MUTUAL COORDS: x = {shared_x}, y = {shared_y}")

    return (x+lens.lens_xpos[1], y+200)

    
class NumericObject(Object):

    #   DODAJ KONWERSJE DLA KAZDEGO ELEMENTU PRZEZ LICZBE SOCZEWEK

    def __init__(self, x, y, sketch, object_type, item_of, image_of) -> None:
        super().__init__(x, y)
        print(sketch)
        self.y = sketch.axis.y1
        self.sketch = sketch
        self.image_of = image_of
        self.item_of = item_of
        self.postfix = ""
        self.object_type = object_type
        self.type_per_lens = {}
        self.parameters_per_lens = {}
        self.real_object = None
        self.in_real_plane = False
        self.already_converted_by = []
        self.bound_objects = []
        self.previous = None
        self.next = None
        self.converted_by = None

        if item_of != None:
            self.already_converted_by.extend(item_of.already_converted_by)
            self.bound_objects.extend(item_of.bound_objects)
            #self.bound_objects.append(item_of)
            item_of.bound_objects.append(self)
            self.item_of = item_of
            self.previous = item_of
            self.item_of.next = self
        if image_of != None:
            self.already_converted_by.extend(image_of.already_converted_by)
            self.bound_objects.extend(image_of.bound_objects)
            self.bound_objects.append(image_of)
            image_of.bound_objects.append(self)
            self.image_of = image_of
            self.previous = image_of
            self.image_of.next = self
        
        if object_type == "user_defined":
            self.real_object = self

        print(len(sketch.lenses))
        if len(sketch.lenses) > 0:
            if isinstance(self, NumericLensObject2):
                #active_lenses = self.get_active_lenses(sketch)
                unbound_lenses = self.get_unbound_lenses(sketch)
                self.define_type_per_lenses(unbound_lenses)
                self.define_parameters_per_lenses(unbound_lenses)
                self.check_real_plane_presence(unbound_lenses)
            else:
                self.define_type_per_lenses(sketch.lenses)
                self.define_parameters_per_lenses(sketch.lenses)
                self.check_real_plane_presence(sketch.lenses)


    def print_active_lenses_numbers(self, lenses):
        numbers = ""
        for lens in lenses:
            numbers += str(lens.number)
            numbers += ", "
        
        print(numbers)


    def get_active_lenses(self, sketch):
        lenses = sketch.lenses.copy()
        
        print(f"START: {lenses}")
        self.print_active_lenses_numbers(lenses)

        for lens in self.already_converted_by:
            if lens in lenses:
                lenses.remove(lens)
        print(f"AFTER REMOVING ALREADY USED LENSES: {lenses}")
        self.print_active_lenses_numbers(lenses)

        if isinstance(self, NumericLensObject2):
            if self in lenses:
                    lenses.remove(self)
            print(f"AFTER REMOVING ITSELF: {lenses}")
            self.print_active_lenses_numbers(lenses)

            for lens in self.bound_objects:
                if lens in lenses:
                    lenses.remove(lens)
            print(f"AFTER REMOVING ITS BOUND ITEMS: {lenses}")
            self.print_active_lenses_numbers(lenses)
        

        return lenses


    def get_unbound_lenses(self, sketch):
        lenses = sketch.lenses.copy()
        print(f"POCZATEK: {lenses}")
        self.print_active_lenses_numbers(lenses)
        
        if isinstance(self, NumericLensObject2):
            for lens in self.bound_objects:
                if lens in lenses:
                    lenses.remove(lens)
            print(f"PO WYJEBANIU SWOICH: {lenses}")
            self.print_active_lenses_numbers(lenses)
        

        return lenses

    

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


    def define_parameters_per_lens(self, lens):
        values = {}

        if self.type_per_lens[lens] == "item":
            optical_x = self.x - (lens.x - lens.focal)
            optical_s = self.x - lens.x
            optical_x_prime = alg.NumericCalc.newton_algorithm_x_prime(lens.focal, optical_x)
            optical_s_prime = alg.NumericCalc.carthesian_algorithm_s_prime(lens.focal, optical_s)
            zoom = alg.NumericCalc.carthesian_zoom(optical_s, optical_s_prime)
            print(f"x: {optical_x}, s: {optical_s}, x': {optical_x_prime}, s': {optical_s_prime}, Beta: {zoom} = {alg.NumericCalc.newton_zoom(optical_x_prime, lens.focal)}")
            
            values.update({"x" : optical_x})
            values.update({"s" : optical_s})
            values.update({"x'" : optical_x_prime})
            values.update({"s'" : optical_s_prime})
            values.update({"zoom" : zoom})
            
        elif self.type_per_lens[lens] == "image":
            optical_x_prime = self.x - (lens.x + lens.focal)
            optical_s_prime = self.x - lens.x
            optical_x = alg.NumericCalc.newton_algorithm_x(lens.focal, optical_x_prime)
            optical_s = alg.NumericCalc.carthesian_algorithm_s(lens.focal, optical_s_prime)
            zoom = alg.NumericCalc.carthesian_zoom(optical_s, optical_s_prime)
            print(f"x': {optical_x_prime}, s': {optical_s_prime}, x: {optical_x}, s: {optical_s}, Beta: {zoom} = {alg.NumericCalc.newton_zoom(optical_x_prime, lens.focal)}")
            
            values.update({"x" : optical_x})
            values.update({"s" : optical_s})
            values.update({"x'" : optical_x_prime})
            values.update({"s'" : optical_s_prime})
            values.update({"zoom" : zoom})

        self.parameters_per_lens.update({lens : values})
    


    def redefine_parameters_per_lens(self, lens, value):
        values = {}

        if self.type_per_lens[lens] == "item":
            optical_s = value
            optical_x = self.x - (lens.x - lens.focal)
            optical_x_prime = alg.NumericCalc.newton_algorithm_x_prime(lens.focal, optical_x)
            optical_s_prime = alg.NumericCalc.carthesian_algorithm_s_prime(lens.focal, optical_s)
            zoom = alg.NumericCalc.carthesian_zoom(optical_s, optical_s_prime)
            print(f"x: {optical_x}, s: {optical_s}, x': {optical_x_prime}, s': {optical_s_prime}, Beta: {zoom} = {alg.NumericCalc.newton_zoom(optical_x_prime, lens.focal)}")
            
            values.update({"x" : optical_x})
            values.update({"s" : optical_s})
            values.update({"x'" : optical_x_prime})
            values.update({"s'" : optical_s_prime})
            values.update({"zoom" : zoom})
            
        elif self.type_per_lens[lens] == "image":
            optical_s_prime = value
            optical_x_prime = self.x - (lens.x + lens.focal)
            optical_x = alg.NumericCalc.newton_algorithm_x(lens.focal, optical_x_prime)
            optical_s = alg.NumericCalc.carthesian_algorithm_s(lens.focal, optical_s_prime)
            zoom = alg.NumericCalc.carthesian_zoom(optical_s, optical_s_prime)
            print(f"x': {optical_x_prime}, s': {optical_s_prime}, x: {optical_x}, s: {optical_s}, Beta: {zoom} = {alg.NumericCalc.newton_zoom(optical_x_prime, lens.focal)}")
            
            values.update({"x" : optical_x})
            values.update({"s" : optical_s})
            values.update({"x'" : optical_x_prime})
            values.update({"s'" : optical_s_prime})
            values.update({"zoom" : zoom})

        self.parameters_per_lens.update({lens : values})


    def redefine_parameters_per_lenses(self, lenses, value):
        for lens in lenses:
            self.redefine_parameters_per_lens(lens, value)

    
    def define_type_per_lens(self, lens):
        if self.x < lens.x:
            self.type_per_lens.update({lens : "item"})
        else:
            self.type_per_lens.update({lens : "image"})

    
    def define_type_per_lenses(self, lenses):
        for lens in lenses:
            self.define_type_per_lens(lens)


    def draw_distance_label(self, sketch, lens):
        if self.type_per_lens[lens] == "item":
            value = abs(self.parameters_per_lens[lens]["s"])
            
        elif self.type_per_lens[lens] == "image":
            value = abs(self.parameters_per_lens[lens]["s'"])
        
        label = NumericDistanceLabel(self, lens, self.y-50, value, sketch)
        
        return label
    







class NumericDistanceLabel():

    selected = None

    def __init__(self, object_1, object_2, y, value, sketch):
        self.object_1 = object_1
        self.object_2 = object_2
        self.y = y
        self.value = value
        self.distance = NumericDistance(object_1.x, object_2.x, y, sketch)
        self.text = NumericText(object_1.x, object_2.x, y, f"{ "%.1f" % value}", sketch)
        self.bind_select_option(sketch)

    def __del__(self):
        print("DELETED DISTANCE LABEL")

    def bind_select_option(self, sketch):
        self.distance.canvas.unbind("<Button-1>")
        self.distance.canvas.bind("<Button-1>", lambda event: self.select_label(sketch))

    def delete_label(self):
        self.distance.delete_distance()
        del self.distance
        self.text.delete_text()
        del self.text

    def select_label(self, sketch):
        NumericDistanceLabel.selected = self
        print(f"SELECTED {NumericDistanceLabel.selected}")
        sketch.canv.unbind("<ButtonRelease-1>")
        sketch.canv.bind("<ButtonRelease-1>", lambda event: self.move_label(event, sketch))

    def move_label(self, event, sketch):
        self.distance.canvas.unbind("<ButtonRelease-1>")
        sketch.canv.unbind("<ButtonRelease-1>")
        print(f"MOVED {NumericDistanceLabel.selected} FROM {self.y} TO {event.y}")
        self.y = event.y
        NumericDistanceLabel.selected = None
        self.distance.place_canvas(self.object_1.x, self.object_2.x, self.y)
        self.text.place_canvas(self.object_1.x, self.object_2.x, self.y)
        print(f"SELECTED {NumericDistanceLabel.selected}")


class NumericDistance():

    def __init__(self, x1, x2, y, sketch):
        self.sketch = sketch
        self.canvas = tk.Canvas(master=sketch.canv, width=abs(x1-x2)-3, height=3, background="white", highlightthickness=0)
        self.line_2 = self.draw_line(x1, x2)
        self.place_canvas(x1, x2, y)


    def __del__(self):
        ...


    def draw_line(self, x1, x2):
        if x1 <= x2:
            return self.canvas.create_line(0, 1, abs(x2-x1), 1, fill="dark green", width=1)
        else:
            return self.canvas.create_line(0, 1, abs(x2-x1), 1, fill="dark green", width=1)
        
    def place_canvas(self, x1, x2, y):
        if x1 <= x2:
            self.canvas.place(x=x1+2, y=y)
        else:
            self.canvas.place(x=x2+2, y=y)


    def delete_distance(self):
        self.canvas.destroy()


class NumericText():

    def __init__(self, x1, x2, y, text, sketch, bd=0):
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.text = text
        self.sketch = sketch
        self.canvas = tk.Canvas(master=sketch.canv, width=self.determine_width(text), height=12, background="white", highlightthickness=bd, highlightbackground="black")
        self.text_id = self.draw_text()
        self.place_canvas(x1, x2, y)

    def __del__(self):
        ...

    def draw_text(self):
        return self.canvas.create_text(self.determine_width(self.text)/2, 6, text=self.text, fill="black", font=('Helvetica 8'), anchor=tk.CENTER)
    
    def determine_width(self, text):
        return 7*len(str(text))

    def place_canvas(self, x1, x2, y):
        self.canvas.place(x=(x2+x1)/2-self.determine_width(self.text)/2, y=y-5)
        self.y = y

    def delete_text(self):
        self.canvas.destroy()

    def update_text(self):
        self.canvas.delete(self.text_id)
        self.text_id = self.draw_text()
    

class NumericLine():

    def __init__(self, x, y, sketch, bd=0):
        self.x = x
        self.y1 = y
        self.y2 = sketch.axis.y1
        self.sketch = sketch
        self.height = self.determine_line_height()
        self.line_id = sketch.canv.create_line(self.x, self.y1, self.x, self.y2, width=1, fill="light grey")
        
    def determine_line_height(self):
        return abs(self.y1 - self.y2)

    def place_line(self, sketch):
        return sketch.canv.create_line(x1=self.x, y1=self.y1, x2=self.x, y2=self.y2, width=1, fill="light grey")


class NumericLensLabel():

    def __init__(self, lens: NumericLens):
        ...



class NumericPoint(NumericObject):

    selected = None


    def __init__(self, x, y, sketch, color="black", object_type = "user_defined", item_of = None, image_of = None) -> None:
        super().__init__(x, y, sketch, object_type, item_of, image_of)
        #self.y = sketch.axis.y1 - 5
        self.color = color
        self.number = len(sketch.points)+1
        self.id = self.draw(sketch)

        self.object_label = NumericPointLabel(self, sketch, self.type_per_lens[sketch.lens])
        self.distance_label = self.draw_distance_label(sketch, sketch.lens)
        self.bind_select_point(sketch)

        if self.object_type == "user_defined":
            self.distance_label.text.canvas.tag_bind(self.distance_label.text.text_id, "<Button-1>",
                                               lambda event: self.set_distance_value(sketch, sketch.lens))
            self.convert_per_lens(sketch)
            print("USER DEFINED POINT")


    def __del__(self):
        ...


    def bind_delete_point(self, sketch):
        sketch.canv.tag_unbind(self.id, "<Button-1>")
        sketch.canv.tag_bind(self.id, "<Button-1>", lambda event: self.delete_point_manually(sketch))
     

    def bind_select_point(self, sketch):
        sketch.canv.tag_unbind(self.id, "<Button-1>")
        sketch.canv.tag_bind(self.id, "<Button-1>", lambda event: self.select_point(sketch))

    
    def convert(self, sketch, lens):
        if self.x < lens.x:
            self.item_of = self.determine_image(sketch, lens)
            self.item_of.number = self.number
            self.item_of.image_of = self
            self.item_of.real_object = self
            self.item_of.postfix = alg.NumericCalc.determine_object_postfix(self.item_of)
            self.item_of.object_label.update_label_text()
            self.postfix = alg.NumericCalc.determine_object_postfix(self)
            self.object_label.update_label_text()
        else:
            self.image_of = self.determine_item(sketch, lens)
            self.image_of.number = self.number
            self.image_of.item_of = self
            self.image_of.real_object = self
            self.image_of.postfix = alg.NumericCalc.determine_object_postfix(self.image_of)
            self.image_of.object_label.update_label_text()
            self.postfix = alg.NumericCalc.determine_object_postfix(self)
            self.object_label.update_label_text()
            #self.postfix += "'"


    def convert_per_lens(self, sketch):
        for lens in sketch.lenses:
            print(lens)
            self.convert(sketch, lens)

    

    def determine_image(self, sketch, lens):
        determined_x = self.parameters_per_lens[lens]["s'"] + lens.x
        determined_y = sketch.axis.y1 + (self.y - sketch.axis.y1)*self.parameters_per_lens[lens]["zoom"]
        #determined_diameter = self.diameter * abs(self.parameters_per_lens[lens]["zoom"])
        return NumericPoint(determined_x, determined_y, sketch, self.color, object_type="resulting")
        


    def determine_item(self, sketch, lens):
        determined_x = self.parameters_per_lens[lens]["s"] + lens.x
        determined_y = sketch.axis.y1 + (self.y - sketch.axis.y1)/self.parameters_per_lens[lens]["zoom"]
        #determined_diameter = self.diameter * abs(self.parameters_per_lens[lens]["zoom"])
        return NumericPoint(determined_x, determined_y, sketch, self.color, object_type="resulting")
        


    def select_point(self, sketch):
        print(f"SELECTED {self}")
        if NumericPoint.selected != None:
            NumericPoint.selected.bind_select_point(sketch)
        NumericPoint.selected = self
        self.bind_delete_point(sketch)

    def delete_point(self, sketch):
        print("DELETING")
        sketch.canv.delete(self.id)

        self.distance_label.delete_label()
        del self.distance_label
        self.object_label.delete_label()


    def delete_point_manually(self, sketch):
        NumericPoint.selected = None
        #self.delete_bonded_points(sketch)
        self.delete_bonded_points(sketch)
        self.delete_point(sketch)
        sketch.points.remove(self.real_object)
        NumericPoint.erase_point(self)


    def delete_bonded_points(self, sketch):
        if self.item_of != None:
            self.item_of.delete_point(sketch)
            NumericPoint.erase_point(self.item_of)
            self.item_of = None
        if self.image_of != None:
            self.image_of.delete_point(sketch)
            NumericPoint.erase_point(self.image_of)
            self.image_of = None


    def draw(self, sketch):
        return sketch.canv.create_line(self.x, self.y - 3, self.x, self.y + 3, fill=self.color, width=3)


    def change_distance(self, sketch, value=150):
        self.delete_point(sketch)
        self.delete_bonded_points(sketch)
        self.x = sketch.lens.x + value
        self.define_type_per_lens(sketch.lens)
        self.id = self.redraw(sketch)
        #self.object_label = NumericApertureLabel(self, sketch, self.type_per_lens[sketch.lens])
        #self.define_conversion_type(sketch)
        self.redefine_parameters_per_lens(sketch.lens, value)
        self.distance_label = self.draw_distance_label(sketch, sketch.lens)
        self.bind_select_point(sketch)
        if self.object_type == "user_defined":
            self.distance_label.text.canvas.tag_bind(self.distance_label.text.text_id, "<Button-1>",
                                               lambda event: self.set_distance_value(sketch, sketch.lens))

        #print(f"{self.conversion_type["to_image"]}, {self.conversion_type["to_item"]}")
        print(f"{self.type_per_lens[sketch.lens]}") 

    
    def redraw(self, sketch):
        return self.draw(sketch)#sketch.canv.create_line(self.x, sketch.axis.y1, self.x, self.y, fill=self.color, width=3)
    
    def set_distance_value(self, sketch, lens):
        print("SETTING DISTANCE VALUE")
        frame = tk.Frame(master = sketch.master,width=100)
        #label = tk.Label(master=frame, width=5, text="s=...")
        #label.pack()
        entry = tk.Entry(master=frame, width=5,  bd=3)
        entry.pack()
        if self.x > lens.x:
            entry.insert(0, f"{self.parameters_per_lens[lens]["s'"]}")
        else:
            entry.insert(0, f"{self.parameters_per_lens[lens]["s"]}")
        window = sketch.canv.create_window((self.x+sketch.lens.x)/2, self.distance_label.y, window=frame)
        entry.bind("<FocusIn>", lambda event: temp_text(event, entry))
        entry.bind("<Return>", lambda event: self.process_distance_entry_value(entry, sketch, window))

    
    def process_distance_entry_value(self, entry, sketch, window):
        try:
            value = float(entry.get())
            self.change_distance(sketch, value)
            sketch.canv.delete(window)
        except ValueError:
            sketch.canv.delete(window)


    @staticmethod
    def erase_point(point):
        print("ERASING POINT")
        del point




class NumericAperture(NumericObject):

    selected = None

    def __init__(self, x, y, sketch, diameter, object_type = "user_defined", item_of = None, image_of = None) -> None:
        super().__init__(x, y, sketch, object_type, item_of, image_of)
        self.diameter = diameter
        self.number = len(sketch.apertures)+1
        self.id = self.draw(sketch)
        self.object_label = NumericApertureLabel(self, sketch, self.type_per_lens[sketch.lens])
        self.distance_label = self.draw_distance_label(sketch, sketch.lens)

        """self.image = self.define_image(sketch)"""
        self.bind_select_aperture(sketch)

        if self.object_type == "user_defined" and sketch.lenses != 0:
            self.distance_label.text.canvas.tag_bind(self.distance_label.text.text_id, "<Button-1>",
                                               lambda event: self.set_distance_value(sketch, sketch.lens))
            self.convert_per_lens(sketch)
            

    def __del__(self):
        print("deleted aperture")


    def bind_delete_aperture(self, sketch):
        for item in self.id:
            sketch.canv.tag_unbind(item, "<Button-1>")
            sketch.canv.tag_bind(item, "<Button-1>", lambda event: self.delete_aperture_manually(sketch))


    def bind_select_aperture(self, sketch):
        for item in self.id:
            sketch.canv.tag_unbind(item, "<Button-1>")
            sketch.canv.tag_bind(item, "<Button-1>", lambda event: self.select_aperture(sketch))


    def convert(self, sketch, lens):
        if self.x < lens.x:
            self.item_of = self.determine_image(sketch, lens)
            self.item_of.image_of = self
            self.item_of.real_object = self
            self.item_of.postfix = alg.NumericCalc.determine_object_postfix(self.item_of)
            self.item_of.number = self.number
            self.item_of.object_label.update_label_text()
            self.postfix = alg.NumericCalc.determine_object_postfix(self)
            self.object_label.update_label_text()

        else:
            self.image_of = self.determine_item(sketch, lens)
            self.image_of.item_of = self
            self.image_of.real_object = self
            self.image_of.postfix = alg.NumericCalc.determine_object_postfix(self.image_of)
            self.image_of.number = self.number
            self.image_of.object_label.update_label_text()
            self.postfix = alg.NumericCalc.determine_object_postfix(self)
            self.object_label.update_label_text()
            #self.postfix += "'"


    def convert_per_lens(self, sketch):
        for lens in sketch.lenses:
            print(lens)
            self.convert(sketch, lens)

    

    def determine_image(self, sketch, lens):
        determined_x = self.parameters_per_lens[lens]["s'"] + lens.x
        determined_y = self.y
        determined_diameter = self.diameter * abs(self.parameters_per_lens[lens]["zoom"])
        return NumericAperture(determined_x, determined_y, sketch, determined_diameter, object_type="resulting")


    def determine_item(self, sketch, lens):
        determined_x = self.parameters_per_lens[lens]["s"] + lens.x
        determined_y = self.y
        determined_diameter = self.diameter / abs(self.parameters_per_lens[lens]["zoom"])
        return NumericAperture(determined_x, determined_y, sketch, determined_diameter, object_type="resulting")


    def draw_resulting_aperture(self, sketch):
        line_width = 3

        center = sketch.axis.y1
        upper_end = center - self.diameter/2
        lower_end = center + self.diameter/2
        id = []
        id.append(sketch.canv.create_line(self.x - 3, upper_end, self.x + 4, upper_end, fill=self.color, width=line_width))
        id.append(sketch.canv.create_line(self.x - 3, lower_end, self.x + 4, lower_end, fill=self.color, width=line_width))
        
        #   MAKING CEASED LINE
        lines_space = 40

        starting_value = upper_end
        while starting_value > 0:
            id.append(sketch.canv.create_line(self.x, starting_value, self.x, starting_value - lines_space, fill=self.color, width=line_width))
            starting_value = starting_value - 1.5*lines_space
        
        starting_value = lower_end
        while starting_value < 800:
            id.append(sketch.canv.create_line(self.x, starting_value, self.x, starting_value + lines_space, fill=self.color, width=line_width))
            starting_value = starting_value + 1.5*lines_space

        return id



    def draw(self, sketch):

        if self.object_type == "resulting":
            return self.draw_resulting_aperture(sketch)
        else:
            line_width = 3

            center = sketch.axis.y1
            upper_end = center - self.diameter/2
            lower_end = center + self.diameter/2
            id = []
            id.append(sketch.canv.create_line(self.x - 3, upper_end, self.x + 4, upper_end, fill=self.color, width=line_width))
            id.append(sketch.canv.create_line(self.x - 3, lower_end, self.x + 4, lower_end, fill=self.color, width=line_width))
            id.append(sketch.canv.create_line(self.x, upper_end, self.x, 0, fill=self.color, width=line_width))
            id.append(sketch.canv.create_line(self.x, lower_end, self.x, 400, fill=self.color, width=line_width))
            return id

    def set_distance_value(self, sketch, lens):
        print("SETTING DISTANCE VALUE")
        frame = tk.Frame(master = sketch.master,width=100)
        #label = tk.Label(master=frame, width=5, text="s=...")
        #label.pack()
        entry = tk.Entry(master=frame, width=5,  bd=3)
        entry.pack()
        if self.x > lens.x:
            entry.insert(0, f"{self.parameters_per_lens[lens]["s'"]}")
        else:
            entry.insert(0, f"{self.parameters_per_lens[lens]["s"]}")
        window = sketch.canv.create_window((self.x+sketch.lens.x)/2, self.distance_label.y, window=frame)
        entry.bind("<FocusIn>", lambda event: temp_text(event, entry))
        entry.bind("<Return>", lambda event: self.process_distance_entry_value(entry, sketch, window))

    
    def process_distance_entry_value(self, entry, sketch, window):
        try:
            value = float(entry.get())
            self.change_distance(sketch, value)
            sketch.canv.delete(window)
        except ValueError:
            sketch.canv.delete(window)

        


    def change_distance(self, sketch, value=150):
        self.delete_aperture(sketch)
        self.delete_bonded_apertures(sketch)
        self.x = sketch.lens.x + value
        self.define_type_per_lens(sketch.lens)
        self.id = self.redraw(sketch)
        self.object_label = NumericApertureLabel(self, sketch, self.type_per_lens[sketch.lens])
        #self.define_conversion_type(sketch)
        self.redefine_parameters_per_lens(sketch.lens, value)
        self.convert_per_lens(sketch)
        """self.distance = self.redefine_distance(sketch, value)
        self.distance_id = self.draw_distance(sketch)
        self.image = self.redefine_image(sketch)"""
        self.distance_label = self.draw_distance_label(sketch, sketch.lens)
        self.bind_select_aperture(sketch)
        if self.object_type == "user_defined":
            self.distance_label.text.canvas.tag_bind(self.distance_label.text.text_id, "<Button-1>",
                                               lambda event: self.set_distance_value(sketch, sketch.lens))

        #print(f"{self.conversion_type["to_image"]}, {self.conversion_type["to_item"]}")
        print(f"{self.type_per_lens[sketch.lens]}")        


    def delete_bonded_apertures(self, sketch):
        if self.item_of != None:
            self.item_of.delete_aperture(sketch)
            NumericAperture.erase_aperture(self.item_of)
            self.item_of = None
        if self.image_of != None:
            self.image_of.delete_aperture(sketch)
            NumericAperture.erase_aperture(self.image_of)
            self.image_of = None


    def delete_aperture(self, sketch):

        for x in range(0, len(self.id)):
            sketch.canv.delete(self.id[x])

        self.distance_label.delete_label()
        del self.distance_label
        self.object_label.delete_label()


    def delete_aperture_manually(self, sketch):
        NumericAperture.selected = None
        self.delete_bonded_apertures(sketch)
        self.delete_aperture(sketch)
        NumericAperture.erase_aperture(self)
        


    def redraw(self, sketch):
        return self.draw(sketch)


    def select_aperture(self, sketch):
        print(f"SELECTED {self}")
        if NumericAperture.selected != None:
            NumericAperture.selected.bind_select_aperture(sketch)
        NumericAperture.selected = self
        self.bind_delete_aperture(sketch)


    @staticmethod
    def erase_aperture(aperture):
        del aperture


class NumericPointLabel():

    def __init__(self, point: NumericPoint, sketch, type="image"):
        self.point = point
        self.sketch = sketch
        self.type = type
        self.y = self.define_number_y_position()
        self.number_label = self.define_point_number_label()
        #self.diameter_label = self.define_aperture_diameter_label(point, sketch)
        #self.value = NumericText(x1, x2, y, f"{value}", sketch)

    def __del__(self):
        print("DELETED APERTURE LABEL")


    def define_number_y_position(self):
        return self.point.y - 15
    
    
    def define_point_number_label(self):
        point = self.point
        sketch = self.sketch
        #if self.type == "image":
            #return NumericText(point.x, point.x, self.y, f"P{len(sketch.points)}'", sketch, bd=1)
        #if self.type == "item":
            #return NumericText(point.x, point.x, self.y, f"P{len(sketch.points)}", sketch, bd=1)
        return NumericText(point.x, point.x, self.y, f"P{point.number}{point.postfix}", sketch, bd=1)


    #def define_aperture_diameter_label(self, aperture, sketch):
        #return NumericText(aperture.x-1, aperture.x+2, self.number_label.y-15, f"Ø: {aperture.diameter}'", sketch, bd=1)


    def delete_label(self):
        self.number_label.delete_text()
        #self.diameter_label.delete_text()
        del self


    def update_label_text(self):
        self.number_label.delete_text()
        self.number_label = self.define_point_number_label()
    


class NumericApertureLabel():

    def __init__(self, aperture: NumericAperture, sketch, type="image"):
        self.aperture = aperture
        self.sketch = sketch
        self.type = type
        self.y = self.define_number_y_position()
        self.number_label = self.define_aperture_number_label()
        self.diameter_label = self.define_aperture_diameter_label()
        #self.value = NumericText(x1, x2, y, f"{value}", sketch)

    def __del__(self):
        print("DELETED APERTURE LABEL")


    def define_number_y_position(self):
        return self.sketch.axis.y1 - self.aperture.diameter/2 - 15
    
    
    def define_aperture_number_label(self):
        aperture = self.aperture
        sketch = self.sketch
        #if self.type == "image":
            #return NumericText(aperture.x, aperture.x, self.y, f"{len(sketch.apertures)+1}'", sketch, bd=1)
        #if self.type == "item":
            #return NumericText(aperture.x, aperture.x, self.y, f"{len(sketch.apertures)+1}", sketch, bd=1)
        return NumericText(aperture.x, aperture.x, self.y, f"{aperture.number}{aperture.postfix}", sketch, bd=1)

    def define_aperture_diameter_label(self):
        aperture = self.aperture
        sketch = self.sketch
        return NumericText(aperture.x-1, aperture.x+2, self.number_label.y-15, f"Ø: {aperture.diameter}'", sketch, bd=1)


    def delete_label(self):
        self.number_label.delete_text()
        self.diameter_label.delete_text()
        del self

    def update_label_text(self):
        self.number_label.delete_text()
        self.number_label = self.define_aperture_number_label()


class NumericRay:

    def __init__(self, sketch, object_1, object_2):
        self.sketch = sketch
        self.object_1 = object_1
        self.object_2 = object_2
        


class NumericApertureRay(NumericRay):

    def __init__(self, sketch, point, aperture):
        super().__init__(sketch, point, aperture)
        self.id = self.draw_aperture_ray(sketch, point, aperture)

    def draw_aperture_ray(self, sketch, point, aperture):
        x1 = point.x
        y1 = point.y
        x2 = aperture.x
        y2 = aperture.y - aperture.diameter/2
        return sketch.canv.create_line(x1, y1, x2, y2, fill="red", width=2)


    def determine_main_aperture(self, sketch):
        ...


class NumericFieldRay(NumericRay):

    def __init__(self, sketch, aperture_1, aperture_2):
        super().__init__(sketch, aperture_1, aperture_2)
        self.id = self.draw_field_ray(sketch, aperture_1, aperture_2)


    def draw_field_ray(self, sketch, aperture_1, aperture_2):
        x1 = aperture_1.x
        y1 = aperture_1.y
        x2 = aperture_2.x
        y2 = aperture_2.y - aperture_2.diameter/2
        return sketch.canv.create_line(x1, y1, x2, y2, fill="blue", width=2)
    


class NumericLensObject2(NumericObject):

    selected = None

    def __init__(self, x, y, sketch, diameter, focal, object_type = "user_defined", item_of = None, image_of = None) -> None:
        super().__init__(x, y, sketch, object_type, item_of, image_of)
        self.diameter = diameter
        self.focal = focal
        
        """self.already_converted_by = []
        self.bound_lenses = []
        if item_of != None:
            self.already_converted_by.extend(item_of.already_converted_by)
            self.bound_lenses.extend(item_of.bound_lenses)
            self.bound_lenses.append(item_of)
            item_of.bound_lenses.append(self)
            self.item_of = item_of
        if image_of != None:
            self.already_converted_by.extend(image_of.already_converted_by)
            self.bound_lenses.extend(image_of.bound_lenses)
            self.bound_lenses.append(image_of)
            image_of.bound_lenses.append(self)
            self.image_of = image_of"""

        self.number = len(sketch.apertures)+1
        self.id = self.draw_lens(sketch)
        self.focus_id = self.draw_focus(sketch)
        self.bind_select_lens(sketch)

        if len(sketch.lenses) == 0:
            self.object_label = NumericLensLabel(self, sketch, "none")
        else:
            self.object_label = NumericLensLabel(self, sketch, self.type_per_lens[sketch.lens])
            self.distance_label = self.draw_distance_label(sketch, sketch.lens)
            if self.object_type == "user_defined":
                self.distance_label.text.canvas.tag_bind(self.distance_label.text.text_id, "<Button-1>",
                                               lambda event: self.set_distance_value(sketch, sketch.lens))
                if len(sketch.lenses) > 0:
                    self.convert_per_lens(sketch)

        

        print(f"LENSY: {len(sketch.lenses)}")

        
        
        
            

    def __del__(self):
        print("deleted aperture")


    def bind_delete_lens(self, sketch):
        for item in self.id:
            sketch.canv.tag_unbind(item, "<Button-1>")
            sketch.canv.tag_bind(item, "<Button-1>", lambda event: self.delete_lens_manually(sketch))


    def bind_select_lens(self, sketch):
        for item in self.id:
            sketch.canv.tag_unbind(item, "<Button-1>")
            sketch.canv.tag_bind(item, "<Button-1>", lambda event: self.select_lens(sketch))


    def convert(self, sketch, lens):
        self.already_converted_by.append(lens)
        if self.x < lens.x:
            self.item_of = self.determine_image(sketch, lens, self)
            #self.item_of.already_converted_by.extend(self.already_converted_by)
            #self.item_of.image_of = self
            self.item_of.real_object = self.real_object
            self.item_of.postfix = alg.NumericCalc.determine_object_postfix(self.item_of)
            self.item_of.number = self.number
            self.item_of.object_label.update_label_text()
            self.postfix = alg.NumericCalc.determine_object_postfix(self)
            self.object_label.update_label_text()
            self.item_of.already_converted_by.append(lens)

        else:
            self.image_of = self.determine_item(sketch, lens, self)
            #self.image_of.already_converted_by.extend(self.already_converted_by)
            #self.image_of.item_of = self
            self.image_of.real_object = self.real_object
            self.image_of.postfix = alg.NumericCalc.determine_object_postfix(self.image_of)
            self.image_of.number = self.number
            self.image_of.object_label.update_label_text()
            self.postfix = alg.NumericCalc.determine_object_postfix(self)
            self.object_label.update_label_text()
            self.image_of.already_converted_by.append(lens)


    def convert_per_lens(self, sketch):
        active_lenses = self.get_active_lenses(sketch)
        
        print(active_lenses)

        for lens in active_lenses:
            print(lens)
            self.convert(sketch, lens)

    

    def determine_image(self, sketch, lens, item):
        determined_x = self.parameters_per_lens[lens]["s'"] + lens.x
        determined_y = self.y
        determined_diameter = self.diameter * abs(self.parameters_per_lens[lens]["zoom"])
        return NumericLensObject2(determined_x, determined_y, sketch, determined_diameter, self.focal, object_type="resulting", image_of=item)


    def determine_item(self, sketch, lens, image):
        determined_x = self.parameters_per_lens[lens]["s"] + lens.x
        #print(f"PRINTUJE IKSA: {determined_x}")
        determined_y = self.y
        determined_diameter = self.diameter / abs(self.parameters_per_lens[lens]["zoom"])
        return NumericLensObject2(determined_x, determined_y, sketch, determined_diameter, self.focal, object_type="resulting", item_of=image)


    



    def draw(self, sketch):

        if self.object_type == "resulting":
            return self.draw_resulting_lens(sketch)
        else:
            line_width = 3

            center = sketch.axis.y1
            upper_end = center - self.diameter/2
            lower_end = center + self.diameter/2
            id = []
            id.append(sketch.canv.create_line(self.x - 3, upper_end, self.x + 4, upper_end, fill=self.color, width=line_width))
            id.append(sketch.canv.create_line(self.x - 3, lower_end, self.x + 4, lower_end, fill=self.color, width=line_width))
            id.append(sketch.canv.create_line(self.x, upper_end, self.x, 0, fill=self.color, width=line_width))
            id.append(sketch.canv.create_line(self.x, lower_end, self.x, 400, fill=self.color, width=line_width))
            return id


    def draw_resulting_lens(self, sketch):
        line_width = 1
        self.color = "grey"

        center = sketch.axis.y1
        upper_end = center - self.diameter/2
        lower_end = center + self.diameter/2
        id = []
        id.append(sketch.canv.create_line(self.x - 3, upper_end, self.x + 4, upper_end, fill=self.color, width=line_width))
        id.append(sketch.canv.create_line(self.x - 3, lower_end, self.x + 4, lower_end, fill=self.color, width=line_width))
        
        #   MAKING CEASED LINE
        lines_space = 40

        starting_value = upper_end
        while starting_value > 0:
            id.append(sketch.canv.create_line(self.x, starting_value, self.x, starting_value - lines_space, fill=self.color, width=line_width))
            starting_value = starting_value - 1.5*lines_space
        
        starting_value = lower_end
        while starting_value < 800:
            id.append(sketch.canv.create_line(self.x, starting_value, self.x, starting_value + lines_space, fill=self.color, width=line_width))
            starting_value = starting_value + 1.5*lines_space

        return id


    def set_distance_value(self, sketch, lens):
        print("SETTING DISTANCE VALUE")
        frame = tk.Frame(master = sketch.master,width=100)
        #label = tk.Label(master=frame, width=5, text="s=...")
        #label.pack()
        entry = tk.Entry(master=frame, width=5,  bd=3)
        entry.pack()
        if self.x > lens.x:
            entry.insert(0, f"{self.parameters_per_lens[lens]["s'"]}")
        else:
            entry.insert(0, f"{self.parameters_per_lens[lens]["s"]}")
        window = sketch.canv.create_window((self.x+sketch.lens.x)/2, self.distance_label.y, window=frame)
        entry.bind("<FocusIn>", lambda event: temp_text(event, entry))
        entry.bind("<Return>", lambda event: self.process_distance_entry_value(entry, sketch, window))

    
    def process_distance_entry_value(self, entry, sketch, window):
        try:
            value = float(entry.get())
            self.change_distance(sketch, value)
            sketch.canv.delete(window)
        except ValueError:
            sketch.canv.delete(window)

        


    def change_distance(self, sketch, value=150):
        self.delete_lens(sketch)
        self.delete_bonded_lenses(sketch)
        self.already_converted_by.clear()
        #self.bound_lenses.clear()

        self.x = sketch.lens.x + value
        self.define_type_per_lens(sketch.lens)
        self.id = self.redraw(sketch)
        self.focus_id = self.draw_focus(sketch)
        self.object_label = NumericLensLabel(self, sketch, self.type_per_lens[sketch.lens])
        #self.define_conversion_type(sketch)
        self.redefine_parameters_per_lens(sketch.lens, value)
        
        self.convert_per_lens(sketch)
        #self.convert(sketch, sketch.lens)
        """self.distance = self.redefine_distance(sketch, value)
        self.distance_id = self.draw_distance(sketch)
        self.image = self.redefine_image(sketch)"""
        print(self.parameters_per_lens[sketch.lens])
        self.distance_label = self.draw_distance_label(sketch, sketch.lens)
        self.bind_select_lens(sketch)
        if self.object_type == "user_defined":
            self.distance_label.text.canvas.tag_bind(self.distance_label.text.text_id, "<Button-1>",
                                               lambda event: self.set_distance_value(sketch, sketch.lens))

        #print(f"{self.conversion_type["to_image"]}, {self.conversion_type["to_item"]}")
        print(f"{self.type_per_lens[sketch.lens]}")        


    def delete_bonded_lenses(self, sketch):

        if self.item_of != None:
            self.item_of.delete_lens(sketch)
            NumericLensObject2.erase_lens(self.item_of)
            self.item_of = None
        if self.image_of != None:
            self.image_of.delete_lens(sketch)
            NumericLensObject2.erase_lens(self.image_of)
            self.image_of = None


    def delete_lens(self, sketch):

        for x in range(0, len(self.id)):
            sketch.canv.delete(self.id[x])

        self.delete_focus(sketch)
        if self.item_of != None:
            self.item_of.image_of = None
        if self.image_of != None:
            self.image_of.item_of = None

        self.distance_label.delete_label()
        del self.distance_label
        self.object_label.delete_label()


    def delete_lens_manually(self, sketch):
        NumericLensObject2.selected = None
        self.delete_bonded_lenses(sketch)
        self.delete_lens(sketch)
        NumericLensObject2.erase_lens(self)
        


    def redraw(self, sketch):
        return self.draw_lens(sketch)


    def select_lens(self, sketch):
        print(f"SELECTED {self}")
        if NumericLensObject2.selected != None:
            NumericLensObject2.selected.bind_select_lens(sketch)
        NumericLensObject2.selected = self
        self.bind_delete_lens(sketch)




    def draw_lens(self, sketch):

        center = sketch.axis.y1
        main_line = sketch.canv.create_line(self.x, center-self.diameter/2, self.x, center+self.diameter/2, fill="black", width=3)
        edges = self.draw_lens_edges(center-self.diameter/2, center+self.diameter/2, sketch)

        id = []
        id.append(main_line)
        id.extend(edges)
        return id
    
    def draw_lens_edges(self, upper_end, lower_end, sketch):
        edges = []
        if self.focal > 0:
            edges.append(sketch.canv.create_line(self.x, upper_end, self.x - 5, upper_end + 8, fill="black", width=3))
            edges.append(sketch.canv.create_line(self.x, upper_end, self.x + 5, upper_end + 8, fill="black", width=3))
            edges.append(sketch.canv.create_line(self.x, lower_end, self.x - 5, lower_end - 8, fill="black", width=3))
            edges.append(sketch.canv.create_line(self.x, lower_end, self.x + 5, lower_end - 8, fill="black", width=3))
        else:
            edges.append(sketch.canv.create_line(self.x, upper_end, self.x - 5, upper_end - 8, fill="black", width=3))
            edges.append(sketch.canv.create_line(self.x, upper_end, self.x + 5, upper_end - 8, fill="black", width=3))
            edges.append(sketch.canv.create_line(self.x, lower_end, self.x - 5, lower_end + 8, fill="black", width=3))
            edges.append(sketch.canv.create_line(self.x, lower_end, self.x + 5, lower_end + 8, fill="black", width=3))
        return edges


    def draw_focus(self, sketch):
        font = ('Helvetica 10 bold')
        self.focus_pos = [self.x-self.focal, self.x+self.focal]

        focus_img = ((sketch.canv.create_line(self.focus_pos[0], 195, self.focus_pos[0], 205, fill="red", width=3),
                    sketch.canv.create_text(self.focus_pos[0], 190, text="F", fill="red", font=font)),
                    (sketch.canv.create_line(self.focus_pos[1], 195, self.focus_pos[1], 205, fill="red", width=3),
                    sketch.canv.create_text(self.focus_pos[1], 190, text="F'", fill="red", font=font)))
        
        return focus_img
    
        
    def redraw_focus(self, sketch):
        return self.draw_focus(sketch)


    def delete_focus(self, sketch):
        for pair in self.focus_id:
            for item in pair:
                sketch.canv.delete(item)


    @staticmethod
    def erase_lens(lens):
        del lens


class NumericLensLabel():

    def __init__(self, lens: NumericLensObject2, sketch, type="image"):

        self.lens = lens
        self.sketch = sketch
        self.type = type
        self.y = self.define_number_y_position()
        self.number_label = self.define_aperture_number_label()
        self.diameter_label = self.define_aperture_diameter_label()
        self.focal_label = self.define_lens_focal_label()
        #self.value = NumericText(x1, x2, y, f"{value}", sketch)

    def __del__(self):
        print("DELETED LENS LABEL")

    def define_lens_focal_label(self):
        aperture = self.lens
        sketch = self.sketch
        return NumericText(aperture.x, aperture.x, self.y, f"f{aperture.number}' = {aperture.focal}", sketch, bd=1)


    def define_number_y_position(self):
        return self.sketch.axis.y1 - self.lens.diameter/2 - 15


    def define_aperture_number_label(self):
        aperture = self.lens
        sketch = self.sketch
        #if self.type == "None":
            #return NumericText(aperture.x, aperture.x, self.y, f"{len(sketch.apertures)+1}'", sketch, bd=1)
        #if self.type == "item":
            #return NumericText(aperture.x, aperture.x, self.y, f"{len(sketch.apertures)+1}", sketch, bd=1)
        return NumericText(aperture.x, aperture.x, self.y, f"{aperture.number}{aperture.postfix}", sketch, bd=1)

    def define_aperture_diameter_label(self):
        aperture = self.lens
        sketch = self.sketch
        return NumericText(aperture.x-1, aperture.x+2, self.number_label.y-15, f"Ø: {aperture.diameter}", sketch, bd=1)


    def delete_label(self):
        self.number_label.delete_text()
        self.diameter_label.delete_text()
        self.focal_label.delete_text()
        del self

    def update_label_text(self):
        self.number_label.delete_text()
        self.number_label = self.define_aperture_number_label()