from os import sep
from matplotlib import font_manager


def get_system_fonts():
    """Return sorted list of all system font names."""
    fonts = set()
    for x in font_manager.findSystemFonts():
        dot = x.rfind('.')
        slash = x.rfind(sep)
        x = x[slash + 1:dot]
        fonts.add(x)
    return sorted(fonts)
