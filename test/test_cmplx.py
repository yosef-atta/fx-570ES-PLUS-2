"""Unit tests for CMPLX Mode (complex numbers)."""
import math
import sympy as sp
from src.core.modes.complex_engine import ComplexEngine

def test_cmplx_arithmetic_and_formatting():
    engine = ComplexEngine(angle_unit="DEG")

    # (2 + 3i) * (4 + 5i) = -7 + 22i
    z1 = 2 + 3 * sp.I
    z2 = 4 + 5 * sp.I
    prod = z1 * z2
    assert engine.format_complex(prod) == "-7+22i"

    # 1 / i = -i
    inv_i = 1 / sp.I
    assert engine.format_complex(inv_i) == "-i"

def test_cmplx_modulus_argument_conjugate():
    engine = ComplexEngine(angle_unit="DEG")

    # Abs(3 + 4i) = 5
    z = 3 + 4 * sp.I
    assert engine.abs_mod(z) == 5

    # arg(1 + i) = 45 deg
    z2 = 1 + sp.I
    assert float(engine.arg(z2)) == 45.0

    # Conjg(2 + 3i) = 2 - 3i
    assert engine.format_complex(engine.conjg(z1 := 2 + 3 * sp.I)) == "2-3i"

def test_cmplx_polar_conversion():
    engine = ComplexEngine(angle_unit="DEG")

    # Polar form of 3 + 4i is 5∠53.13010235
    z = 3 + 4 * sp.I
    pol_str = engine.format_complex(z, target_format="r∠θ")
    assert pol_str.startswith("5∠53.13")

    # 2∠45 converted to rectangular
    rec = engine.polar_to_complex(math.sqrt(2), 45)
    assert round(complex(sp.N(rec)).real, 2) == 1.0
    assert round(complex(sp.N(rec)).imag, 2) == 1.0
