from collage.CollageSelector import CollageSelector


class CollageItem():
    def __init__(self, id, collage):
        self.id = id
        self.collage = collage
        self.selector = CollageSelector(self)

    def move(self, dx, dy):
        return self.collage.move(self.Id, dx, dy)

    def apply_selection(self):
        """
        If item not selected then sets selection
        If item select then unsets selection
        """
        return self.selector.apply_selection()

    def reset_selection(self):
        """
        If item selected then redraws selection
        """
        return self.selector.reset_selection()

    def set_selection(self):
        return self.selector.set_selection()

    def unset_selection(self):
        return self.selector.unset_selection()

    Id = property()
    Pos = property()
    IsSelected = property()

    @Pos.getter
    def Pos(self):
        return self.collage.coords(self.Id)

    @Id.getter
    def Id(self):
        return self.id

    @IsSelected.getter
    def IsSelected(self):
        return self.selector.is_selected
