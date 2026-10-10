"""Translate Qt key events to registry identities with configurable shortcut overrides."""
from PySide6.QtCore import Qt

KEYS = {
    Qt.Key.Key_Return: "equals", Qt.Key.Key_Enter: "equals",
    Qt.Key.Key_Backspace: "del", Qt.Key.Key_Delete: "del",
    Qt.Key.Key_Escape: "ac", Qt.Key.Key_Left: "left",
    Qt.Key.Key_Right: "right", Qt.Key.Key_Up: "up",
    Qt.Key.Key_Down: "down", Qt.Key.Key_Home: "home",
    Qt.Key.Key_End: "end", Qt.Key.Key_F2: "shift",
    Qt.Key.Key_F3: "alpha", Qt.Key.Key_F4: "mode",
    Qt.Key.Key_Plus: "add", Qt.Key.Key_Minus: "subtract",
    Qt.Key.Key_Asterisk: "multiply", Qt.Key.Key_Slash: "divide",
    Qt.Key.Key_Period: "dot", Qt.Key.Key_Comma: "comma",
    Qt.Key.Key_Equal: "equals",
}

CHARACTERS = {
    "+": "add", "-": "subtract", "*": "multiply", "/": "divide",
    ".": "dot", ",": "comma", "(": "lparen", ")": "rparen",
    "=": "equals", "^": "power", "%": "percent", "!": "factorial",
    "x": "multiply", "X": "multiply",
    "s": "sin", "c": "cos", "t": "tan", "l": "ln", "r": "sqrt",
    "i": "eng", "p": "pi",
}

# Configurable user shortcut overrides
CUSTOM_SHORTCUTS: dict[str, str] = {}


def register_custom_shortcut(key_or_char: str, key_id: str) -> None:
    """Registers or overrides a keyboard shortcut."""
    CUSTOM_SHORTCUTS[key_or_char] = key_id


def clear_custom_shortcuts() -> None:
    """Clears all custom shortcuts, restoring default mappings."""
    CUSTOM_SHORTCUTS.clear()


def key_to_id(event) -> str | None:
    """Translates a QKeyEvent into a calculator key identifier."""
    if event.key() == Qt.Key.Key_F5:
        return "setup_shortcut"

    text = event.text()

    # Check custom user shortcuts first
    if text and text in CUSTOM_SHORTCUTS:
        return CUSTOM_SHORTCUTS[text]
    key_name = str(event.key())
    if key_name in CUSTOM_SHORTCUTS:
        return CUSTOM_SHORTCUTS[key_name]

    if event.key() in KEYS:
        return KEYS[event.key()]

    if text in "0123456789" and len(text) == 1:
        return text

    return CHARACTERS.get(text)
