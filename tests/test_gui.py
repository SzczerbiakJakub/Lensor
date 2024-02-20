import sys
import pytest

sys.path.insert(0, 'C:/users/administrator/apka/lensor/src')

import gui


#main_window = gui.MainWindow()

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


def test_create_numeric_sketch(get_numeric_project):
    main_window, numeric_sketch = get_numeric_project
    assert numeric_sketch.master is main_window.root
    assert int(numeric_sketch.canv.cget("width")) == 800
    assert int(numeric_sketch.canv.cget("height")) == 400


def test_create_graphic_sketch(get_graphic_project):
    main_window, graphic_sketch = get_graphic_project
    assert main_window.sketch.master is main_window.root
    assert int(graphic_sketch.canv.cget("width")) == 800
    assert int(graphic_sketch.canv.cget("height")) == 400


def test_create_graphic_sketch_axis(get_graphic_project):
    main_window, graphic_sketch = get_graphic_project
    assert graphic_sketch.axis is not None
    assert graphic_sketch.axis.y1 == 200
    """main_window.create_numeric_project()
    assert main_window.sketch.axis.y1 == 200"""

def test_create_numeric_sketch_axis(get_numeric_project):
    main_window, numeric_sketch = get_numeric_project
    assert numeric_sketch.axis is not None
    assert numeric_sketch.axis.y1 == 200

    

def test_create_graphic_sketch_lens(get_graphic_sketch):
     #main_window.create_graphic_project()
     #graphic_sketch = main_window.sketch
     graphic_sketch = get_graphic_sketch
     assert graphic_sketch.lens.focal == 100
     assert graphic_sketch.lens.pos == 400
     assert graphic_sketch.lens.space == 30


"""def test_create_graphic_sketch_lens(get_graphic_sketch):
     #main_window.create_graphic_project()
     #graphic_sketch = main_window.sketch
     assert graphic_sketch.lens.focal == 100
     assert graphic_sketch.lens.pos == 400
     assert graphic_sketch.lens.space == 30"""


def test_new_point(get_graphic_sketch):
    graphic_sketch = get_graphic_sketch
    graphic_sketch.new_point(100, 200)
    assert len(graphic_sketch.points) == 1
    assert len(graphic_sketch.resulting_points) == 1
    graphic_sketch.new_point(100, 300)
    graphic_sketch.new_point(100, 400)
    assert len(graphic_sketch.points) == 3
    assert len(graphic_sketch.resulting_points) == 3


"""
@pytest.mark.parametrize("graphic_sketch", [
    graphic_sketch
])
def test_check_point_presence(graphic_sketch):
    graphic_sketch.new_point(100, 200)
    assert graphic_sketch.check_point_presence(100, 100) == False
    assert graphic_sketch.check_point_presence(100, 200) == True


@pytest.mark.parametrize("graphic_sketch", [
    graphic_sketch
])
def test_cursor_over_point(graphic_sketch):
    point = graphic_sketch.new_point(100, 200)
    graphic_sketch.cursor_over_point(point)
    assert gui.GraphicSketch.processed_point == point


@pytest.mark.parametrize("graphic_sketch", [
    graphic_sketch
])
def test_cursor_left_point(graphic_sketch):
    graphic_sketch.cursor_left_point()
    assert gui.GraphicSketch.processed_point == None


@pytest.mark.parametrize("graphic_sketch", [
    graphic_sketch
])
def test_build_shape(graphic_sketch):
    graphic_sketch.build_shape()
    assert graphic_sketch.create_shape_button.cget("bg") == "red"
    assert graphic_sketch.building_shape == True


@pytest.mark.parametrize("graphic_sketch", [
    graphic_sketch
]
)
def test_clear_sketch(graphic_sketch):
    graphic_sketch.clear_sketch()
    assert len(graphic_sketch.points) == 0
    assert len(graphic_sketch.resulting_points) == 0
    assert len(graphic_sketch.shapes) == 0

@pytest.mark.parametrize("graphic_sketch", [
    graphic_sketch
]
)
def test_delete_point(graphic_sketch):
    point = graphic_sketch.new_point(100, 100)
    assert len(graphic_sketch.points) == 1
    assert len(graphic_sketch.resulting_points) == 1
    graphic_sketch.delete_point(point)
    assert len(graphic_sketch.points) == 0
    assert len(graphic_sketch.resulting_points) == 0

@pytest.mark.parametrize("graphic_sketch", [
    graphic_sketch
]
)
def test_hide_all_rays(graphic_sketch):
    point_1 = graphic_sketch.new_point(100, 100)
    point_2 = graphic_sketch.new_point(100, 200)
    graphic_sketch.hide_all_rays()
    assert point_1.show_rays == False
    assert point_2.show_rays == False"""