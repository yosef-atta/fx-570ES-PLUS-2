from src.core.action import Kind
from src.core.key_registry import KEYS, REGISTRY, resolve

def test_unique_positions_and_ids():
    assert len(KEYS) == len(REGISTRY)
    assert len({(k.row, k.column) for k in KEYS}) == len(KEYS)

def test_shift_setup_and_off():
    assert resolve("mode", "shift").name == "setup"
    assert resolve("ac", "shift").name == "off"

def test_numeric_keys_insert():
    for digit in "0123456789":
        action = resolve(digit)
        assert action.kind is Kind.INSERT and action.text == digit

def test_scientific_actions_are_explicitly_deferred():
    assert resolve("sin").kind is Kind.DEFERRED
    assert resolve("equals").name == "evaluate"
