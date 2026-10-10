"""Tests for calculator memory, variables, M+, Ans, PreAns, and replay history."""
import sympy as sp
from src.core.math.memory import MemoryManager

def test_variable_get_set():
    mem = MemoryManager()
    assert mem.get_var("A") == 0
    mem.set_var("A", 15)
    assert mem.get_var("A") == 15
    mem.set_var("B", sp.Rational(1, 2))
    assert mem.get_var("B") == sp.Rational(1, 2)

def test_ans_and_preans():
    mem = MemoryManager()
    mem.store_result("2+3", sp.Integer(5), "5")
    assert mem.ans == 5
    assert mem.pre_ans == 0

    mem.store_result("5*2", sp.Integer(10), "10")
    assert mem.ans == 10
    assert mem.pre_ans == 5

def test_independent_memory_m():
    mem = MemoryManager()
    assert not mem.has_independent_memory
    mem.m_plus(100)
    assert mem.get_var("M") == 100
    assert mem.has_independent_memory
    mem.m_minus(40)
    assert mem.get_var("M") == 60
    mem.m_minus(60)
    assert mem.get_var("M") == 0
    assert not mem.has_independent_memory

def test_history_replay():
    mem = MemoryManager()
    mem.store_result("1+1", sp.Integer(2), "2")
    mem.store_result("2+2", sp.Integer(4), "4")
    mem.store_result("3+3", sp.Integer(6), "6")

    # Navigate up (older)
    e3 = mem.history_prev()
    assert e3.expression == "3+3"
    e2 = mem.history_prev()
    assert e2.expression == "2+2"
    e1 = mem.history_prev()
    assert e1.expression == "1+1"

    # Navigate down (newer)
    e2_again = mem.history_next()
    assert e2_again.expression == "2+2"
    e3_again = mem.history_next()
    assert e3_again.expression == "3+3"
    assert mem.history_next() is None

def test_clear_memory():
    mem = MemoryManager()
    mem.set_var("X", 99)
    mem.store_result("1+1", sp.Integer(2), "2")
    mem.clear_memory()
    assert mem.get_var("X") == 0
    assert mem.ans == 0
    assert len(mem.history) == 1  # History preserved on clear_memory

    mem.clear_all()
    assert len(mem.history) == 0  # History cleared on clear_all
