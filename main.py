from argparse import ArgumentParser

import layouts

from layouts import horizontal_line_layout, grid_layout


DEFAULT_RADIUS = 10  # px

LAYOUT_FUNCTION_MAP = {
    "horizontal_line": horizontal_line_layout,
    "grid": grid_layout,
}

LAYOUT_TYPES = LAYOUT_FUNCTION_MAP.keys()


if __name__ == "__main__":
    parser = ArgumentParser(description="Arrange circles of RADIUS in the selected layout.")
    parser.add_argument("width", type=int, help="container width")
    parser.add_argument("height", type=int, help="container height")
    parser.add_argument("num_items", type=int, help="number of items to add to container")
    parser.add_argument("-t", "--layout-type", choices=LAYOUT_TYPES, default=LAYOUT_TYPES[0],
                        help="type of layout to generate. default: %s" % LAYOUT_TYPES[0])
    parser.add_argument("-r", "--radius", type=int, default=DEFAULT_RADIUS,
                        help="radius of the items. default: %dpx" % DEFAULT_RADIUS)
    args = parser.parse_args()

    layout_function = LAYOUT_FUNCTION_MAP[args.layout_type]

    layouts.radius = args.radius
    print(layout_function(args.width, args.height, args.num_items))
