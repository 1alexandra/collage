import numpy as np
from PIL import Image, ImageFilter


class CornerCreator:
    """Create corners with a given curvature from 0 to 1.

    ``Curve``:
    - 0: no corners,
    - from 0 to 0.5: hyperbolic convex corners,
    - 0.5: linear corners,
    - from 0.5 to 1: hyperbolic concave corners,
    - 1: square corner.

    ``Width``:
        defines corner size (Width x Width).
    """
    def __init__(self, corner_width, corner_curvature):
        self.Width = corner_width
        self.Curve = corner_curvature

    Width = property()
    Curve = property()

    @Width.getter
    def Width(self):
        return self._width

    @Width.setter
    def Width(self, value):
        self._width = max(value, 0)

    @Curve.getter
    def Curve(self):
        return self._curve

    @Curve.setter
    def Curve(self, value):
        self._curve = max(min(value, 1), 0)

    def linear(self, x):
        """Linear L(x).

        L(0) = Width,
        L(Width * Curve) = Width * Curve,
        L(Width) = 0.
        """
        if self.Curve == 0:
            return 0
        if self.Curve == 0.5:
            return self.Width - x
        if self.Curve == 1:
            return self.Width

    def hyperbole(self, x):
        """Hyperbolic h(x).

        h(0) = Width,
        h(Width * Curve) = Width * Curve,
        h(Width) = 0.
        """
        c = self.Width
        z = self.Curve
        a = z * z * c / (1 - 2 * z)
        k = a * (a + c)
        b = - k / (a + c)
        return k / (x + a) + b

    def corner_function(self, x):
        if not (0 <= x <= self.Width):
            return 0
        if self.Curve in [0, 0.5, 1]:
            return self.linear(x)
        return self.hyperbole(x)

    def get_corner(self):
        """Return boolean array with (Width x Widht) corner."""
        r = self.Width
        corner = np.ones((r, r))
        for i in range(r):
            cols = np.round(self.corner_function(i))
            corner[i, :int(cols)] = False
        return np.logical_or(corner, corner.T)

    def apply_corner(self, arr, corner):
        """Apply corner mask to all four arr corners with correct rotation."""
        r = self.Width

        arr[:r, :r] = np.logical_and(arr[:r, :r], corner)
        corner = np.rot90(corner)

        arr[-r:, :r] = np.logical_and(arr[-r:, :r], corner)
        corner = np.rot90(corner)

        arr[-r:, -r:] = np.logical_and(arr[-r:, -r:], corner)
        corner = np.rot90(corner)

        arr[:r, -r:] = np.logical_and(arr[:r, -r:], corner)
        corner = np.rot90(corner)

        return arr

    def smooth_boundary(self, mask):
        """Put zeros to the boundary points."""
        mask[0] = 0
        mask[-1] = 0
        mask[:, 0] = 0
        mask[:, -1] = 0

    def get_alpha(self, size):
        """Return PIL Image alpha channel with 0 in corners and boundary.
        
        If size < 2.1 * Width, the corners don't appear."""
        h, w = size
        if w <= 0 or h <= 0:
            return np.array([])
        mask = np.ones((w, h), dtype=bool)
        self.smooth_boundary(mask)
        minsize = 2.1 * self.Width
        if self.Width > 0 and min(w, h) >= minsize:
            corner = self.get_corner()
            self.apply_corner(mask, corner)
        alpha = mask.astype(np.uint8) * 255
        alpha = Image.fromarray(alpha, mode="L")
        return alpha.filter(ImageFilter.GaussianBlur(3))
