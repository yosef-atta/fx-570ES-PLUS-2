"""Original desktop palette and Qt stylesheet."""
STYLESHEET = """
QMainWindow { background: #1e2735; }
QWidget#shell { background: #2a3546; border: 2px solid #111a27; border-radius: 16px; }
QLabel#brand { color: #f2f4f7; font: bold 19px 'Segoe UI'; }
QLabel#subtitle { color: #b6c3d5; font: 10px 'Segoe UI'; }
QFrame#lcd { background: #cbdac7; border: 3px solid #859b8b; border-radius: 7px; }
QLabel#indicators { color: #304b3b; font: 11px 'Consolas'; }
QLabel#expression { color: #17271f; font: 18px 'Consolas'; }
QLabel#result { color: #17271f; font: bold 16px 'Consolas'; }
QPushButton { min-height: 43px; color: #f8fafc; background: #3e5069;
 border: 1px solid #19283a; border-radius: 7px; font: bold 15px 'Segoe UI'; }
QPushButton:hover { background: #526783; }
QPushButton:pressed { background: #8da8c2; }
QPushButton:focus { border: 2px solid #f4bd62; }
QPushButton[category="number"] { background: #f2f3f5; color: #192332; }
QPushButton[category="number"]:hover { background: #dce9f4; }
QPushButton[category="operator"] { background: #dde2e9; color: #152136; }
QPushButton[category="control"] { background: #b85e52; }
QPushButton[category="modifier"] { background: #c5a155; color: #182436; }
QPushButton[category="navigation"] { background: #51677a; }
"""
