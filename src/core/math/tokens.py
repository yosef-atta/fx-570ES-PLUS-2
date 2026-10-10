"""Token definitions and data models for mathematical expressions."""
from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    # Literals & Identifiers
    NUMBER = auto()
    VARIABLE = auto()        # A, B, C, D, E, F, X, Y, M
    ANS = auto()             # Ans
    PREANS = auto()          # PreAns
    PI = auto()              # π
    E_CONST = auto()         # e (mathematical constant 2.718...)

    # Operators
    PLUS = auto()            # +
    MINUS = auto()           # - / −
    NEG = auto()             # Unary negation (−)
    MULTIPLY = auto()        # × / *
    DIVIDE = auto()          # ÷ / /
    POWER = auto()           # ^, x² (as ^2), x³ (as ^3)
    RECIPROCAL = auto()      # x⁻¹ (as ^-1)
    PERCENT = auto()         # %
    FACTORIAL = auto()       # !
    NPR = auto()             # nPr (permutation)
    NCR = auto()             # nCr (combination)
    EXP10 = auto()           # ×10ˣ or E

    # Fractions
    FRACTION = auto()        # fraction bar /
    MIXED_FRACTION = auto()  # mixed fraction separator

    # Delimiters & Punctuation
    LPAREN = auto()          # (
    RPAREN = auto()          # )
    COMMA = auto()           # ,
    COLON = auto()           # : (multi-statement separator)
    EQUALS = auto()          # = (relational equality in SOLVE)
    DMS = auto()             # ° ' " symbol

    # Functions
    SIN = auto()
    COS = auto()
    TAN = auto()
    ASIN = auto()
    ACOS = auto()
    ATAN = auto()
    SINH = auto()
    COSH = auto()
    TANH = auto()
    ASINH = auto()
    ACOSH = auto()
    ATANH = auto()
    LOG = auto()             # log (base 10) or log(base, value)
    LN = auto()              # ln (natural log)
    EXP = auto()             # e^x
    TEN_POW = auto()         # 10^x
    SQRT = auto()            # √
    CBRT = auto()            # ³√
    NTH_ROOT = auto()        # ˣ√□
    ABS = auto()             # Abs
    RND = auto()             # Rnd
    RAN_INT = auto()         # RanInt#
    RAN_HASH = auto()        # Ran#
    POL = auto()             # Pol
    REC = auto()             # Rec
    DERIVATIVE = auto()      # d/dx
    INTEGRAL = auto()        # ∫
    SUMMATION = auto()       # Σ

    # End of Input
    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: str
    position: int            # Starting character position in source string
    length: int = 1          # Length of the matched token in characters

    @property
    def end_position(self) -> int:
        return self.position + self.length
