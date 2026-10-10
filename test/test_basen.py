"""Unit tests for BASE-N Mode (decimal, hex, binary, octal, and bitwise logic)."""
from src.core.modes.basen_engine import BaseNEngine

def test_basen_parsing_and_formatting():
    engine = BaseNEngine(current_base="HEX")

    # Parse hex FF -> 255
    v = engine.parse_value("FF")
    assert v == 255
    assert engine.format_value(v, target_base="DEC") == "255"
    assert engine.format_value(v, target_base="BIN") == "11111111"
    assert engine.format_value(v, target_base="OCT") == "377"

def test_basen_prefix_overrides():
    engine = BaseNEngine(current_base="DEC")
    # b1010 + d10 = 10 + 10 = 20
    v1 = engine.parse_value("b1010")
    v2 = engine.parse_value("d10")
    res = engine.add(v1, v2)
    assert res == 20
    assert engine.format_value(res, "HEX") == "14"

def test_basen_bitwise_logic():
    engine = BaseNEngine()
    # 1010 (10) AND 1100 (12) = 1000 (8)
    assert engine.bit_and(10, 12) == 8
    # 1010 (10) OR 1100 (12) = 1110 (14)
    assert engine.bit_or(10, 12) == 14
    # 1010 (10) XOR 1100 (12) = 0110 (6)
    assert engine.bit_xor(10, 12) == 6

def test_basen_twos_complement_negation():
    engine = BaseNEngine()
    # Negate 5 -> -5
    neg = engine.bit_neg(5)
    assert neg == -5
    # Hex of -1 is FFFFFFFF
    assert engine.format_value(-1, "HEX") == "FFFFFFFF"
