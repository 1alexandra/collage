import os
import numpy as np
from src.CornerCreator import CornerCreator


def test_PolyCorner():
    c = 200
    w = int(2.5 * c + 12)
    h = 5 * c + 24
    for z in [0.3, 0.9]:
        cr = CornerCreator(c, z)
        alpha = cr.get_alpha((h, w))
        alpha = np.asarray(alpha, dtype=np.uint8)
        name = 'corner_example_' + str(z) + '.npy'
        path = os.path.join('test', 'files', name)
        saved = np.load(path)
        assert alpha.shape == saved.shape
        assert np.all(alpha == saved)
