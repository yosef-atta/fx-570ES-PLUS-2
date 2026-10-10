"""Diagnostic error classes matching Casio fx-570ES PLUS error specifications."""

class CalculatorError(Exception):
    """Base class for all calculator errors."""
    error_title = "ERROR"

    def __init__(self, message: str = "", position: int | None = None):
        super().__init__(message)
        self.message = message
        self.position = position

    @property
    def display_name(self) -> str:
        return self.error_title


class MathError(CalculatorError):
    """Raised for domain violations, division by zero, and numerical overflow."""
    error_title = "Math ERROR"


class SyntaxError(CalculatorError):
    """Raised for malformed expressions, unexpected tokens, and unbalanced structures."""
    error_title = "Syntax ERROR"


class StackError(CalculatorError):
    """Raised when expression complexity or stack depth exceeds limit."""
    error_title = "Stack ERROR"


class ArgumentError(CalculatorError):
    """Raised when a function receives an argument outside valid parameters."""
    error_title = "Argument ERROR"


class CantSolveError(CalculatorError):
    """Raised when SOLVE algorithm cannot converge to a solution."""
    error_title = "Can't Solve"


class TimeOutError(CalculatorError):
    """Raised when numerical calculus calculation exceeds iteration/time limit."""
    error_title = "Time Out"
