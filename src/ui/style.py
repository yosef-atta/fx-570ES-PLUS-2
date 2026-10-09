STYLESHEET = """
QMainWindow { background: #1a222d; }
QWidget#shell { background: #242f3e; border: 2px solid #101721; border-radius: 16px; }
QLabel#brand { color: #f2f4f7; font: bold 19px 'Segoe UI'; }
QLabel#subtitle { color: #8e9fad; font: 10px 'Segoe UI'; letter-spacing: 1px; }

QFrame#lcd { background: #cbdac7; border: 3px solid #859b8b; border-radius: 8px; }
QFrame#lcd[power="off"] { background: #18201a; border: 3px solid #222c24; }

QLabel#indicators { color: #2d4536; font: bold 11px 'Consolas'; }
QLabel#expression { color: #17271f; font: 20px 'Consolas'; }
QLabel#result { color: #17271f; font: bold 22px 'Consolas'; }
QLabel#menu_heading { color: #203528; font: bold 12px 'Consolas'; }
QLabel#menu_options { color: #17271f; font: 12px 'Consolas'; }

QPushButton {
    min-height: 44px;
    background: #39475c;
    border: 1px solid #1d2735;
    border-radius: 7px;
    padding: 0;
}
QPushButton:hover { background: #4c5d75; }
QPushButton:pressed { background: #6b82a3; }
QPushButton:focus { border: 2px solid #f4bd62; }

QLabel#shift_sublabel {
    color: #e5a93c;
    font: bold 9px 'Segoe UI';
    background: transparent;
}
QLabel#alpha_sublabel {
    color: #e05555;
    font: bold 9px 'Segoe UI';
    background: transparent;
}
QLabel#main_key_label {
    font: bold 13px 'Segoe UI';
    color: #f8fafc;
    background: transparent;
}

QPushButton[category="number"] { background: #edf0f4; border-color: #bac4d0; }
QPushButton[category="number"]:hover { background: #dce3ec; }
QPushButton[category="number"] QLabel#main_key_label { color: #111a24; font-size: 15px; }

QPushButton[category="operator"] { background: #d5dde8; border-color: #a6b5c7; }
QPushButton[category="operator"]:hover { background: #c5d0de; }
QPushButton[category="operator"] QLabel#main_key_label { color: #111a24; font-size: 14px; }

QPushButton[category="control"] { background: #4a576b; }
QPushButton[category="modifier"] { background: #4a576b; }
QPushButton[category="navigation"] { background: #47586e; }

QPushButton#key_shift { background: #d4a017; border-color: #a3780a; }
QPushButton#key_shift:hover { background: #e0ab20; }
QPushButton#key_shift QLabel#main_key_label { color: #141b24; }

QPushButton#key_alpha { background: #c73852; border-color: #9c2339; }
QPushButton#key_alpha:hover { background: #d6435d; }
QPushButton#key_alpha QLabel#main_key_label { color: #ffffff; }

QPushButton#key_del, QPushButton#key_ac { background: #b8493d; border-color: #8c3228; }
QPushButton#key_del:hover, QPushButton#key_ac:hover { background: #c75346; }
QPushButton#key_del QLabel#main_key_label, QPushButton#key_ac QLabel#main_key_label { color: #ffffff; }

QPushButton#key_on, QPushButton#key_mode { background: #435266; }
"""

