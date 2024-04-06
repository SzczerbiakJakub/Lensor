import sys
import pytest
import tkinter as tk
from unittest.mock import patch

sys.path.insert(0, 'C:/users/administrator/apka/lensor/src')

import gui


class MockEvent:
    def __init__(self, type, widget, x, y, char=None, keysym=None, delta=None):
        self.type = type
        self.widget = widget
        self.x = x
        self.y = y
        self.char = char
        self.keysym = keysym
        self.delta = delta




@pytest.fixture
def get_main_window():
    main_window = gui.MainWindow()
    return main_window

@pytest.fixture
def get_graphic_sketch(get_main_window):
    main_window = get_main_window
    main_window.create_graphic_project()
    graphic_sketch = main_window.sketch
    return graphic_sketch

@pytest.fixture
def get_numeric_sketch(get_main_window):
    main_window = get_main_window
    main_window.create_numeric_project()
    numeric_sketch = main_window.sketch
    return numeric_sketch


@pytest.fixture
def get_graphic_project(get_main_window):
    main_window = get_main_window
    main_window.create_graphic_project()
    graphic_sketch = main_window.sketch
    return main_window, graphic_sketch

@pytest.fixture
def get_numeric_project(get_main_window):
    main_window = get_main_window
    main_window.create_numeric_project()
    numeric_sketch = main_window.sketch
    return main_window, numeric_sketch

@pytest.fixture
def event():
    return "<ButtonRelease-3 state=Button3 num=3 x=91 y=69>"


def test_create_graphic_project(get_graphic_project):
    main_window, graphic_sketch = get_graphic_project
    assert graphic_sketch.master is main_window.root
    assert isinstance(graphic_sketch, gui.GraphicSketch)
    assert gui.GraphicSketch.over_point == False
    assert gui.GraphicSketch.deleting_point_mode == False
    assert gui.GraphicSketch.processed_point == None
    assert isinstance(gui.GraphicSketch.shape_initial_points, list)
    assert len(gui.GraphicSketch.shape_initial_points) == 0
    assert isinstance(gui.GraphicSketch.points_coords, list)
    assert len(gui.GraphicSketch.points_coords) == 0
    assert isinstance(graphic_sketch.points, list)
    assert len(graphic_sketch.points) == 0
    assert isinstance(graphic_sketch.resulting_points, dict)
    assert len(graphic_sketch.resulting_points) == 0
    assert isinstance(graphic_sketch.shapes, list)
    assert len(graphic_sketch.shapes) == 0
    assert graphic_sketch.building_shape == False


def test_create_numeric_project(get_numeric_project):
    main_window, numeric_sketch = get_numeric_project
    assert numeric_sketch.master is main_window.root
    assert isinstance(numeric_sketch, gui.NumericSketch)



def test_destroy_starting_buttons(get_main_window):
    main_window = get_main_window
    assert main_window.new_graphic_button != None
    assert main_window.new_numeric_button != None
    assert main_window.open_graphic_button != None
    assert main_window.open_numeric_button != None



#   TEST OF SKETCH CLASS

def test_create_sketch_axis(get_graphic_sketch, get_numeric_sketch):
    graphic_sketch = get_graphic_sketch
    numeric_sketch = get_numeric_sketch
    assert graphic_sketch.axis is not None
    assert graphic_sketch.axis.y1 == 200
    assert numeric_sketch.axis is not None
    assert numeric_sketch.axis.y1 == 200




#   TESTS OF GRAPHIC SKETCH CLASS


def test_create_graphic_sketch(get_graphic_project):
    main_window, graphic_sketch = get_graphic_project
    assert main_window.sketch.master is main_window.root
    assert int(graphic_sketch.canv.cget("width")) == 800
    assert int(graphic_sketch.canv.cget("height")) == 400

    

def test_create_graphic_sketch_lens(get_graphic_sketch):
     graphic_sketch = get_graphic_sketch
     assert graphic_sketch.lens.focal == 100
     assert graphic_sketch.lens.pos == 400
     assert graphic_sketch.lens.space == 30


def test_new_point(get_graphic_sketch):
    graphic_sketch = get_graphic_sketch
    graphic_sketch.new_point(100, 200)
    assert len(graphic_sketch.points) == 1
    assert len(graphic_sketch.resulting_points) == 1
    graphic_sketch.new_point(100, 300)
    graphic_sketch.new_point(100, 400)
    assert len(graphic_sketch.points) == 3
    assert len(graphic_sketch.resulting_points) == 3



def test_check_point_presence(get_graphic_sketch):
    graphic_sketch = get_graphic_sketch
    graphic_sketch.new_point(100, 200)
    assert graphic_sketch.check_point_presence(100, 100) == False
    assert graphic_sketch.check_point_presence(100, 200) == True


def test_cursor_over_point(get_graphic_sketch):
    graphic_sketch = get_graphic_sketch
    point = graphic_sketch.new_point(100, 200)
    graphic_sketch.cursor_over_point(point)
    assert gui.GraphicSketch.processed_point == point


def test_cursor_left_point(get_graphic_sketch):
    graphic_sketch = get_graphic_sketch
    graphic_sketch.cursor_left_point()
    assert gui.GraphicSketch.processed_point == None


def test_build_shape(get_graphic_sketch):
    graphic_sketch = get_graphic_sketch
    graphic_sketch.build_shape()
    assert graphic_sketch.create_shape_button.cget("bg") == "red"
    assert graphic_sketch.building_shape == True


def test_clear_sketch(get_graphic_sketch):
    graphic_sketch = get_graphic_sketch
    graphic_sketch.clear_sketch()
    assert len(graphic_sketch.points) == 0
    assert len(graphic_sketch.resulting_points) == 0
    assert len(graphic_sketch.shapes) == 0


def test_delete_point(get_graphic_sketch):
    graphic_sketch = get_graphic_sketch
    point = graphic_sketch.new_point(100, 100)
    assert len(graphic_sketch.points) == 1
    assert len(graphic_sketch.resulting_points) == 1
    graphic_sketch.delete_point(point)
    assert len(graphic_sketch.points) == 0
    assert len(graphic_sketch.resulting_points) == 0


def test_hide_all_rays(get_graphic_sketch):
    graphic_sketch = get_graphic_sketch
    point_1 = graphic_sketch.new_point(100, 100)
    point_2 = graphic_sketch.new_point(100, 200)
    graphic_sketch.hide_all_rays()
    assert point_1.show_rays == False
    assert point_2.show_rays == False

def test_create_shape(get_graphic_sketch):
    graphic_sketch = get_graphic_sketch
    gui.GraphicSketch.create_shape(graphic_sketch)
    assert graphic_sketch.create_shape_button.cget("bg") == "white"
    assert graphic_sketch.building_shape is False


#   TESTS OF NUMERIC SKETCH CLASS


def test_create_numeric_sketch(get_numeric_project):
    main_window, numeric_sketch = get_numeric_project
    assert numeric_sketch.master is main_window.root
    assert int(numeric_sketch.canv.cget("width")) == 800
    assert int(numeric_sketch.canv.cget("height")) == 400
    assert numeric_sketch.lens is None
    assert isinstance(numeric_sketch.lenses, list)
    assert len(numeric_sketch.lenses) == 0
    assert isinstance(numeric_sketch.apertures, list)
    assert len(numeric_sketch.apertures) == 0
    assert isinstance(numeric_sketch.points, list)
    assert len(numeric_sketch.points) == 0



def test_numeric_create_lens(get_numeric_sketch):
    numeric_sketch = get_numeric_sketch
    function_output = numeric_sketch.create_lens()
    assert isinstance(function_output, gui.CreateLensWindow)
    assert function_output.x == 400
    assert function_output.y == 200
    assert function_output.master is numeric_sketch.master
    assert function_output.sketch is numeric_sketch


def test_numeric_create_lens2(get_numeric_sketch):
    numeric_sketch = get_numeric_sketch
    numeric_sketch.create_lens2()
    assert numeric_sketch.place_lens_button.cget("bg") == "red"

def test_numeric_create_point(get_numeric_sketch):
    numeric_sketch = get_numeric_sketch
    numeric_sketch.create_point()
    assert numeric_sketch.place_object_button.cget("bg") == "red"


"""def test_numeric_place_point(get_numeric_sketch):
    numeric_sketch = get_numeric_sketch
    former_sketch_points_length = len(numeric_sketch.points)
    event = MockEvent("ButtonRelease-1", None, 100, 100)
    numeric_sketch.place_point(event)
    assert numeric_sketch.place_object_button.cget("bg") == "white"
    assert len(numeric_sketch.points) == former_sketch_points_length + 1"""


"""def test_numeric_create_aperture(get_numeric_sketch):
    numeric_sketch = get_numeric_sketch
    numeric_sketch.create_aperture()
    assert numeric_sketch.place_aperture_button.cget("bg") == "red"


    def move_distance_label(self, event):
        self.canv.unbind('<ButtonRelease-1>')
        self.canv.bind('<ButtonRelease-1>', self.place_aperture)



@patch <ButtonRelease event state=Button3 num=3 x=91 y=69>
def test_numeric_place_point(get_numeric_sketch):
    numeric_sketch = get_numeric_sketch
    former_sketch_points_length = len(numeric_sketch.points)
    numeric_sketch.place_aperture()
    assert numeric_sketch.place_object_button.cget("bg") == "white"
    assert len(numeric_sketch.points) == former_sketch_points_length + 1

    def place_aperture(self, event):
        self.place_aperture_button.config(background="white")
        self.canv.unbind('<ButtonRelease-1>')
        return CreateApertureWindow(event.x, event.y, self.master, self)


    def place_lens(self, event):
        self.place_lens_button.config(background="white")
        self.canv.unbind('<ButtonRelease-1>')
        return CreateLensWindow(event.x, event.y, self.master, self)


    def show_data(self):
        print(len(self.apertures))"""