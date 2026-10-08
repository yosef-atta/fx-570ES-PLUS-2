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
