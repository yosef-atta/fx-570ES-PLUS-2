"""Authentic design system replicating the physical Casio fx-570ES PLUS 2nd Edition."""

STYLESHEET = """
QMainWindow {
    background: #0d0e11;
}

QWidget#shell {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #25272e, stop:0.04 #1c1d22, stop:0.96 #16171b, stop:1 #111215);
    border: 2px solid #2d3039;
    border-radius: 36px;
}

/* -------------------------------------------------------------
 * Authentic Top Branding
 * ------------------------------------------------------------- */
QLabel#brand_casio {
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 21px;
    font-weight: 900;
    letter-spacing: 2px;
    background: transparent;
}

QLabel#brand_model {
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 1px;
    background: transparent;
}

QLabel#brand_vpam {
    color: #c9cfdc;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 11px;
    font-weight: bold;
    font-style: italic;
    letter-spacing: 1.5px;
    background: transparent;
}

QLabel#brand_edition {
    color: #9da3b2;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10px;
    background: transparent;
}

/* -------------------------------------------------------------
 * Recessed LCD Screen Frame & Dot-Matrix Display
 * ------------------------------------------------------------- */
QFrame#lcd_frame {
    background: #111215;
    border: 2px solid #23252b;
    border-radius: 12px;
}

QFrame#lcd {
    background: #c2ceb8;
    border: 1px solid #9aa890;
    border-radius: 6px;
}

QFrame#lcd[power="off"] {
    background: #161a16;
    border: 1px solid #202620;
}

QLabel#indicators {
    color: #17271f;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 11px;
    font-weight: bold;
    background: transparent;
}

QLabel#expression {
    color: #17271f;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 20px;
    background: transparent;
}

QLabel#result {
    color: #17271f;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 22px;
    font-weight: bold;
    background: transparent;
}

QLabel#menu_heading {
    color: #1c2e23;
    font-family: 'Consolas', monospace;
    font-size: 12px;
    font-weight: bold;
    background: transparent;
}

QLabel#menu_options {
    color: #17271f;
    font-family: 'Consolas', monospace;
    font-size: 12px;
    background: transparent;
}

/* -------------------------------------------------------------
 * Button Base & Scientific Tier
 * ------------------------------------------------------------- */
QPushButton {
    min-height: 34px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #383a42, stop:1 #28292f);
    border: 1px solid #1f2025;
    border-bottom: 2px solid #16171b;
    border-radius: 6px;
    padding: 0;
}

QPushButton:hover {
    background: #464853;
}

QPushButton:pressed {
    background: #1f2025;
    border-bottom: 1px solid #16171b;
}

QPushButton:focus {
    outline: none;
}

/* Sub-labels */
QLabel#shift_sublabel {
    color: #e5a93c;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 9px;
    font-weight: bold;
    background: transparent;
}

QLabel#alpha_sublabel {
    color: #e05375;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 9px;
    font-weight: bold;
    background: transparent;
}

QLabel#base_sublabel {
    color: #00a3e0;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 8px;
    font-weight: bold;
    background: transparent;
}

QLabel#main_key_label {
    color: #f2f4f8;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    font-weight: bold;
    background: transparent;
}

/* -------------------------------------------------------------
 * Top Cluster: Oval Buttons (SHIFT, ALPHA, MODE, ON)
 * ------------------------------------------------------------- */
QPushButton[shape="oval"] {
    min-width: 44px;
    min-height: 28px;
    max-height: 28px;
    border-radius: 14px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3c3e46, stop:1 #26272d);
    border: 1px solid #484b55;
    border-bottom: 2px solid #1a1b20;
}

QPushButton[shape="oval"]:hover {
    background: #4c4f5a;
}

QPushButton[shape="oval"]:pressed {
    background: #1f2025;
}

/* Top oval key special colors for main labels */
QPushButton#key_shift QLabel#main_key_label {
    color: #f0f2f6;
    font-size: 11px;
}
QPushButton#key_alpha QLabel#main_key_label {
    color: #f0f2f6;
    font-size: 11px;
}
QPushButton#key_mode QLabel#main_key_label {
    color: #f0f2f6;
    font-size: 11px;
}
QPushButton#key_on QLabel#main_key_label {
    color: #f0f2f6;
    font-size: 11px;
}

/* -------------------------------------------------------------
 * Top Center: Circular REPLAY D-Pad
 * ------------------------------------------------------------- */
QFrame#replay_pad {
    background: qradialgradient(cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 #363943, stop:0.75 #24262d, stop:1 #191a20);
    border: 2px solid #3c3f4a;
    border-radius: 39px;
}

QLabel#replay_center_label {
    color: #8c93a4;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 7px;
    font-weight: bold;
    letter-spacing: 1px;
    background: transparent;
}

QPushButton[shape="dpad"] {
    min-width: 26px;
    max-width: 28px;
    min-height: 20px;
    max-height: 22px;
    background: #2f3139;
    border: 1px solid #23242a;
    border-radius: 5px;
}

QPushButton[shape="dpad"]:hover {
    background: #444753;
}

QPushButton[shape="dpad"]:pressed {
    background: #1c1d22;
}

QPushButton[shape="dpad"] QLabel#main_key_label {
    color: #ffffff;
    font-size: 10px;
    font-weight: bold;
}

/* -------------------------------------------------------------
 * Number & Input Tier (Crisp Light Keys)
 * ------------------------------------------------------------- */
QPushButton[is_number="true"],
QPushButton#key_dot,
QPushButton#key_exp10,
QPushButton#key_ans,
QPushButton#key_equals {
    min-height: 38px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:0.08 #f5f6f9, stop:1 #e2e4ea);
    border: 1px solid #b4b8c4;
    border-bottom: 2px solid #9fa4b2;
    border-radius: 7px;
}

QPushButton[is_number="true"]:hover,
QPushButton#key_dot:hover,
QPushButton#key_exp10:hover,
QPushButton#key_ans:hover,
QPushButton#key_equals:hover {
    background: #ffffff;
}

QPushButton[is_number="true"]:pressed,
QPushButton#key_dot:pressed,
QPushButton#key_exp10:pressed,
QPushButton#key_ans:pressed,
QPushButton#key_equals:pressed {
    background: #d4d7e0;
    border-bottom: 1px solid #b4b8c4;
}

QPushButton[is_number="true"] QLabel#main_key_label,
QPushButton#key_dot QLabel#main_key_label,
QPushButton#key_exp10 QLabel#main_key_label,
QPushButton#key_ans QLabel#main_key_label,
QPushButton#key_equals QLabel#main_key_label {
    color: #111317;
    font-size: 16px;
    font-weight: bold;
}

/* Arithmetic Operators */
QPushButton#key_multiply,
QPushButton#key_divide,
QPushButton#key_add,
QPushButton#key_subtract {
    min-height: 38px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f2f3f7, stop:1 #d8dbe2);
    border: 1px solid #acb1be;
    border-bottom: 2px solid #969ba8;
    border-radius: 7px;
}

QPushButton#key_multiply:hover,
QPushButton#key_divide:hover,
QPushButton#key_add:hover,
QPushButton#key_subtract:hover {
    background: #ffffff;
}

QPushButton#key_multiply:pressed,
QPushButton#key_divide:pressed,
QPushButton#key_add:pressed,
QPushButton#key_subtract:pressed {
    background: #caced8;
    border-bottom: 1px solid #acb1be;
}

QPushButton#key_multiply QLabel#main_key_label,
QPushButton#key_divide QLabel#main_key_label,
QPushButton#key_add QLabel#main_key_label,
QPushButton#key_subtract QLabel#main_key_label {
    color: #111317;
    font-size: 16px;
    font-weight: bold;
}

/* -------------------------------------------------------------
 * DEL & AC: Vibrant Casio Lime Green
 * ------------------------------------------------------------- */
QPushButton#key_del,
QPushButton#key_ac {
    min-height: 38px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #86bb32, stop:1 #6b9c24);
    border: 1px solid #547c1a;
    border-bottom: 2px solid #436414;
    border-radius: 7px;
}

QPushButton#key_del:hover,
QPushButton#key_ac:hover {
    background: #94cc39;
}

QPushButton#key_del:pressed,
QPushButton#key_ac:pressed {
    background: #58821c;
    border-bottom: 1px solid #547c1a;
}

QPushButton#key_del QLabel#main_key_label,
QPushButton#key_ac QLabel#main_key_label {
    color: #ffffff;
    font-size: 15px;
    font-weight: bold;
}
"""
