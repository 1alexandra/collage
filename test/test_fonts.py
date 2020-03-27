import collage.fonts


def test_get_system_fonts():
    fonts = collage.fonts.get_system_fonts()
    assert len(fonts) > 0
