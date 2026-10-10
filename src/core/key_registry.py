"""Physical key mappings for fx-570ES PLUS-2 calculator across all 8 modes."""
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
    return Key(id, label, row, col, primary or Action.command(id), shift, alpha, shift_label, alpha_label, category)

I, C = Action.insert, Action.command
KEYS = (
    make("shift", "SHIFT", 0, 0, primary=C("shift"), category="modifier"),
    make("alpha", "ALPHA", 0, 1, primary=C("alpha"), category="modifier"),
    make("left", "◀", 0, 2, primary=C("left"), category="navigation"),
    make("up", "▲", 0, 3, primary=C("up"), category="navigation"),
    make("down", "▼", 0, 4, primary=C("down"), category="navigation"),
    make("right", "▶", 0, 5, primary=C("right"), category="navigation"),
    make("mode", "MODE", 1, 0, primary=C("mode"), shift=C("setup"), shift_label="SETUP", category="control"),
    make("on", "ON", 1, 1, primary=C("on"), category="control"),
    make("calc", "CALC", 1, 2, primary=C("calc"), shift=C("solve"), shift_label="SOLVE", alpha=I("="), alpha_label="="),
    make("integral", "∫", 1, 3, primary=I("∫("), shift=I("d/dx("), shift_label="d/dx", alpha=I(":"), alpha_label=":"),
    make("fraction", "□/□", 1, 4, primary=I("/"), shift=I("mixed/"), shift_label="■□/□"),
    make("sqrt", "√", 1, 5, primary=I("√("), shift=I("³√("), shift_label="³√"),
    make("square", "x²", 2, 0, primary=I("²"), shift=I("³"), shift_label="x³"),
    make("power", "x^", 2, 1, primary=I("^"), shift=I("ˣ√("), shift_label="ˣ√□"),
    make("log", "log", 2, 2, primary=I("log("), shift=I("10ˣ("), shift_label="10ˣ"),
    make("ln", "ln", 2, 3, primary=I("ln("), shift=I("eˣ("), shift_label="eˣ", alpha=I("e"), alpha_label="e"),
    make("negative", "(-)", 2, 4, primary=I("−"), shift=C("arg"), shift_label="arg", alpha=I("A"), alpha_label="A"),
    make("dms", "°′″", 2, 5, primary=I("°"), shift=C("arrow_dms"), shift_label="←", alpha=I("B"), alpha_label="B"),
    make("hyp", "hyp", 3, 0, primary=C("hyp"), shift=C("inv_hyp"), shift_label="hyp⁻¹", alpha=I("C"), alpha_label="C"),
    make("sin", "sin", 3, 1, primary=I("sin("), shift=I("sin⁻¹("), shift_label="sin⁻¹", alpha=I("D"), alpha_label="D"),
    make("cos", "cos", 3, 2, primary=I("cos("), shift=I("cos⁻¹("), shift_label="cos⁻¹", alpha=I("E"), alpha_label="E"),
    make("tan", "tan", 3, 3, primary=I("tan("), shift=I("tan⁻¹("), shift_label="tan⁻¹", alpha=I("F"), alpha_label="F"),
    make("rcl", "RCL", 3, 4, primary=C("rcl"), shift=C("sto"), shift_label="STO"),
    make("eng", "ENG", 3, 5, primary=C("eng"), shift=C("arrow_eng"), shift_label="←", alpha=I("i"), alpha_label="i"),
    make("lparen", "(", 4, 0, primary=I("("), shift=I("Abs("), shift_label="abs"),
    make("rparen", ")", 4, 1, primary=I(")"), shift=I(","), shift_label=",", alpha=I("X"), alpha_label="X"),
    make("sd", "S⇔D", 4, 2, primary=C("sd"), shift=C("mixed_sd"), shift_label="a b/c⇔d/c", alpha=I("Y"), alpha_label="Y"),
    make("mplus", "M+", 4, 3, primary=C("mplus"), shift=C("mminus"), shift_label="M−", alpha=I("M"), alpha_label="M"),
    make("del", "DEL", 4, 4, primary=C("del"), shift=C("insert_toggle"), shift_label="INS", category="control"),
    make("ac", "AC", 4, 5, primary=C("ac"), shift=C("off"), shift_label="OFF", category="control"),
    make("7", "7", 5, 0, primary=I("7"), shift=C("const"), shift_label="CONST", category="number"),
    make("8", "8", 5, 1, primary=I("8"), shift=C("conv"), shift_label="CONV", category="number"),
    make("9", "9", 5, 2, primary=I("9"), shift=C("clr"), shift_label="CLR", category="number"),
    make("divide", "÷", 5, 3, primary=I("÷"), shift=I("Pol("), shift_label="Pol", category="operator"),
    make("percent", "%", 5, 4, primary=I("%")),
    make("ans", "Ans", 5, 5, primary=I("Ans"), shift=I("%"), shift_label="%", alpha=I("PreAns"), alpha_label="PreAns"),
    make("4", "4", 6, 0, primary=I("4"), shift=C("matrix_menu"), shift_label="MATRIX", category="number"),
    make("5", "5", 6, 1, primary=I("5"), shift=C("vector_menu"), shift_label="VECTOR", category="number"),
    make("6", "6", 6, 2, primary=I("6"), category="number"),
    make("multiply", "×", 6, 3, primary=I("×"), shift=I("Rec("), shift_label="Rec", category="operator"),
    make("factorial", "x!", 6, 4, primary=I("!"), shift=I("!")),
    make("pi", "π", 6, 5, primary=I("π")),
    make("1", "1", 7, 0, primary=I("1"), shift=C("stat_menu"), shift_label="STAT", category="number"),
    make("2", "2", 7, 1, primary=I("2"), shift=C("cmplx_menu"), shift_label="CMPLX", category="number"),
    make("3", "3", 7, 2, primary=I("3"), shift=C("base_menu"), shift_label="BASE", category="number"),
    make("subtract", "−", 7, 3, primary=I("−"), shift=I("nPr"), shift_label="nPr", category="operator"),
    make("comma", ",", 7, 4, primary=I(",")),
    make("exp10", "×10ˣ", 7, 5, primary=I("×10^"), shift=I("π"), shift_label="π", alpha=I("e"), alpha_label="e"),
    make("0", "0", 8, 0, primary=I("0"), shift=I("Rnd("), shift_label="Rnd", category="number"),
    make("dot", ".", 8, 1, primary=I("."), shift=I("RanInt#("), shift_label="RanInt#", category="number"),
    make("equals", "=", 8, 2, primary=C("evaluate"), category="operator"),
    make("add", "+", 8, 3, primary=I("+"), shift=I("nCr"), shift_label="nCr", category="operator"),
    make("reciprocal", "x⁻¹", 8, 4, primary=I("⁻¹"), shift=I("!"), shift_label="x!"),
    make("random", "Ran#", 8, 5, primary=I("Ran#")),
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
