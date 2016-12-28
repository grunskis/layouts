from itertools import combinations

from PIL import Image, ImageDraw

from .primitives import Item
from .errors import LayoutError


class BaseLayout(object):
    def items_intersect(self):
        """
        Return True if any of the items intersect, otherwise False.
        """
        for a, b in combinations(self.items, 2):
            if a.intersects_with(b):
                return True

        return False

    def save(self):
        """
        Creates bitmap image of the layout and saves as a plot.bmp.
        """
        img = Image.new("1", (self.container.width, self.container.height))
        draw = ImageDraw.Draw(img)
        for item in self.items:
            draw.ellipse(item.box_coordinates(), fill=1)
        del draw
        img.save("plot.bmp", "bmp")

    def as_tuples(self):
        return [x.as_tuple() for x in self.items]


class HorizontalLineLayout(BaseLayout):
    """
    All items are aligned on a horizontal line, centered in the container.
    """
    def __init__(self, container):
        self.items = []
        self.container = container

    @property
    def baseline(self):
        """
        Return y coordinate of the horizontal baseline.
        """
        if getattr(self, "_baseline", None) is None:
            self._baseline = (self.container.height - 1) / 2
        return self._baseline

    def add(self, item):
        """
        Add a new item to the layout and re-arrange the layout.

        Raise an error if items are overlapping.
        """
        self.items.append(item)
        self._arrange()

        if self.items_intersect():
            raise LayoutError("overlapping items")

    def _arrange(self):
        """
        Arrange items in layout or raise error if it's not possible.
        """
        part_width = self.container.width / len(self.items)

        for i, item in enumerate(self.items):
            item.x = (i * part_width) + (part_width / 2)
            item.y = self.baseline

            # make sure item fits within the container bounds
            if not self.container.within_bounds(item):
                raise LayoutError("item doesn't fit in the container")


class GridLayout(BaseLayout):
    """
    All items are organized in a grid, all aligned vertically and horizontally.
    """
    def __init__(self, container):
        self.container = container
        self.items = []

    def grid_intersections(self, num_items):
        """
        Returns list of coordinates where grid lines intersect in
        format [(x, y), ...]

        Grid always has same number of vertical and horizontal
        columns.

        There has to be at least 2px margin between grid lines.
        """
        num_columns = min([num_items + 1, Item.MIN_SIDE_SIZE])
        column_width = self.container.width / num_columns
        column_height = self.container.height / num_columns

        points = []
        for x in range(0, num_items):
            for y in range(0, num_items):
                px = (x * (column_width + 1)) + column_width
                py = (y * (column_height + 1)) + column_height

                # there has to be at least 1px margin around the intersection point
                if px + 1 >= self.container.width or py + 1 >= self.container.height or \
                   px - 1 < 0 or py - 1 < 0:
                    # item would go out bounds of the container, skip this point...
                    continue

                points.append((px, py))

        return points

    def add(self, item):
        """
        Add a new item to the layout and re-arrange the layout.

        Raise an error if items are overlapping or container is too
        small.
        """
        self.items.append(item)

        # make sure there's enough space to fit all items
        if self.container.capacity(Item.MIN_SIDE_SIZE) < len(self.items):
            raise LayoutError("container too small to fit all items")

        points = self.grid_intersections(len(self.items))
        self._arrange(points)

        if self.items_intersect():
            raise LayoutError("overlapping items")

    def _arrange(self, points):
        """
        Arrange items in layout or raise error if it's not possible.
        """
        i = 0
        for item in self.items:
            item.x = points[i][0]
            item.y = points[i][1]

            # make sure item fits within the container bounds
            if not self.container.within_bounds(item):
                raise LayoutError("item doesn't fit in the container")

            i += 1