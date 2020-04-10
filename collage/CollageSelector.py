class CollageSelector():
    """
    Class for collage items selection
    """
    def __init__(self, item):
        """
        item - CollageItem object
        """
        self.item = item
        self.collage = item.collage
        self.is_selected = False

    def apply_selection(self):
        """
        If item not selected then sets selection
        If item select then unsets selection
        """
        if self.is_selected:
            self.unset_selection()
        else:
            self.set_selection()

    def reset_selection(self):
        """
        If item selected then redraws selection
        """
        if self.is_selected:
            self.unset_selection()
            self.set_selection()

    def set_selection(self):
        if not self.is_selected:
            self.is_selected = True
            bounds = self.collage.bbox(self.item.Id)
            self.collage.coords(
                self.collage.selection_rectangle_id,
                *bounds
            )

    def unset_selection(self):
        if self.is_selected:
            self.is_selected = False
            self.collage.coords(self.collage.selection_rectangle_id, 0, 0, 0, 0)
