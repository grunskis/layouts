from unittest import TestCase

from mock import patch

from ..primitives import Container, Circle
from ..layouts import HorizontalLineLayout, GridLayout, CircleLayout, RandomLayout
from ..errors import LayoutError


class TestHorizontalLineLayout(TestCase):
    def setUp(self):
        self.container = Container(width=3, height=3)

    def test_baseline_odd_height(self):
        l1 = HorizontalLineLayout(Container(width=1, height=3))
        self.assertEquals(l1.baseline, 1)
        l2 = HorizontalLineLayout(Container(width=1, height=5))
        self.assertEquals(l2.baseline, 2)

    def test_baseline_even_height(self):
        l1 = HorizontalLineLayout(Container(width=1, height=4))
        self.assertEquals(l1.baseline, 1)
        l2 = HorizontalLineLayout(Container(width=1, height=6))
        self.assertEquals(l2.baseline, 2)

    def test_no_items(self):
        layout = HorizontalLineLayout(self.container)
        self.assertEquals(layout.as_tuples(), [])

    def test_one_item_valid_layout(self):
        layout = HorizontalLineLayout(self.container)
        circle = Circle(radius=1)
        layout.add(circle)

        items = layout.as_tuples()
        self.assertEquals(items, [(1, 1, 1)])

    def test_one_item_invalid_layout(self):
        # circle radius too big to fit into the provided container
        layout = HorizontalLineLayout(self.container)
        with self.assertRaises(LayoutError):
            layout.add(Circle(radius=2))

    def test_multiple_item_layout(self):
        container = Container(height=3, width=6)
        layout = HorizontalLineLayout(container)

        layout.add(Circle(radius=1))
        items = layout.as_tuples()
        self.assertEquals(items, [(3, 1, 1)])

        layout.add(Circle(radius=1))
        items = layout.as_tuples()
        self.assertEquals(items, [(1, 1, 1), (4, 1, 1)])

        # no space for another circle
        with self.assertRaises(LayoutError):
            layout.add(Circle(radius=1))

    def test_multiple_items_overlap(self):
        container = Container(height=5, width=7)
        layout = HorizontalLineLayout(container)
        layout.add(Circle(radius=1))
        with self.assertRaises(LayoutError):
            layout.add(Circle(radius=2))


class GridLayoutTests(TestCase):
    def test_grid_intersections(self):
        layout = GridLayout(Container(width=7, height=7))
        self.assertEquals(layout.grid_intersections(1), [(3, 3)])
        self.assertEquals(layout.grid_intersections(2), [(2, 2), (2, 5), (5, 2), (5, 5)])
        self.assertEquals(layout.grid_intersections(3), [(2, 2), (2, 5), (5, 2), (5, 5)])
        self.assertEquals(layout.grid_intersections(4), [(2, 2), (2, 5), (5, 2), (5, 5)])
        self.assertEquals(layout.grid_intersections(5), [(2, 2), (2, 5), (5, 2), (5, 5)])
            
    def test_grid_layout_add_items_overlap(self):
        layout = GridLayout(Container(width=7, height=7))
        layout.add(Circle(radius=2))
        with self.assertRaises(LayoutError):
            layout.add(Circle(radius=1))

    def test_contiiner_not_big_enough(self):
        layout = GridLayout(Container(width=3, height=3))
        layout.add(Circle(radius=1))
        with self.assertRaises(LayoutError):
            layout.add(Circle(radius=1))


class CircleLayoutTests(TestCase):
    def test_circle_radius(self):
        l1 = CircleLayout(Container(width=20, height=10))
        self.assertEquals(l1.circle_radius, 2)
        l2 = CircleLayout(Container(width=40, height=60))
        self.assertEquals(l2.circle_radius, 10)

    def test_circle_center(self):
        l1 = CircleLayout(Container(width=4, height=4))
        self.assertEquals(l1.circle_center, (2, 2))
        l2 = CircleLayout(Container(width=5, height=5))
        self.assertEquals(l2.circle_center, (2, 2))

    def test_item_coordinates(self):
        tests = {
            1: [(15, 10)],
            2: [(5, 10), (15, 10)],
            3: [(8, 15), (8, 6), (15, 10)],
            4: [(10, 15), (5, 10), (10, 5), (15, 10)],
        }
        l = CircleLayout(Container(width=20, height=20))
        for num_items, coords in tests.items():
            self.assertEquals(l.item_coordinates(num_items), coords)

    def test_add_items(self):
        layout = CircleLayout(Container(width=9, height=9))
        layout.add(Circle(radius=1))
        layout.add(Circle(radius=1))

        self.assertEquals(layout.as_tuples(), [(2, 4, 1), (6, 4, 1)])

        with self.assertRaises(LayoutError):
            layout.add(Circle(radius=1))


class RandomLayoutTests(TestCase):
    def test_center_coords(self):
        radius = 1
        layout = RandomLayout(radius, Container(width=3, height=3))
        self.assertEquals(layout.center_coords(), {(1, 1)})

        radius = 2
        layout = RandomLayout(radius, Container(width=3, height=3))
        self.assertEquals(layout.center_coords(), set())

        radius = 1
        layout = RandomLayout(radius, Container(width=4, height=4))
        self.assertEquals(layout.center_coords(), {(1, 1), (1, 2), (2, 1), (2, 2)})

    def test_center_coords_cleanup(self):
        radius = 1
        point = (1, 1)
        coords = {(1, 1)}
        layout = RandomLayout(radius, Container(width=3, height=3))
        self.assertEquals(layout.center_coords_cleanup(coords, point), set())

        radius = 2
        point = (2, 2)
        layout = RandomLayout(radius, Container(width=7, height=5))
        coords = layout.center_coords()
        self.assertEquals(layout.center_coords_cleanup(coords, point), set())

        radius = 1
        point = (1, 1)
        layout = RandomLayout(radius, Container(width=6, height=3))
        coords = layout.center_coords()
        self.assertEquals(layout.center_coords_cleanup(coords, point), {(4, 1)})

    def test_item_coordinates(self):
        def random_choice_mock_x(coords):
            # always return point with smallest x coordinate
            return sorted(coords)[0]

        def random_choice_mock_y(coords):
            # always return point with smallest y coordinate
            return sorted(coords, key=lambda x: x[1])[0]

        radius = 1
        l1 = RandomLayout(radius, Container(width=6, height=3))
        with patch("random.choice", side_effect=random_choice_mock_x):
            self.assertEquals(l1.item_coordinates(1), [(1, 1)])
            self.assertEquals(l1.item_coordinates(2), [(1, 1), (4, 1)])
            self.assertEquals(l1.item_coordinates(3), [(1, 1), (4, 1)])

        l2 = RandomLayout(radius, Container(width=3, height=6))
        with patch("random.choice", side_effect=random_choice_mock_y):
            self.assertEquals(l2.item_coordinates(1), [(1, 1)])
            self.assertEquals(l2.item_coordinates(2), [(1, 1), (1, 4)])
            self.assertEquals(l2.item_coordinates(3), [(1, 1), (1, 4)])

    def test_add_items(self):
        radius = 1
        l1 = RandomLayout(radius, Container(width=3, height=3))
        with self.assertRaises(AssertionError):
            l1.add(Circle(radius=2))  # radius mismatch

        l1.add(Circle(radius=1))
        with self.assertRaises(LayoutError) as e:
            l1.add(Circle(radius=1))
        self.assertEquals(e.exception.message, "container too small to fit all items")

    def test_add_items_no_space(self):
        def random_choice_mock_x(coords):
            # always return point with median x coordinate
            return sorted(coords)[len(coords) / 2]

        radius = 1
        l1 = RandomLayout(radius, Container(width=6, height=3))
        with patch("random.choice", side_effect=random_choice_mock_x):
            # item placed in a way that there's no more space for the 2nd item
            l1.add(Circle(radius=1))
            with self.assertRaises(LayoutError) as e:
                l1.add(Circle(radius=1))
            self.assertEquals(e.exception.message, "couldn't place all items in the container")
