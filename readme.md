# Layouts

## What is this all about?

When young children learn how to count, they need to understand that
the position of the objects doesn't matter. For example, if I show 10
objects in a line, and then move them around to form a circle, there
are still 10 objects!


## Requirements & dependencies

All scripts are implemented in Python. I've only tested this with
Python 2.7.12. There are 2 dependencies to external libraries that are
not included in the Python standard library:

* `Pillow` - an imaging library used to create visual representation of the layout
* `mock` - mocking library used in unit tests

To install all 3rd-party dependencies run:

    $ pip install -r requirements.txt


## Running the CLI script

To interact with the layout generator you can use the provided
`main.py` CLI script. To list all the available options use `-h`
command line switch:

    $ python main.py -h
    usage: main.py [-h] [-t {horizontal_line,random,grid,circle}] [-r RADIUS]
                   width height num_items
    
    Arrange circles of RADIUS in the selected layout.
    
    positional arguments:
      width                 container width
      height                container height
      num_items             number of items to add to container
    
    optional arguments:
      -h, --help            show this help message and exit
      -t {horizontal_line,random,grid,circle}, --layout-type {horizontal_line,random,grid,circle}
                            type of layout to generate. default: horizontal_line
      -r RADIUS, --radius RADIUS
                            radius of the items. default: 10px

This script prints out coordinates of items laid out in different
layouts within the container of specified size. The format of the
output is:

    [(x0, y0, r0), (x1, y1, r1), (xN, yN, rN), ...]

The layout image is also saved as bitmap file in `plot.bmp` and placed
in the current working directory.

If the number of items can't be arranged in the container of specified
size or the items would overlap then an error message will be printed.

Example layouts:

Layout | Command | Output | Plot
-------|---------|--------|-----
Horizontal line | `python main.py -t grid 100 100 3` | `[(33, 33, 10), (33, 67, 10), (67, 33, 10)]` | ![grid layout](/examples/grid3.bmp)
Grid | `python main.py -r 5 100 20 5` | `[(10, 9, 5), (30, 9, 5), (50, 9, 5), (70, 9, 5), (90, 9, 5)]` | ![horizontal line layout](/examples/hline5.bmp)
Circle | `python main.py -r 4 -t circle 70 50 3` | `[(30, 36, 4), (29, 15, 4), (47, 25, 4)]` | ![circle layout](/examples/circle3.bmp)
Random | `python main.py -t random 100 100 10` | `[(59, 25, 10), (22, 64, 10), (88, 77, 10), (82, 54, 10), (31, 41, 10), (59, 49, 10), (31, 88, 10), (81, 18, 10), (60, 79, 10), (32, 14, 10)]` | ![random layout](/examples/random10.bmp)


## Running unit tests

    $ make test
