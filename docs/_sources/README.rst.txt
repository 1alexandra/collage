User Guide
==========


About application
-----------------

The app allows you to create collages from photos.
You can add photos interactively: you can add a photo from any of the four
sides of the rectangle, but it will take up half of the image, and the rest
of the collage will be scaled automatically. The basic functions are creating
a canvas of any size, adding photos, automatically zooming and cropping them,
and saving the resulting collage. As additional functions, you can
change the parameters of the image borders (size, padding, corner type),
implement control of elements on the canvas: the ability to move the
borders, change the cropping window of the photo (zoom and change the
position).


Installation
------------

To install the app clone repository https://github.com/1alexandra/collage
and in collage root directory execute::

    python3 -m pip install setuptools==46.0.0 wheel==0.34.2
    python3 setup.py sdist bdist_wheel
    pip3 install dist/collage-0.0.1-py3-none-any.whl


Running
-------

To run the app execute in collage root directory::

    python3 run.py


Testing
-------

To test the app modules execute in collage root directory::

    python3 -m pytest


Flake8
------

Run the command to check flake8 code in collage root directory::

    flake8


Localisation
------------

The application is adapted for two languages: English and Russian. 
Localization is selected based on system parameters.


How to use
----------

After launching the app, you see a window divided into two areas: the menu and
the workspace.

Use the input fields in the menu to configure collage settings.
Make sure that you have entered numbers that match the input format:
the values in pixels must be natural numbers,
and the real values must be real numbers.
After completing the changes, click the ``Change settings`` button.
You can also change the parameters while editing the collage.

Use one of the ``+`` buttons on the right side of the screen to add the first
photo to the collage. The app supports adding photos in JPEG, PNG, GIF, TIFF,
and BMP formats.

After adding the first photo to the collage,
you can update layout by 3 types of operations:

1. Adding a photo from one side of the collage border.
      In this case, the new cell appears on this side of the collage
      and takes up half of the collage regardless of size.
      All previously existing cells are compressed to make room for a new cell.
2. The division of the photo cell.
      After right-clicking on a photo, a drop-down menu appears with
      the options: add photo on the left, add photo on the right,
      add photo on the top, add photo on the bottom.
      If you click on one of them, the selected photo cell is divided into two cells,
      one of which is placed a new photo, according to your side choice,
      and the second remains the old photo.
3. Movement of the border between photos.
      Hold down the left mouse button on boarder part and
      drag the border between cells moving the mouse.

Initially, middle part of the photo appears in the cell. You can change the position:
select photo cell using mouse click and use keyboard arrows to move photo inside
the cell or simply use mouse.
Also, you can change photo scale using mouse wheel or ``[`` and ``]`` keyboard buttons.

You can dump and load collage project using menu buttons. Use ``Save as...``
menu button to save collage image file to file system.
After saving the file, you can open it in any graphics editor and do whatever you want with it.