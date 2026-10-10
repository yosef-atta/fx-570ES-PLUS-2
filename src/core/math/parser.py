"""Recursive descent parser with Casio fx-570ES PLUS operator precedence and auto-closing parentheses."""
from .ast_nodes import (
    ASTNode, NumberNode, VariableNode, ConstantNode, AnsNode, PreAnsNode,
    UnaryOpNode, BinaryOpNode, PostfixOpNode, FractionNode, MixedFractionNode,
    FunctionCallNode, DerivativeNode, IntegralNode, SummationNode,
    EquationNode, MultiStatementNode, DMSNode
)
from .errors import SyntaxError
from .tokens import Token, TokenType

class Parser:
    """Parses a list of tokens into an AST."""

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.open_paren_count = 0

    def parse(self) -> ASTNode:
        if not self.tokens or self._current().type == TokenType.EOF:
            return NumberNode(value="0", position=0)

        # Check for multi-statements separated by ':'
        statements: list[ASTNode] = []
        stmt = self._parse_statement()
        statements.append(stmt)

        while self._match(TokenType.COLON):
            if self._current().type == TokenType.EOF:
                break
            statements.append(self._parse_statement())

        if len(statements) == 1:
            return statements[0]
        return MultiStatementNode(statements=tuple(statements), position=statements[0].position)

    def _parse_statement(self) -> ASTNode:
        """Parses an expression or an equation (left = right)."""
        left = self._parse_expression()

        if self._match(TokenType.EQUALS):
            eq_pos = self._previous().position
            right = self._parse_expression()
            return EquationNode(left=left, right=right, position=eq_pos)

        return left

    def _parse_expression(self) -> ASTNode:
        """Entry point for expression parsing (lowest precedence binary ops: +, -)."""
        return self._parse_addition()

    def _parse_addition(self) -> ASTNode:
        node = self._parse_multiplication()

        while True:
            if self._match(TokenType.PLUS):
                op = "+"
                pos = self._previous().position
                right = self._parse_multiplication()
                node = BinaryOpNode(left=node, op=op, right=right, position=pos)
            elif self._match(TokenType.MINUS):
                op = "-"
                pos = self._previous().position
                right = self._parse_multiplication()
                node = BinaryOpNode(left=node, op=op, right=right, position=pos)
            else:
                break

        return node

    def _parse_multiplication(self) -> ASTNode:
        node = self._parse_combinatorics()

        while True:
            if self._match(TokenType.MULTIPLY):
                pos = self._previous().position
                right = self._parse_combinatorics()
                node = BinaryOpNode(left=node, op="×", right=right, position=pos)
            elif self._match(TokenType.DIVIDE):
                pos = self._previous().position
                right = self._parse_combinatorics()
                node = BinaryOpNode(left=node, op="÷", right=right, position=pos)
            else:
                break

        return node

    def _parse_combinatorics(self) -> ASTNode:
        """Parses nPr and nCr."""
        node = self._parse_unary()

        while True:
            if self._match(TokenType.NPR):
                pos = self._previous().position
                right = self._parse_unary()
                node = BinaryOpNode(left=node, op="nPr", right=right, position=pos)
            elif self._match(TokenType.NCR):
                pos = self._previous().position
                right = self._parse_unary()
                node = BinaryOpNode(left=node, op="nCr", right=right, position=pos)
            elif self._match(TokenType.ANGLE):
                pos = self._previous().position
                right = self._parse_unary()
                node = BinaryOpNode(left=node, op="∠", right=right, position=pos)
            else:
                break

        return node

    def _parse_unary(self) -> ASTNode:
        """Unary negation operator (−). Has lower precedence than powers (e.g. −3² = −9)."""
        if self._match(TokenType.NEG):
            pos = self._previous().position
            operand = self._parse_unary()
            return UnaryOpNode(op="−", operand=operand, position=pos)

        return self._parse_power()

    def _parse_power(self) -> ASTNode:
        """Exponentiation (^) is right-associative."""
        node = self._parse_postfix()

        if self._match(TokenType.POWER):
            pos = self._previous().position
            right = self._parse_power()  # Right-associative
            return BinaryOpNode(left=node, op="^", right=right, position=pos)

        return node

    def _parse_postfix(self) -> ASTNode:
        """Postfix operators: factorials (!), percentages (%), DMS (°), and mixed fractions."""
        node = self._parse_primary()

        # Infix mixed fraction: <whole> mixed/ <num> / <den> or <whole> ⌟ <num> ⌟ <den>
        if self._match(TokenType.MIXED_FRACTION):
            pos = self._previous().position
            second = self._parse_primary()
            if self._match(TokenType.DIVIDE) or self._match(TokenType.MIXED_FRACTION):
                third = self._parse_primary()
                node = MixedFractionNode(whole=node, numerator=second, denominator=third, position=pos)
            else:
                # Single separator: e.g. 1⌟3 -> 1/3
                node = FractionNode(numerator=node, denominator=second, position=pos)

        while True:
            if self._match(TokenType.FACTORIAL):
                pos = self._previous().position
                node = PostfixOpNode(operand=node, op="!", position=pos)
            elif self._match(TokenType.PERCENT):
                pos = self._previous().position
                node = PostfixOpNode(operand=node, op="%", position=pos)
            elif self._match(TokenType.DMS):
                pos = self._previous().position
                node = PostfixOpNode(operand=node, op="°", position=pos)
            elif self._match(TokenType.EXP10):
                # e.g., 2.5 ×10^ 3 -> 2.5 * (10 ^ 3)
                pos = self._previous().position
                exp_operand = self._parse_unary()
                ten_pow = BinaryOpNode(
                    left=NumberNode("10", position=pos),
                    op="^",
                    right=exp_operand,
                    position=pos
                )
                node = BinaryOpNode(left=node, op="×", right=ten_pow, position=pos)
            else:
                break

        return node

    def _parse_primary(self) -> ASTNode:
        token = self._current()

        # 0. Prefix mixed fraction (e.g. mixed/ 2/1/3 or mixed/(2, 1, 3))
        if self._match(TokenType.MIXED_FRACTION):
            pos = self._previous().position
            if self._match(TokenType.LPAREN):
                self.open_paren_count += 1
                first = self._parse_expression()
                if self._match(TokenType.COMMA):
                    second = self._parse_expression()
                    if self._match(TokenType.COMMA):
                        third = self._parse_expression()
                        if self._match(TokenType.RPAREN):
                            self.open_paren_count -= 1
                        elif self._current().type == TokenType.EOF:
                            self.open_paren_count -= 1
                        return MixedFractionNode(whole=first, numerator=second, denominator=third, position=pos)
                    else:
                        if self._match(TokenType.RPAREN):
                            self.open_paren_count -= 1
                        elif self._current().type == TokenType.EOF:
                            self.open_paren_count -= 1
                        return FractionNode(numerator=first, denominator=second, position=pos)
                else:
                    if self._match(TokenType.RPAREN):
                        self.open_paren_count -= 1
                    return first
            else:
                first = self._parse_primary()
                if self._match(TokenType.DIVIDE) or self._match(TokenType.MIXED_FRACTION):
                    second = self._parse_primary()
                    if self._match(TokenType.DIVIDE) or self._match(TokenType.MIXED_FRACTION):
                        third = self._parse_primary()
                        return MixedFractionNode(whole=first, numerator=second, denominator=third, position=pos)
                    else:
                        return FractionNode(numerator=first, denominator=second, position=pos)
                return first

        # 1. Number
        if self._match(TokenType.NUMBER):
            return NumberNode(value=token.value, position=token.position)

        # 2. Variable
        if self._match(TokenType.VARIABLE):
            return VariableNode(name=token.value, position=token.position)

        # 3. Ans / PreAns
        if self._match(TokenType.ANS):
            return AnsNode(position=token.position)
        if self._match(TokenType.PREANS):
            return PreAnsNode(position=token.position)

        # 4. Constants
        if self._match(TokenType.PI):
            return ConstantNode(name="pi", position=token.position)
        if self._match(TokenType.E_CONST):
            return ConstantNode(name="e", position=token.position)
        if self._match(TokenType.I_IMAG):
            return ConstantNode(name="i", position=token.position)

        # 5. Parenthesized expression
        if self._match(TokenType.LPAREN):
            pos = self._previous().position
            self.open_paren_count += 1
            expr = self._parse_expression()
            if self._match(TokenType.RPAREN):
                self.open_paren_count -= 1
            elif self._current().type == TokenType.EOF:
                # Auto-close parenthesis at EOF
                self.open_paren_count -= 1
            else:
                raise SyntaxError("Expected closing parenthesis ')'", position=self._current().position)
            return expr

        # 6. Functions with parentheses/arguments
        if token.type in (
            TokenType.SIN, TokenType.COS, TokenType.TAN,
            TokenType.ASIN, TokenType.ACOS, TokenType.ATAN,
            TokenType.SINH, TokenType.COSH, TokenType.TANH,
            TokenType.ASINH, TokenType.ACOSH, TokenType.ATANH,
            TokenType.LOG, TokenType.LN, TokenType.EXP, TokenType.TEN_POW,
            TokenType.SQRT, TokenType.CBRT, TokenType.NTH_ROOT,
            TokenType.ABS, TokenType.RND, TokenType.RAN_HASH, TokenType.RAN_INT,
            TokenType.POL, TokenType.REC,
            TokenType.DERIVATIVE, TokenType.INTEGRAL, TokenType.SUMMATION,
            TokenType.ARG, TokenType.CONJG
        ):
            return self._parse_function_call()

        # Unexpected token
        if token.type == TokenType.EOF:
            raise SyntaxError("Unexpected end of expression", position=token.position)
        raise SyntaxError(f"Unexpected token '{token.value}'", position=token.position)

    def _parse_function_call(self) -> ASTNode:
        fn_tok = self._advance()
        name = fn_tok.value
        pos = fn_tok.position

        # Special 0-arg function: Ran#
        if fn_tok.type == TokenType.RAN_HASH:
            return FunctionCallNode(name="Ran#", args=(), position=pos)

        # Expect open paren '(' if present, or parse single primary operand
        has_paren = self._match(TokenType.LPAREN)
        if has_paren:
            self.open_paren_count += 1

        args: list[ASTNode] = []
        if not has_paren:
            arg = self._parse_postfix()
            args = [arg]
        else:
            if self._current().type == TokenType.RPAREN:
                # Empty argument
                self._advance()
                self.open_paren_count -= 1
            else:
                first_arg = self._parse_expression()
                args.append(first_arg)

                while self._match(TokenType.COMMA):
                    args.append(self._parse_expression())

                if self._match(TokenType.RPAREN):
                    self.open_paren_count -= 1
                elif self._current().type == TokenType.EOF:
                    # Auto-close at EOF
                    self.open_paren_count -= 1
                else:
                    raise SyntaxError("Expected ')' or ','", position=self._current().position)

        # Map to specialized AST node if applicable
        if fn_tok.type == TokenType.DERIVATIVE:
            # d/dx(f(x), a, [tol])
            if len(args) < 2:
                raise SyntaxError("d/dx requires expression and evaluation point", position=pos)
            tol = args[2] if len(args) > 2 else None
            return DerivativeNode(expr=args[0], variable="X", at_point=args[1], tolerance=tol, position=pos)

        if fn_tok.type == TokenType.INTEGRAL:
            # ∫(f(x), a, b, [tol])
            if len(args) < 3:
                raise SyntaxError("∫ requires expression, lower bound, and upper bound", position=pos)
            tol = args[3] if len(args) > 3 else None
            return IntegralNode(expr=args[0], variable="X", lower=args[1], upper=args[2], tolerance=tol, position=pos)

        if fn_tok.type == TokenType.SUMMATION:
            # Σ(f(x), a, b)
            if len(args) < 3:
                raise SyntaxError("Σ requires expression, lower bound, and upper bound", position=pos)
            return SummationNode(expr=args[0], variable="X", lower=args[1], upper=args[2], position=pos)

        # Square root / Cube root without explicit function name
        if fn_tok.type == TokenType.SQRT:
            return FunctionCallNode(name="sqrt", args=tuple(args), position=pos)
        if fn_tok.type == TokenType.CBRT:
            return FunctionCallNode(name="cbrt", args=tuple(args), position=pos)
        if fn_tok.type == TokenType.NTH_ROOT:
            # xth root of y: args[0]=root_index, args[1]=radicand
            return FunctionCallNode(name="nth_root", args=tuple(args), position=pos)

        return FunctionCallNode(name=name, args=tuple(args), position=pos)

    def _current(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]

    def _previous(self) -> Token:
        return self.tokens[self.pos - 1]

    def _advance(self) -> Token:
        token = self._current()
        if self.pos < len(self.tokens):
            self.pos += 1
        return token

    def _match(self, token_type: TokenType) -> bool:
        if self._current().type == token_type:
            self._advance()
            return True
        return False
