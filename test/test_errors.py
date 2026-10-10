"""Tests for calculator diagnostic error classes and jump-to-error."""
import pytest
from src.core.controller import Controller
from src.core.math.errors import (
    MathError, SyntaxError, StackError, ArgumentError, CantSolveError
)

def test_error_titles():
    assert MathError().display_name == "Math ERROR"
    assert SyntaxError().display_name == "Syntax ERROR"
    assert StackError().display_name == "Stack ERROR"
    assert ArgumentError().display_name == "Argument ERROR"
    assert CantSolveError().display_name == "Can't Solve"

def test_syntax_error_goto_cursor_position():
    c = Controller()
    # Malformed expression: 3 + × 2
    for k in ("3", "add", "multiply", "2", "equals"):
        c.press(k)
    assert c.state.error_state
    assert c.state.error_message == "Syntax ERROR"

    # Press right to jump to error
    c.press("right")
    assert not c.state.error_state
    assert c.state.cursor_position == 2  # Position of unexpected '×'
