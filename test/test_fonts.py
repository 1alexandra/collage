from src.fonts import get_system_fonts


def test_get_system_fonts():
    fonts = get_system_fonts()
    assert len(fonts) > 0
