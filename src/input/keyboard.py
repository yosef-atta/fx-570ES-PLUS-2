"""Translate Qt key events to registry identities."""
from PySide6.QtCore import Qt

KEYS = {
    Qt.Key.Key_Return: "equals", Qt.Key.Key_Enter: "equals",
    Qt.Key.Key_Backspace: "del", Qt.Key.Key_Delete: "del",
    Qt.Key.Key_Escape: "ac", Qt.Key.Key_Left: "left",
    Qt.Key.Key_Right: "right", Qt.Key.Key_Up: "up",
    Qt.Key.Key_Down: "down", Qt.Key.Key_F2: "shift",
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

def key_to_id(event) -> str | None:
    if event.key() == Qt.Key.Key_F5:
        return "setup_shortcut"
    if event.key() in KEYS:
        return KEYS[event.key()]
    text = event.text()
    if text in "0123456789" and len(text) == 1:
        return text
    return CHARACTERS.get(text)
