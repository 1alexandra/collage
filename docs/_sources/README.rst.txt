User Guide
==========


About application
-----------------

The app allows you to create collages from photos.
You can add photos interactively: you can add a photo from any of the four
sides of the rectangle, but it will take up half of the image, and the rest
of the collage will be scaled automatically. The basic functions are creating
a canvas of any size, adding photos, automatically zooming and cropping them,
and saving and printing the resulting collage. As additional functions, you can
change the parameters of the image borders (size, steepness of the rounded
corner), implement control of elements on the canvas: the ability to move the
borders, change the cropping window of the photo (zoom and change the
position), and add a caption to the canvas.


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
      Click on a border part. When it is selected, you can move it by the keyboard
      arrows: vertical borders can be moved left and right,
      horizontal can be moved up or down. 

Initially, middle part of the photo appears in the cell. You can change the position:
select photo sell using mouse click and use keyboard arrows to move photo inside
the cell. When you reach the photo boarder, the app will show a warning message.
Also, you can change photo scale by ``[`` and ``]`` keyboard buttons. If you trying 
to scale photo beyond it's boarder, a worning message will be shown. To confirm 
new photo scale and position, click somewhere outside this photo cell or press
``Enter`` button. If you want to cancel your changes, press ``Esc``.

Click on ``Add text...`` button to open capture setup window.
This window consists of five blocks:

    - text redactor,
    - font chooser,
    - canvas with an intermediate result,
    - font parameters input fields: italic, bold, underlined checkboxes
      and font size entry,
    - buttons block: ``Change color...``, ``Try font``, ``OK`` buttons.

Write your caption in text redactor, choose font and style, click on ``Try font``
button to see the result. If you want to add it to the collage, click on ``OK``
button. Otherwise continue changing it or close the window.

When your caption is placed on the collage, you can click on it and move over
the collage using keyboard arrows.

