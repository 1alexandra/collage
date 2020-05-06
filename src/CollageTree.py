import tkinter as tk
from src.utils import ask_open_image, get_orient, is_up_left, int_clamp, is_vertical, mix_image_with_bg
from src.CollageImage import safe_open_image
from src.BaseTkTree import BaseTkTreeNode, BreedingTkNode, UpdatableTkNode
from src.constants import WINDOW_SEP_WIDTH, HIGHLIGHT_BORDER_WIDTH
from PIL import Image
from PIL.ImageTk import PhotoImage


class CollageBreedingNode(BreedingTkNode):
    def add_image_child(self, image, where, corner_creator, margin=0):
        assert where in ('w', 's', 'n', 'e')

        # actually, it doesn't matter, what width and height we are passing
        # to the constructor, because we align the windows later anyway
        width, height = self._width, self._height
        leaf_node = ResizableLeaf(
            image=image, corner_creator=corner_creator, parent=self,
            width=width, height=height, bg=self._bg, bd=0, highlightthickness=0, margin=margin
        )
        self.add_child(leaf_node, begin=is_up_left(where))


class InternalTkNode(CollageBreedingNode, UpdatableTkNode):
    def __init__(self, parent, orient, **init_kwargs):
        BaseTkTreeNode.__init__(
            self, tk.PanedWindow, parent=parent, orient=orient,
            sashwidth=WINDOW_SEP_WIDTH, sashpad=0, bd=0, opaqueresize=False,
            **init_kwargs
        )
        self._is_vertical = is_vertical(orient)

    def add_to_collage(self, im, x_offset, y_offset):
        if self._left is not None:
            self._left.add_to_collage(im, x_offset, y_offset)
        if self._right is not None:
            if self._is_vertical:
                self._right.add_to_collage(im, x_offset, y_offset + self._left.get_height() + WINDOW_SEP_WIDTH)
            else:
                self._right.add_to_collage(im, x_offset + self._left.get_width() + WINDOW_SEP_WIDTH, y_offset)

    def __getstate__(self):
        state = self.__dict__.copy()
        state['_root'] = None
        return state


class CollageRoot(CollageBreedingNode):
    def __init__(self, tk_master, corner_creator, margin=0, **init_kwargs):
        super().__init__(obj_class=tk.PanedWindow, parent=None, bd=0, tk_master=tk_master, **init_kwargs)

        self._margin = margin
        self._corner_creator = corner_creator

    def __getstate__(self):
        state = self.__dict__.copy()
        state['_root'] = None
        return state

    def reload_object(self, tk_master):
        self._create_tk_object(tk_master=tk_master)
        self._left.update_tk_object()

    def get_corners(self):
        return self._corner_creator

    def save_collage(self, filename):
        if self._left is not None and filename != "":
            collage_im = Image.new("RGBA", (self._width, self._height))
            self._left.add_to_collage(collage_im, 0, 0)

            collage_im = mix_image_with_bg(collage_im, bg_color=self._bg)
            collage_im.save(filename)

    def add_image(self, image, where):
        """
        Adds the image to the collage.
        If there were no images before, just adds it,
        otherwise - creates new PanedWindow that consists of
        old version of collage and new image.

        Parameters
        ----------
        image : PILCollageImage

        where: str
            Specifies the place where we should put the image.
            Can be one of ('w', 's', 'n', 'e').
        """
        if self._left is not None:
            self._left.wrap_into_paned(internal_node_class=InternalTkNode, orient=get_orient(where))
            self._left.add_image_child(
                image=image, where=where, margin=self._margin,
                corner_creator=self._corner_creator)
        else:
            self.add_image_child(
                image=image, where=where, margin=self._margin,
                corner_creator=self._corner_creator)

    def update_params(self, new_width, new_height, new_margin):
        """
        Updates images' corners.
        Also updates some other collage parameters according to the passed arguments.

        Parameters
        ----------
        new_width: int, non-negative
        new_height: int, non-negative
        new_margin: int, non-negative
        """
        assert new_margin >= 0
        assert new_height >= 0
        assert new_width >= 0
        if new_width != self._width or new_height != self._height:
            self._root.config(width=new_width, height=new_height)
        self._margin = new_margin
        self.update_leaf_vars(margin=self._margin)


class CollageLeafNode(UpdatableTkNode):
    def __init__(self, image, corner_creator, parent, margin=0, **init_kwargs):
        self._margin = margin
        self._image = image
        self._image_id = None

        self._corner_creator = corner_creator

        super().__init__(obj_class=tk.Canvas, parent=parent, **init_kwargs)

    def get_real_width(self):
        """Returns actual width of the image (without margin)"""
        return int_clamp(self._width - 2 * self._margin, min_val=0)

    def get_real_height(self):
        """Returns actual height of the image (without margin)"""
        return int_clamp(self._height - 2 * self._margin, min_val=0)

    def update_leaf_vars(self, margin=None, **kwargs):
        """Updates the margin and corners of the image"""
        if margin is not None:
            diff = margin - self._margin
            self._margin = margin
            self._move_image_on_canvas(dx=diff, dy=diff)
        self._set_image()

    def destroy(self):
        """
        Destroys the leaf and replaces the parent of the leaf
        by the only child left (so the tree remains to be binary).
        """
        self._parent.remove_child(self)
        self._parent.collapse()

    def _move_image_on_canvas(self, dx, dy):
        """Moves the image on canvas"""
        if self._image_id is not None:
            self._root.move(self._image_id, dx, dy)

    def _set_image(self):
        """Resizes the image and puts it on canvas"""
        if self._image is not None:
            width, height = self.get_real_width(), self.get_real_height()
            self._image.resize((width, height))
            if self._image_id is None:
                self._create_image()
            else:
                self._update_image()

    def _set_photo_image(self):
        self._photo_im = PhotoImage(self._image.PIL)

    def _create_image(self, x_coord=0, y_coord=0):
        """Creates the image and puts it on canvas"""
        self._delete_image()
        self._set_photo_image()
        self._image_id = self._root.create_image(
            self._margin + x_coord, self._margin + y_coord, anchor="nw", image=self._photo_im)

    def _update_image(self):
        """Updates the image on canvas"""
        self._set_photo_image()
        self._root.itemconfig(self._image_id, image=self._photo_im)

    def _delete_image(self):
        """Deletes the image from canvas"""
        if self._image_id is not None:
            self._root.delete(self._image_id)
            self._image_id = None

    def _create_tk_object(self, tk_master=None):
        """Creates the canvas"""
        self._image_id = None

        super()._create_tk_object(tk_master)

        self._set_image()

        self._context_menu = tk.Menu(self._root, tearoff=0)
        self._context_menu.add_command(label="Add image to the left", command=self._add_image_func('w'))
        self._context_menu.add_command(label="Add image to the right", command=self._add_image_func('e'))
        self._context_menu.add_command(label="Add image on top", command=self._add_image_func('n'))
        self._context_menu.add_command(label="Add image below", command=self._add_image_func('s'))
        self._context_menu.add_command(label="Remove the image", command=self.destroy)

        self._root.bind("<Button-3>", self._context_menu_handler)
        self._root.bind("<FocusIn>", lambda _: self._root.config(highlightthickness=HIGHLIGHT_BORDER_WIDTH))
        self._root.bind("<FocusOut>", lambda _: self._root.config(highlightthickness=0))

    def _resize_handler(self, event):
        if event.width != self._width or event.height != self._height:
            self._width = event.width
            self._height = event.height
            self._set_image()
            self._parent.update_proportion(self)

    def _context_menu_handler(self, event):
        self._root.focus_set()
        try:
            # display the context menu
            self._context_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self._context_menu.grab_release()

    def add_image(self, image, where):
        """
        Adds new image to the tree.

        Creates new PanedWindow that consists of this image and the currently loaded image.

        Parameters
        ----------
        where: str
            Specifies the place where we should put the image.
            Can be one of ('w', 's', 'n', 'e').
        """
        if image:
            self.wrap_into_paned(internal_node_class=InternalTkNode, orient=get_orient(where))
            self._parent.add_image_child(
                image=image, margin=self._margin, where=where,
                corner_creator=self._corner_creator
            )

    def _add_image_func(self, where):
        def func():
            filename = ask_open_image()
            image = safe_open_image(filename, corner_creator=self._corner_creator)
            self.add_image(image=image, where=where)
        return func

    def add_to_collage(self, im, x_offset, y_offset):
        raise NotImplementedError('add_to_collage is not implemented')


class ResizableLeaf(CollageLeafNode):
    def __init__(self, *args, **kwargs):
        self._corner = None

        super().__init__(*args, **kwargs)

    def _create_tk_object(self, tk_master=None):
        """Creates the canvas"""
        super()._create_tk_object(tk_master)

        self._cur_x = None
        self._cur_y = None

        self._root.bind("<Button-1>", self._drag_event_handler)
        self._root.bind("<ButtonRelease-1>", self._drag_release_handler)
        self._root.bind("<B1-Motion>", self._pressed_mouse_motion_handler)
        self._root.bind("<Up>", self._move_image_view_up_handler)
        self._root.bind("<Down>", self._move_image_view_down_handler)
        self._root.bind("<Left>", self._move_image_view_left_handler)
        self._root.bind("<Right>", self._move_image_view_right_handler)
        self._root.bind("<Key>", self._scale_image_handler)
        self._root.bind("<MouseWheel>", self._on_mousewheel)

    def _create_image(self):
        """Creates the image and puts it on canvas"""
        if self._corner is None:
            super()._create_image()
        else:
            super()._create_image(x_coord=self._corner[0], y_coord=self._corner[1])

    def _update_image(self):
        """Updates the image on canvas"""
        if self._corner is None:
            diff = self._image.corner
        else:
            diff = (self._image.corner[0] - self._corner[0], self._image.corner[1] - self._corner[1])
        self._corner = self._image.corner
        self._move_image_on_canvas(*diff)
        super()._update_image()

    def _on_mousewheel(self, event):
        if event.delta > 0:
            self._image.zoom_in()
        else:
            self._image.zoom_out()
        self._update_image()

    def _scale_image_handler(self, event):
        if event.char in ['[', ']']:
            if event.char == '[':
                self._image.zoom_in()
            elif event.char == ']':
                self._image.zoom_out()
            self._update_image()

    def _move_image_view_up_handler(self, _):
        self._image.move_view_up()
        self._update_image()

    def _move_image_view_down_handler(self, _):
        self._image.move_view_down()
        self._update_image()

    def _move_image_view_left_handler(self, _):
        self._image.move_view_left()
        self._update_image()

    def _move_image_view_right_handler(self, _):
        self._image.move_view_right()
        self._update_image()

    def _drag_event_handler(self, event):
        self._root.focus_set()
        self._root.config(cursor="fleur")
        self._cur_x = event.x
        self._cur_y = event.y

    def _pressed_mouse_motion_handler(self, event):
        offset_x = event.x - self._cur_x
        offset_y = event.y - self._cur_y
        self._cur_x = event.x
        self._cur_y = event.y
        self._image.move_view(-offset_x, -offset_y)
        self._update_image()

    def _drag_release_handler(self, _):
        self._root.config(cursor="")
        self._cur_x = None
        self._cur_y = None

    def add_to_collage(self, collage_im, x_offset, y_offset):
        im = self._image.PIL
        corner = (0, 0) if self._corner is None else self._corner
        corner = (corner[0] + self._margin, corner[1] + self._margin)
        collage_im.paste(im, (x_offset + corner[0], y_offset + corner[1]))

    def __getstate__(self):
        state = self.__dict__.copy()
        state['_root'] = None
        state['_image_id'] = None
        state['_photo_im'] = None
        state['_context_menu'] = None
        return state
