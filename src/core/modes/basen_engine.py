"""Base-N mode engine supporting DEC, HEX, BIN, OCT and 32-bit bitwise logic."""
from src.core.math.errors import MathError, SyntaxError

MASK_32 = 0xFFFFFFFF
SIGN_32 = 0x80000000

class BaseNEngine:
    """Handles 32-bit signed integer calculations, base conversions, and logical operations."""

    def __init__(self, current_base: str = "DEC"):
        self.current_base = current_base  # "DEC", "HEX", "BIN", "OCT"

    def parse_value(self, val_str: str, base_override: str | None = None) -> int:
        """Parses a string token into a 32-bit signed integer."""
        s = val_str.strip()
        b = base_override or self.current_base

        # Check prefix override (e.g. d10, hFF, b1010, o77)
        if len(s) > 1 and s[0] in ("d", "h", "b", "o"):
            prefix = s[0]
            s = s[1:]
            if prefix == "d":
                b = "DEC"
            elif prefix == "h":
                b = "HEX"
            elif prefix == "b":
                b = "BIN"
            elif prefix == "o":
                b = "OCT"

        try:
            if b == "DEC":
                val = int(s, 10)
            elif b == "HEX":
                val = int(s, 16)
            elif b == "BIN":
                val = int(s, 2)
            elif b == "OCT":
                val = int(s, 8)
            else:
                raise SyntaxError(f"BASE-N: unknown base {b}")
        except ValueError:
            raise SyntaxError(f"BASE-N: invalid value '{val_str}' for base {b}")

        # Convert to signed 32-bit
        val &= MASK_32
        if val & SIGN_32:
            val -= (1 << 32)
        return val

    def format_value(self, val: int, target_base: str | None = None) -> str:
        """Formats a signed integer into the target base string representation."""
        b = target_base or self.current_base
        u_val = val & MASK_32

        if b == "DEC":
            # Signed decimal
            if u_val & SIGN_32:
                signed = u_val - (1 << 32)
                return str(signed)
            return str(u_val)

        if b == "HEX":
            return f"{u_val:X}"

        if b == "BIN":
            return f"{u_val:b}"

        if b == "OCT":
            return f"{u_val:o}"

        return str(val)

    # Arithmetic Operations
    def add(self, a: int, b: int) -> int:
        return self._to_signed((a + b) & MASK_32)

    def sub(self, a: int, b: int) -> int:
        return self._to_signed((a - b) & MASK_32)

    def mul(self, a: int, b: int) -> int:
        return self._to_signed((a * b) & MASK_32)

    def div(self, a: int, b: int) -> int:
        if b == 0:
            raise MathError("Division by zero")
        return self._to_signed(int(a / b) & MASK_32)

    # Bitwise Logical Operations
    def bit_and(self, a: int, b: int) -> int:
        return self._to_signed((a & b) & MASK_32)

    def bit_or(self, a: int, b: int) -> int:
        return self._to_signed((a | b) & MASK_32)

    def bit_xor(self, a: int, b: int) -> int:
        return self._to_signed((a ^ b) & MASK_32)

    def bit_xnor(self, a: int, b: int) -> int:
        return self._to_signed((~(a ^ b)) & MASK_32)

    def bit_not(self, a: int) -> int:
        return self._to_signed((~a) & MASK_32)

    def bit_neg(self, a: int) -> int:
        return self._to_signed((-a) & MASK_32)

    @staticmethod
    def _to_signed(u_val: int) -> int:
        if u_val & SIGN_32:
            return u_val - (1 << 32)
        return u_val

    def evaluate_expression(self, expr_str: str, ans: int = 0) -> int:
        """Parses and evaluates a Base-N expression with arithmetic and bitwise logic."""
        import re
        s = expr_str.replace("×", "*").replace("÷", "/").replace("−", "-")

        token_patterns = [
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("NOT", r"\bNot\b|\bnot\b"),
            ("NEG", r"\bNeg\b|\bneg\b"),
            ("AND", r"\band\b"),
            ("XNOR", r"\bxnor\b"),
            ("XOR", r"\bxor\b"),
            ("OR", r"\bor\b"),
            ("OP_ADD", r"[+\-]"),
            ("OP_MUL", r"[*\/]"),
            ("ANS", r"\bAns\b|\bans\b"),
            ("NUM", r"[dhbo]?[0-9A-Fa-f]+"),
            ("WS", r"\s+"),
        ]
        master_pat = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in token_patterns))

        tokens: list[tuple[str, str]] = []
        for match in master_pat.finditer(s):
            kind = match.lastgroup
            val = match.group()
            if kind != "WS":
                tokens.append((kind, val))

        pos = 0

        def peek() -> tuple[str, str] | None:
            return tokens[pos] if pos < len(tokens) else None

        def match(*kinds: str) -> tuple[str, str] | None:
            nonlocal pos
            p = peek()
            if p and p[0] in kinds:
                pos += 1
                return p
            return None

        def parse_or() -> int:
            left = parse_and()
            while True:
                op = match("OR", "XOR", "XNOR")
                if not op:
                    break
                right = parse_and()
                if op[0] == "OR":
                    left = self.bit_or(left, right)
                elif op[0] == "XOR":
                    left = self.bit_xor(left, right)
                elif op[0] == "XNOR":
                    left = self.bit_xnor(left, right)
            return left

        def parse_and() -> int:
            left = parse_add()
            while True:
                op = match("AND")
                if not op:
                    break
                right = parse_add()
                left = self.bit_and(left, right)
            return left

        def parse_add() -> int:
            left = parse_mul()
            while True:
                op = match("OP_ADD")
                if not op:
                    break
                right = parse_mul()
                if op[1] == "+":
                    left = self.add(left, right)
                else:
                    left = self.sub(left, right)
            return left

        def parse_mul() -> int:
            left = parse_unary()
            while True:
                op = match("OP_MUL")
                if not op:
                    break
                right = parse_unary()
                if op[1] == "*":
                    left = self.mul(left, right)
                else:
                    left = self.div(left, right)
            return left

        def parse_unary() -> int:
            if match("NOT"):
                return self.bit_not(parse_unary())
            if match("NEG"):
                return self.bit_neg(parse_unary())
            op = match("OP_ADD")
            if op:
                val = parse_unary()
                return self.bit_neg(val) if op[1] == "-" else val
            return parse_primary()

        def parse_primary() -> int:
            if match("LPAREN"):
                val = parse_or()
                match("RPAREN")
                return val
            ans_tok = match("ANS")
            if ans_tok:
                return ans
            num_tok = match("NUM")
            if num_tok:
                return self.parse_value(num_tok[1])
            raise SyntaxError("BASE-N: invalid syntax in expression")

        return parse_or()

