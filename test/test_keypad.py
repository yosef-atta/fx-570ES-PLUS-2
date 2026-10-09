from src.core.key_registry import REGISTRY
from src.ui.keypad import Keypad

def test_all_registry_keys_render(application):
    widget = Keypad()
    assert set(widget.buttons) == set(REGISTRY)
    widget.close()

def test_click_emits_physical_key(application):
    widget = Keypad()
    observed = []
    widget.triggered.connect(observed.append)
    widget.buttons["7"].click()
    assert observed == ["7"]
    widget.close()

def test_button_sublabels_and_tooltips(application):
    widget = Keypad()
    mode_btn = widget.buttons["mode"]
    assert mode_btn.shift_lbl.text() == "SETUP"
    assert "SETUP" in mode_btn.toolTip()

    sin_btn = widget.buttons["sin"]
    assert sin_btn.shift_lbl.text() == "sin⁻¹"
    assert sin_btn.alpha_lbl.text() == "D"

    ac_btn = widget.buttons["ac"]
    assert ac_btn.shift_lbl.text() == "OFF"
    widget.close()

def test_sequential_clicks(application):
    widget = Keypad()
    clicked = []
    widget.triggered.connect(clicked.append)
    for key_id in ("1", "add", "2", "equals"):
        widget.buttons[key_id].click()
    assert clicked == ["1", "add", "2", "equals"]
    widget.close()

