from src.core.action import Kind
from src.core.key_registry import KEYS, REGISTRY, resolve

def test_unique_positions_and_ids():
    assert len(KEYS) == len(REGISTRY)
    assert len({(k.row, k.column) for k in KEYS}) == len(KEYS)

def test_shift_setup_and_off():
    assert resolve("mode", "shift").name == "setup"
    assert resolve("ac", "shift").name == "off"
    assert resolve("del", "shift").name == "insert_toggle"

def test_numeric_keys_insert():
    for digit in "0123456789":
        action = resolve(digit)
        assert action.kind is Kind.INSERT and action.text == digit

def test_scientific_actions_are_explicitly_deferred():
    assert resolve("sin").kind is Kind.DEFERRED
    assert resolve("equals").name == "evaluate"
    assert resolve("cos").kind is Kind.DEFERRED
    assert resolve("sqrt").kind is Kind.DEFERRED

def test_alpha_variable_mappings():
    alpha_vars = {
        "negative": "A",
        "dms": "B",
        "hyp": "C",
        "sin": "D",
        "cos": "E",
        "tan": "F",
        "rparen": "X",
        "sd": "Y",
        "mplus": "M",
    }
    for key_id, expected_char in alpha_vars.items():
        act = resolve(key_id, "alpha")
        assert act.kind is Kind.INSERT
        assert act.text == expected_char

def test_modifier_fallback_to_primary():
    # If a key does not define a shift function, it falls back to primary
    action = resolve("7", "alpha")
    assert action.kind is Kind.INSERT and action.text == "7"

def test_all_keys_have_valid_actions():
    for key in KEYS:
        assert key.id in REGISTRY
        assert key.primary is not None
        assert key.category in ("number", "operator", "control", "modifier", "navigation", "scientific")

