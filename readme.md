# Layouts

## What is this all about?

When young children learn how to count, they need to understand that
the position of the objects doesn't matter. For example, if I show 10
objects in a line, and then move them around to form a circle, there
are still 10 objects!


## Requirements & dependencies

All scripts are implemented in Python. I've only tested this with
Python 2.7. The only requirement that is not included in the Python
standard library is `Pillow`. `Pillow` is an imaging library used to
create visual representation of the layout.

To install dependencies run:

    $ pip install -r requirements.txt


## Running the CLI script

This script prints out coordinates of items laid out in different
layouts within the container of specified size. The format of the
output is:

    [(x0, y0, r0), (x1, y1, r1), (xN, yN, rN), ...]

To interact with the layout generator you can use the provided
`main.py` CLI script. To list all the available options use `-h`
command line switch:

    $ python main.py -h
    usage: main.py [-h] [-t {horizontal_line,grid}] [-r RADIUS]
                   width height num_items
    
    Arrange circles of RADIUS in the selected layout.
    
    positional arguments:
      width                 container width
      height                container height
      num_items             number of items to add to container
    
    optional arguments:
      -h, --help            show this help message and exit
      -t {horizontal_line,grid}, --layout-type {horizontal_line,grid}
                            type of layout to generate. default: horizontal_line
      -r RADIUS, --radius RADIUS
                            radius of the items. default: 10px

If the number of items can't be arranged in the container of specified
size or the items would overlap then an error message will be printed.

An example run that will arrange 3 circles in a grid layout:

    $ python main.py -t grid 100 100 3
    [(33, 33, 10), (33, 67, 10), (67, 33, 10)]
    
Also the following image of the grid layout is saved in `plot.bmp`
file:

![grid layout](/examples/grid3.bmp)

Another example with horizontal line layout of 5 circles:

    $ python main.py -r 5 100 20 5
    [(10, 9, 5), (30, 9, 5), (50, 9, 5), (70, 9, 5), (90, 9, 5)]

![horizontal line layout](/examples/hline5.bmp)


## Running unit tests

    $ make test
