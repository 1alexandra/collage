import numpy as np
from PIL import Image, ImageFilter


class CornerCreator:
    def __init__(self, corner_width, corner_curvature):
        self.width = corner_width
        self.curve = corner_curvature

    def linear(self, x):
        """Linear L(x).

        L(0) = width,
        L(width * curve) = width * curve,
        L(width) = 0.
        """
        if self.curve == 0:
            return 0
        if self.curve == 0.5:
            return self.width - x
        if self.curve == 1:
            return self.width

    def hyperbole(self, x):
        """Hyperbolic h(x).

        h(0) = width,
        h(width * curve) = width * curve,
        h(width) = 0.
        """
        c = self.width
        z = self.curve
        a = z * z * c / (1 - 2 * z)
        k = a * (a + c)
        b = - k / (a + c)
        return k / (x + a) + b

    def corner_function(self, x):
        if not (0 <= x <= self.width):
            return 0
        if self.curve in [0, 0.5, 1]:
            return self.linear(x)
        return self.hyperbole(x)

    def get_corner(self):
        """Return boolean array width*widht with corner."""
        r = self.width
        corner = np.ones((r, r))
        for i in range(r):
            cols = np.round(self.corner_function(i))
            corner[i, :int(cols)] = False
        return np.logical_or(corner, corner.T)

    def apply_corner(self, arr, corner):
        """Apply corner mask to all four arr corners."""
        r = self.width

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
        """Return PIL Image alpha channel with 0 in corners and boundary."""
        h, w = size
        if w <= 0 or h <= 0:
            return np.array([])
        mask = np.ones((w, h), dtype=bool)
        self.smooth_boundary(mask)
        minsize = 2.1 * self.width
        if self.width > 0 and min(w, h) >= minsize:
            corner = self.get_corner()
            self.apply_corner(mask, corner)
        alpha = mask.astype(np.uint8) * 255
        alpha = Image.fromarray(alpha, mode="L")
        return alpha.filter(ImageFilter.GaussianBlur(3))
