from src.core.controller import Controller
from src.ui.menu_view import MenuView

def test_mode_menu_navigation():
    c = Controller()
    c.press("mode")
    for _ in range(6):
        c.press("down")
    assert c.state.menu_page == 1
    c.press("1")
    assert c.state.mode == "TABLE"

def test_menu_render(application):
    c = Controller()
    menu = MenuView()
    c.press("mode")
    menu.render(c.state)
    assert not menu.isHidden()
    assert "COMP" in menu.options.text()
    menu.close()
