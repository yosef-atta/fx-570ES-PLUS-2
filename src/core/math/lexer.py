"""Lexer for mathematical expressions with implicit multiplication handling."""
import re
from .errors import SyntaxError
from .tokens import Token, TokenType

# Keyword and multi-character function map
KEYWORDS: list[tuple[str, TokenType]] = [
    # Multi-statement and relations
    (":", TokenType.COLON),
    ("=", TokenType.EQUALS),
    (",", TokenType.COMMA),

    # Powers & Special postfix
    ("×10^", TokenType.EXP10),
    ("x10^", TokenType.EXP10),
    ("×10", TokenType.EXP10),
    ("x10", TokenType.EXP10),
    ("²", TokenType.POWER),
    ("³", TokenType.POWER),
    ("⁻¹", TokenType.RECIPROCAL),
    ("x⁻¹", TokenType.RECIPROCAL),
    ("x²", TokenType.POWER),
    ("x³", TokenType.POWER),
    ("x!", TokenType.FACTORIAL),
    ("!", TokenType.FACTORIAL),
    ("%", TokenType.PERCENT),
    ("°′″", TokenType.DMS),
    ("°'\"", TokenType.DMS),
    ("°", TokenType.DMS),

    # Mixed Fraction & Fraction Separators
    ("mixed/", TokenType.MIXED_FRACTION),
    ("mixed", TokenType.MIXED_FRACTION),
    ("⌟", TokenType.MIXED_FRACTION),
    ("┘", TokenType.MIXED_FRACTION),
    ("_", TokenType.MIXED_FRACTION),

    # Calculus & Special
    ("d/dx", TokenType.DERIVATIVE),
    ("∫", TokenType.INTEGRAL),
    ("Σ", TokenType.SUMMATION),
    ("³√", TokenType.CBRT),
    ("ˣ√", TokenType.NTH_ROOT),
    ("√", TokenType.SQRT),
    ("sqrt", TokenType.SQRT),
    ("cbrt", TokenType.CBRT),

    # Inverse Hyperbolic
    ("sinh⁻¹", TokenType.ASINH),
    ("cosh⁻¹", TokenType.ACOSH),
    ("tanh⁻¹", TokenType.ATANH),
    ("asinh", TokenType.ASINH),
    ("acosh", TokenType.ACOSH),
    ("atanh", TokenType.ATANH),

    # Hyperbolic
    ("sinh", TokenType.SINH),
    ("cosh", TokenType.COSH),
    ("tanh", TokenType.TANH),

    # Inverse Trig
    ("sin⁻¹", TokenType.ASIN),
    ("cos⁻¹", TokenType.ACOS),
    ("tan⁻¹", TokenType.ATAN),
    ("asin", TokenType.ASIN),
    ("acos", TokenType.ACOS),
    ("atan", TokenType.ATAN),

    # Trig
    ("sin", TokenType.SIN),
    ("cos", TokenType.COS),
    ("tan", TokenType.TAN),

    # Logarithms & Exponential
    ("log", TokenType.LOG),
    ("ln", TokenType.LN),
    ("10ˣ", TokenType.TEN_POW),
    ("eˣ", TokenType.EXP),

    # General Functions & Memory
    ("RanInt#", TokenType.RAN_INT),
    ("RanInt", TokenType.RAN_INT),
    ("Ran#", TokenType.RAN_HASH),
    ("Ran", TokenType.RAN_HASH),
    ("Rnd", TokenType.RND),
    ("Abs", TokenType.ABS),
    ("abs", TokenType.ABS),
    ("Pol", TokenType.POL),
    ("pol", TokenType.POL),
    ("Rec", TokenType.REC),
    ("rec", TokenType.REC),
    ("PreAns", TokenType.PREANS),
    ("Ans", TokenType.ANS),

    # Combinatorics
    ("nPr", TokenType.NPR),
    ("nCr", TokenType.NCR),
    ("P", TokenType.NPR),
    ("C", TokenType.NCR),

    # Complex functions & Angle
    ("arg", TokenType.ARG),
    ("Conjg", TokenType.CONJG),
    ("conjg", TokenType.CONJG),
    ("∠", TokenType.ANGLE),

    # Constants
    ("π", TokenType.PI),
    ("pi", TokenType.PI),

    # Arithmetic
    ("+", TokenType.PLUS),
    ("−", TokenType.MINUS),   # U+2212 minus
    ("-", TokenType.MINUS),   # ASCII hyphen
    ("×", TokenType.MULTIPLY),# U+00D7
    ("*", TokenType.MULTIPLY),
    ("÷", TokenType.DIVIDE),  # U+00F7
    ("/", TokenType.DIVIDE),
    ("^", TokenType.POWER),
    ("(", TokenType.LPAREN),
    (")", TokenType.RPAREN),
]
# Sort keywords by length descending so longer tokens take precedence (e.g. Conjg before C)
KEYWORDS.sort(key=lambda p: len(p[0]), reverse=True)

# Variables: single letters
VARIABLES = {"A", "B", "C", "D", "E", "F", "X", "Y", "M"}


class Lexer:
    """Scans raw expression strings into a stream of typed Tokens."""

    def __init__(self, text: str):
        self.text = text
        self.length = len(text)
        self.pos = 0

    def tokenize(self) -> list[Token]:
        raw_tokens: list[Token] = []

        while self.pos < self.length:
            ch = self.text[self.pos]

            # 1. Skip whitespace
            if ch.isspace():
                self.pos += 1
                continue

            # 2. Match number (ASCII digits 0-9 and decimal point)
            if ("0" <= ch <= "9") or (ch == "." and self._peek_digit()):
                token = self._read_number()
                raw_tokens.append(token)
                continue

            # 3. Check for Casio negation symbol `(−)`
            if ch == "−" or ch == "-":
                # Check if this minus should be a unary negation
                # If at start of input, or after an operator, open paren, comma, colon
                is_unary = False
                if not raw_tokens or raw_tokens[-1].type in (
                    TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE,
                    TokenType.POWER, TokenType.LPAREN, TokenType.COMMA, TokenType.COLON,
                    TokenType.EQUALS, TokenType.NEG
                ):
                    is_unary = True

                start = self.pos
                self.pos += 1
                if is_unary:
                    raw_tokens.append(Token(TokenType.NEG, "−", start, 1))
                else:
                    raw_tokens.append(Token(TokenType.MINUS, "-", start, 1))
                continue

            # 4. Check multi-character keywords and symbols
            matched = False
            for pattern, token_type in KEYWORDS:
                if self.text.startswith(pattern, self.pos):
                    start = self.pos
                    length = len(pattern)
                    self.pos += length
                    # For superscript symbols like ², translate value
                    val = pattern
                    if pattern in ("²", "x²"):
                        # Represents power of 2
                        raw_tokens.append(Token(TokenType.POWER, "^", start, length))
                        raw_tokens.append(Token(TokenType.NUMBER, "2", start, length))
                        matched = True
                        break
                    elif pattern in ("³", "x³"):
                        # Represents power of 3
                        raw_tokens.append(Token(TokenType.POWER, "^", start, length))
                        raw_tokens.append(Token(TokenType.NUMBER, "3", start, length))
                        matched = True
                        break
                    elif pattern in ("⁻¹", "x⁻¹"):
                        # Represents power of -1
                        raw_tokens.append(Token(TokenType.POWER, "^", start, length))
                        raw_tokens.append(Token(TokenType.LPAREN, "(", start, length))
                        raw_tokens.append(Token(TokenType.NEG, "−", start, length))
                        raw_tokens.append(Token(TokenType.NUMBER, "1", start, length))
                        raw_tokens.append(Token(TokenType.RPAREN, ")", start, length))
                        matched = True
                        break

                    raw_tokens.append(Token(token_type, val, start, length))
                    matched = True
                    break

            if matched:
                continue

            # 5. Check variable letters
            if ch in VARIABLES:
                start = self.pos
                self.pos += 1
                raw_tokens.append(Token(TokenType.VARIABLE, ch, start, 1))
                continue

            # 6. Check constant e (lowercase e when not followed by other letters)
            if ch == "e":
                start = self.pos
                self.pos += 1
                raw_tokens.append(Token(TokenType.E_CONST, "e", start, 1))
                continue

            # 7. Check imaginary unit i
            if ch == "i":
                start = self.pos
                self.pos += 1
                raw_tokens.append(Token(TokenType.I_IMAG, "i", start, 1))
                continue

            # 8. Unrecognized character
            raise SyntaxError(f"Unexpected character '{ch}'", position=self.pos)

        # Add EOF token
        raw_tokens.append(Token(TokenType.EOF, "", self.pos, 0))

        # Insert implicit multiplications
        return self._insert_implicit_multiplication(raw_tokens)

    def _peek_digit(self) -> bool:
        return self.pos + 1 < self.length and ("0" <= self.text[self.pos + 1] <= "9")

    def _read_number(self) -> Token:
        start = self.pos
        has_dot = False

        while self.pos < self.length:
            ch = self.text[self.pos]
            if "0" <= ch <= "9":
                self.pos += 1
            elif ch == "." and not has_dot:
                has_dot = True
                self.pos += 1
            else:
                break

        val = self.text[start:self.pos]
        return Token(TokenType.NUMBER, val, start, self.pos - start)

    def _insert_implicit_multiplication(self, tokens: list[Token]) -> list[Token]:
        """Injects multiplication operators where Casio rules specify implicit multiplication."""
        if len(tokens) <= 1:
            return tokens

        result: list[Token] = []

        # Tokens that can serve as the left operand of implicit multiplication
        left_tokens = (
            TokenType.NUMBER,
            TokenType.VARIABLE,
            TokenType.CONSTANT if hasattr(TokenType, "CONSTANT") else None,
            TokenType.PI,
            TokenType.E_CONST,
            TokenType.I_IMAG,
            TokenType.ANS,
            TokenType.PREANS,
            TokenType.RPAREN,
            TokenType.PERCENT,
            TokenType.FACTORIAL,
            TokenType.DMS,
            TokenType.RAN_HASH,
        )

        # Tokens that can serve as the right operand of implicit multiplication
        right_tokens = (
            TokenType.VARIABLE,
            TokenType.PI,
            TokenType.E_CONST,
            TokenType.I_IMAG,
            TokenType.ANS,
            TokenType.PREANS,
            TokenType.LPAREN,
            TokenType.SQRT,
            TokenType.CBRT,
            TokenType.NTH_ROOT,
            TokenType.SIN,
            TokenType.COS,
            TokenType.TAN,
            TokenType.ASIN,
            TokenType.ACOS,
            TokenType.ATAN,
            TokenType.SINH,
            TokenType.COSH,
            TokenType.TANH,
            TokenType.ASINH,
            TokenType.ACOSH,
            TokenType.ATANH,
            TokenType.LOG,
            TokenType.LN,
            TokenType.ABS,
            TokenType.POL,
            TokenType.REC,
            TokenType.DERIVATIVE,
            TokenType.INTEGRAL,
            TokenType.SUMMATION,
            TokenType.RAN_HASH,
            TokenType.RAN_INT,
        )

        for i in range(len(tokens) - 1):
            curr = tokens[i]
            nxt = tokens[i + 1]
            result.append(curr)

            # Check if implicit multiplication applies
            if curr.type in left_tokens and nxt.type in right_tokens:
                # e.g., 2π, 2(3), (2)(3), 2sin(30), 3X
                result.append(Token(TokenType.MULTIPLY, "×", curr.end_position, 0))
            elif curr.type == TokenType.RPAREN and nxt.type == TokenType.NUMBER:
                # e.g. (2)3 -> (2)*3
                result.append(Token(TokenType.MULTIPLY, "×", curr.end_position, 0))
            elif (curr.type in (TokenType.PI, TokenType.E_CONST, TokenType.VARIABLE)) and nxt.type == TokenType.NUMBER:
                # e.g. π 3 -> π * 3
                result.append(Token(TokenType.MULTIPLY, "×", curr.end_position, 0))

        result.append(tokens[-1])  # Append EOF
        return result
