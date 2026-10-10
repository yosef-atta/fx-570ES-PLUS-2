"""Tests for Pol, Rec, and sexagesimal DMS operations."""
import math
from src.core.math.coordinates import pol_convert, rec_convert, dms_to_decimal, decimal_to_dms, format_dms

def test_polar_conversion():
    r, theta = pol_convert(1, 1, angle_unit="DEG")
    assert round(r, 6) == round(math.sqrt(2), 6)
    assert round(theta, 6) == 45.0

    r_rad, theta_rad = pol_convert(0, 2, angle_unit="RAD")
    assert r_rad == 2.0
    assert round(theta_rad, 6) == round(math.pi / 2, 6)

def test_rectangular_conversion():
    x, y = rec_convert(math.sqrt(2), 45, angle_unit="DEG")
    assert round(x, 6) == 1.0
    assert round(y, 6) == 1.0

def test_dms_conversion():
    # 2° 20' 30" -> decimal
    dec = dms_to_decimal(2, 20, 30)
    assert round(dec, 5) == round(2 + 20/60 + 30/3600, 5)

    # decimal -> DMS
    d, m, s = decimal_to_dms(dec)
    assert d == 2
    assert m == 20
    assert round(s) == 30

    # formatting
    s_formatted = format_dms(dec)
    assert s_formatted == "2°20°30°"
