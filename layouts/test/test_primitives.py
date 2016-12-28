from unittest import TestCase
from itertools import combinations

from ..primitives import Container, Circle


class ContainerTests(TestCase):
    def test_invalid_dimensions(self):
        with self.assertRaises(AssertionError):
            self.assertEquals(Container(width=0, height=0))
        with self.assertRaises(AssertionError):
            self.assertEquals(Container(width=1, height=0))
        with self.assertRaises(AssertionError):
            self.assertEquals(Container(width=0, height=1))

    def test_valid_dimensions(self):
        c = Container(width=1, height=2)
        self.assertEquals(1, c.width)
        self.assertEquals(2, c.height)

    def test_capacity(self):
        c1 = Container(width=1, height=1)
        self.assertEquals(c1.capacity(3), 0)

        c2 = Container(width=3, height=3)
        self.assertEquals(c2.capacity(3), 1)

        c3 = Container(width=3, height=5)
        self.assertEquals(c3.capacity(3), 1)

        c4 = Container(width=7, height=7)
        self.assertEquals(c4.capacity(3), 4)

    def test_within_bounds(self):
        c = Container(width=3, height=3)
        self.assertTrue(c.within_bounds(Circle(radius=1, x=1, y=1)))
        self.assertFalse(c.within_bounds(Circle(radius=2, x=1, y=1)))


class CircleTests(TestCase):
    def test_default_coordinates(self):
        c1 = Circle(radius=1)
        self.assertEquals(c1.x, 0)
        self.assertEquals(c1.y, 0)

        c2 = Circle(radius=1, x=1, y=1)
        self.assertEquals(c2.x, 1)
        self.assertEquals(c2.y, 1)

    def test_box_coordinates(self):
        tests = [
            {"x": 2, "y": 1, "box": (1, 0, 3, 2)},
            {"x": 1, "y": 2, "box": (0, 1, 2, 3)},
        ]
        for t in tests:
            c = Circle(radius=1, x=t["x"], y=t["y"])
            self.assertEquals(c.box_coordinates(), t["box"])


class ItemTests(TestCase):
    def test_items_intersect(self):
        a = Circle(radius=2, x=2, y=2)
        b = Circle(radius=1, x=2, y=5)
        self.assertTrue(a.intersects_with(b))

    def test_items_dont_intersect(self):
        items = [
            Circle(radius=1, x=2, y=2),
            Circle(radius=1, x=2, y=5),
            Circle(radius=1, x=5, y=2),
            Circle(radius=1, x=5, y=5),
        ]
        for a, b in combinations(items, 2):
            self.assertFalse(a.intersects_with(b))
