"""Unit tests for VECTOR Mode (vector algebra, dot and cross products)."""
from src.core.modes.vector_engine import VectorEngine

def test_vector_addition_and_subtraction():
    engine = VectorEngine()
    engine.set_vector("VctA", [1, 2, 3])
    engine.set_vector("VctB", [4, 5, 6])

    # VctA + VctB = [5, 7, 9]
    v_sum = engine.add("VctA", "VctB")
    assert v_sum == [5.0, 7.0, 9.0]

    # VctB - VctA = [3, 3, 3]
    v_diff = engine.sub("VctB", "VctA")
    assert v_diff == [3.0, 3.0, 3.0]

def test_vector_dot_and_cross_product():
    engine = VectorEngine()
    engine.set_vector("VctA", [1, 2, 3])
    engine.set_vector("VctB", [4, 5, 6])

    # VctA • VctB = 1*4 + 2*5 + 3*6 = 32
    assert engine.dot("VctA", "VctB") == 32.0

    # VctA × VctB = (-3, 6, -3)
    cross_v = engine.cross("VctA", "VctB")
    assert cross_v == [-3.0, 6.0, -3.0]

def test_vector_magnitude():
    engine = VectorEngine()
    engine.set_vector("VctA", [3, 4])
    assert engine.magnitude("VctA") == 5.0
