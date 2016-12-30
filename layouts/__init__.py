from .primitives import Container, Circle
from .layouts import HorizontalLineLayout, GridLayout, CircleLayout, RandomLayout


# radius is a global b/c we can't add extra parameters to layout functions
radius = None


def horizontal_line_layout(container_width, container_height, number_of_items):
    container = Container(container_width, container_height)
    layout = HorizontalLineLayout(container)
    return arrange_items_in_layout(layout, number_of_items)


def grid_layout(container_width, container_height, number_of_items):
    container = Container(container_width, container_height)
    layout = GridLayout(container)
    return arrange_items_in_layout(layout, number_of_items)


def circle_layout(container_width, container_height, number_of_items):
    container = Container(container_width, container_height)
    layout = CircleLayout(container)
    return arrange_items_in_layout(layout, number_of_items)


def random_layout(container_width, container_height, number_of_items):
    container = Container(container_width, container_height)
    layout = RandomLayout(radius, container)
    return arrange_items_in_layout(layout, number_of_items)


def arrange_items_in_layout(layout, number_of_items):
    for x in range(0, number_of_items):
        item = Circle(radius=radius)
        layout.add(item)

    layout.save()

    return layout.as_tuples()
