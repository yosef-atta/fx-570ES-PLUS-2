"""Physical key mappings; evaluation of scientific actions is deferred."""
from dataclasses import dataclass
from .action import Action

@dataclass(frozen=True)
class Key:
    id: str
    label: str
    row: int
    column: int
    primary: Action
    shift: Action | None = None
    alpha: Action | None = None
    shift_label: str = ""
    alpha_label: str = ""
    category: str = "scientific"

def make(id: str, label: str, row: int, col: int, *, primary: Action | None = None,
         shift: Action | None = None, alpha: Action | None = None,
         shift_label: str = "", alpha_label: str = "", category: str = "scientific") -> Key:
    return Key(id, label, row, col, primary or Action.deferred(id), shift, alpha, shift_label, alpha_label, category)

I, C, D = Action.insert, Action.command, Action.deferred
KEYS = (
    make("shift", "SHIFT", 0, 0, primary=C("shift"), category="modifier"),
    make("alpha", "ALPHA", 0, 1, primary=C("alpha"), category="modifier"),
    make("left", "◀", 0, 2, primary=C("left"), category="navigation"),
    make("up", "▲", 0, 3, primary=C("up"), category="navigation"),
    make("down", "▼", 0, 4, primary=C("down"), category="navigation"),
    make("right", "▶", 0, 5, primary=C("right"), category="navigation"),
    make("mode", "MODE", 1, 0, primary=C("mode"), shift=C("setup"), shift_label="SETUP", category="control"),
    make("on", "ON", 1, 1, primary=C("on"), category="control"),
    make("calc", "CALC", 1, 2, shift=D("solve"), shift_label="SOLVE"),
    make("integral", "∫", 1, 3, shift=D("derivative"), shift_label="d/dx"),
    make("fraction", "□/□", 1, 4, shift=D("mixed_fraction")),
    make("sqrt", "√", 1, 5, shift=D("cube_root"), shift_label="³√"),
    make("square", "x²", 2, 0, shift=D("cube"), shift_label="x³"),
    make("power", "x^", 2, 1, shift=D("nth_root")),
    make("log", "log", 2, 2, shift=D("ten_power"), shift_label="10ˣ"),
    make("ln", "ln", 2, 3, shift=D("exp"), shift_label="eˣ"),
    make("negative", "(-)", 2, 4, primary=I("−")),
    make("dms", "°′″", 2, 5),
    make("hyp", "hyp", 3, 0),
    make("sin", "sin", 3, 1, shift=D("asin"), shift_label="sin⁻¹"),
    make("cos", "cos", 3, 2, shift=D("acos"), shift_label="cos⁻¹"),
    make("tan", "tan", 3, 3, shift=D("atan"), shift_label="tan⁻¹"),
    make("rcl", "RCL", 3, 4, shift=D("sto"), shift_label="STO"),
    make("eng", "ENG", 3, 5),
    make("lparen", "(", 4, 0, primary=I("(")),
    make("rparen", ")", 4, 1, primary=I(")")),
    make("sd", "S⇔D", 4, 2),
    make("mplus", "M+", 4, 3),
    make("del", "DEL", 4, 4, primary=C("del"), shift=C("insert_toggle"), shift_label="INS", category="control"),
    make("ac", "AC", 4, 5, primary=C("ac"), shift=C("off"), shift_label="OFF", category="control"),
    make("7", "7", 5, 0, primary=I("7"), category="number"),
    make("8", "8", 5, 1, primary=I("8"), category="number"),
    make("9", "9", 5, 2, primary=I("9"), category="number"),
    make("divide", "÷", 5, 3, primary=I("÷"), category="operator"),
    make("percent", "%", 5, 4),
    make("ans", "Ans", 5, 5),
    make("4", "4", 6, 0, primary=I("4"), category="number"),
    make("5", "5", 6, 1, primary=I("5"), category="number"),
    make("6", "6", 6, 2, primary=I("6"), category="number"),
    make("multiply", "×", 6, 3, primary=I("×"), category="operator"),
    make("factorial", "x!", 6, 4),
    make("pi", "π", 6, 5),
    make("1", "1", 7, 0, primary=I("1"), category="number"),
    make("2", "2", 7, 1, primary=I("2"), category="number"),
    make("3", "3", 7, 2, primary=I("3"), category="number"),
    make("subtract", "−", 7, 3, primary=I("−"), category="operator"),
    make("comma", ",", 7, 4, primary=I(",")),
    make("exp10", "×10ˣ", 7, 5),
    make("0", "0", 8, 0, primary=I("0"), category="number"),
    make("dot", ".", 8, 1, primary=I("."), category="number"),
    make("equals", "=", 8, 2, primary=D("evaluate"), category="operator"),
    make("add", "+", 8, 3, primary=I("+"), category="operator"),
    make("reciprocal", "x⁻¹", 8, 4),
    make("random", "Ran#", 8, 5),
)
REGISTRY = {item.id: item for item in KEYS}
if len(REGISTRY) != len(KEYS) or len({(k.row, k.column) for k in KEYS}) != len(KEYS):
    raise ValueError("Duplicate physical key identity or position")

def resolve(key_id: str, modifier: str | None = None) -> Action:
    item = REGISTRY[key_id]
    if modifier == "shift" and item.shift:
        return item.shift
    if modifier == "alpha" and item.alpha:
        return item.alpha
    return item.primary
