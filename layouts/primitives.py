class Item(object):
    # size of square box to fit smallest possible circle
    MIN_SIDE_SIZE = 3

    def __init__(self, **kwargs):
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)

    def box_coordinates(self):
        """
        Returns coordinates for the containing box of the item in
        format (x0, y0, x1, y1).

        All subclasses must implement this method.
        """
        raise NotImplementedError()

    def intersects_with(self, item):
        """
        Return True if this item intersects with other item, otherwise
        False.
        """
        ax0, ay0, ax1, ay1 = self.box_coordinates()
        bx0, by0, bx1, by1 = item.box_coordinates()

        return ax0 <= bx1 and ax1 >= bx0 and ay0 <= by1 and ay1 >= by0


class Circle(Item):
    def __init__(self, radius=None, **kwargs):
        super(Circle, self).__init__(**kwargs)

        assert radius is not None and radius > 0, "radius has to be greater than 0"
        self.radius = radius

    def box_coordinates(self):
        """
        Returns coordinates for the containing box of the circle in
        format (x0, y0, x1, y1)
        """
        x0 = self.x - self.radius
        y0 = self.y - self.radius
        x1 = self.x + self.radius
        y1 = self.y + self.radius
        return (x0, y0, x1, y1)

    def as_tuple(self):
        return (self.x, self.y, self.radius, )

    def __repr__(self):
        return str(self.as_tuple())


class Container(object):
    def __init__(self, width=None, height=None):
        """
        All dimensions must be specified in pixels.
        """
        assert width is not None and width > 0, "width has to be greater than 0"
        assert height is not None and height > 0, "height has to be greater than 0"

        self.width = width
        self.height = height

    def capacity(self, size):
        """
        Returns number of items of size * size this container can
        contain without overlap.
        """
        sw = self.width - (self.width % size)
        sh = self.height - (self.height % size)
        return (sw * sh) / (size * size)

    def within_bounds(self, item):
        """
        Returns True if box containing item is within container
        bounds, otherwise False.
        """
        x0, y0, x1, y1 = item.box_coordinates()
        return x0 >= 0 and y0 >= 0 and x1 < self.width and y1 < self.height
