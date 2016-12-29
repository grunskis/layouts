from .primitives import Container, Circle
from .layouts import HorizontalLineLayout, GridLayout, CircleLayout


# radius is a global b/c we can't add extra parameters to layout functions
radius = None


def horizontal_line_layout(container_width, container_height, number_of_items):
    container = Container(container_width, container_height)
    return arrange_items_in_layout(HorizontalLineLayout, container, number_of_items)


def grid_layout(container_width, container_height, number_of_items):
    container = Container(container_width, container_height)
    return arrange_items_in_layout(GridLayout, container, number_of_items)


def circle_layout(container_width, container_height, number_of_items):
    container = Container(container_width, container_height)
    return arrange_items_in_layout(CircleLayout, container, number_of_items)


def arrange_items_in_layout(layout_class, container, number_of_items):
    layout = layout_class(container)

    for x in range(0, number_of_items):
        item = Circle(radius=radius)
        layout.add(item)

    layout.save()

    return layout.as_tuples()
