"""Abstract Syntax Tree node definitions for mathematical expressions."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ASTNode:
    """Base class for all AST nodes."""
    position: int = 0


@dataclass(frozen=True)
class NumberNode(ASTNode):
    value: str = "0"


@dataclass(frozen=True)
class VariableNode(ASTNode):
    name: str = "X"


@dataclass(frozen=True)
class ConstantNode(ASTNode):
    name: str = "pi"  # "pi" or "e"


@dataclass(frozen=True)
class AnsNode(ASTNode):
    pass


@dataclass(frozen=True)
class PreAnsNode(ASTNode):
    pass


@dataclass(frozen=True)
class UnaryOpNode(ASTNode):
    op: str = "−"
    operand: ASTNode = None


@dataclass(frozen=True)
class BinaryOpNode(ASTNode):
    left: ASTNode = None
    op: str = "+"
    right: ASTNode = None


@dataclass(frozen=True)
class PostfixOpNode(ASTNode):
    operand: ASTNode = None
    op: str = "%"


@dataclass(frozen=True)
class FractionNode(ASTNode):
    numerator: ASTNode = None
    denominator: ASTNode = None


@dataclass(frozen=True)
class MixedFractionNode(ASTNode):
    whole: ASTNode = None
    numerator: ASTNode = None
    denominator: ASTNode = None


@dataclass(frozen=True)
class FunctionCallNode(ASTNode):
    name: str = "sin"
    args: tuple[ASTNode, ...] = ()


@dataclass(frozen=True)
class DerivativeNode(ASTNode):
    expr: ASTNode = None
    variable: str = "X"
    at_point: ASTNode = None
    tolerance: ASTNode | None = None


@dataclass(frozen=True)
class IntegralNode(ASTNode):
    expr: ASTNode = None
    variable: str = "X"
    lower: ASTNode = None
    upper: ASTNode = None
    tolerance: ASTNode | None = None


@dataclass(frozen=True)
class SummationNode(ASTNode):
    expr: ASTNode = None
    variable: str = "X"
    lower: ASTNode = None
    upper: ASTNode = None


@dataclass(frozen=True)
class DMSNode(ASTNode):
    degrees: ASTNode = None
    minutes: ASTNode | None = None
    seconds: ASTNode | None = None


@dataclass(frozen=True)
class EquationNode(ASTNode):
    left: ASTNode = None
    right: ASTNode = None


@dataclass(frozen=True)
class MultiStatementNode(ASTNode):
    statements: tuple[ASTNode, ...] = ()
