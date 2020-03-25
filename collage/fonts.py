from matplotlib import font_manager
import numpy as np


def get_system_fonts():
    fonts = []
    for x in font_manager.findSystemFonts():
        x = x[::-1]
        dot = x.find('.')
        slash = x.find('\\')
        x = x[slash-1:dot:-1]
        fonts += [x]
    return np.unique(fonts)
