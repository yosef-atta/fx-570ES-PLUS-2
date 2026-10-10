"""Unit tests for 40 Scientific Constants and 40 Metric Conversions."""
from src.core.modes.constants_conv import get_constant, convert_metric

def test_scientific_constants():
    # 01: proton mass
    c1 = get_constant(1)
    assert c1.symbol == "mp"
    assert c1.value == 1.672621637e-27

    # 28: speed of light
    c28 = get_constant(28)
    assert c28.symbol == "c0"
    assert c28.value == 299792458.0

    # 35: g
    c35 = get_constant(35)
    assert c35.symbol == "g"
    assert c35.value == 9.80665

def test_metric_conversions():
    # 01: 10 in -> 25.4 cm
    assert convert_metric(1, 10.0) == 25.4
    # 02: 25.4 cm -> 10 in
    assert convert_metric(2, 25.4) == 10.0

    # 19: 36 km/h -> 10 m/s
    assert convert_metric(19, 36.0) == 10.0
    # 20: 10 m/s -> 36 km/h
    assert convert_metric(20, 10.0) == 36.0

    # 37: 212 °F -> 100 °C
    assert convert_metric(37, 212.0) == 100.0
    # 38: 100 °C -> 212 °F
    assert convert_metric(38, 100.0) == 212.0
