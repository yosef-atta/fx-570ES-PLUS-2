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
    assert "▶ 1: COMP" in menu.options.text()
    assert "▼" in menu.heading.text()
    menu.close()

def test_setup_menu_render_and_selection(application):
    c = Controller()
    menu = MenuView()
    c.press("shift")
    c.press("mode")
    menu.render(c.state)
    assert not menu.isHidden()
    assert "SETUP" in menu.heading.text()
    assert "DEG" in menu.options.text()
    # Select RAD (option 4)
    c.press("4")
    menu.render(c.state)
    assert menu.isHidden()
    assert c.state.angle_unit == "RAD"
    menu.close()

def test_menu_hides_on_power_off(application):
    c = Controller()
    menu = MenuView()
    c.press("mode")
    menu.render(c.state)
    assert not menu.isHidden()
    c.press("shift")
    c.press("ac")
    menu.render(c.state)
    assert menu.isHidden()
    menu.close()

