"""Coordinate (Pol, Rec) and Sexagesimal DMS (Degrees-Minutes-Seconds) conversions."""
import math
import sympy as sp

def pol_convert(x: float, y: float, angle_unit: str = "DEG") -> tuple[float, float]:
    """Converts rectangular (x, y) to polar (r, θ)."""
    r = math.hypot(x, y)
    theta_rad = math.atan2(y, x)

    if angle_unit == "DEG":
        theta = math.degrees(theta_rad)
    elif angle_unit == "GRA":
        theta = theta_rad * 200 / math.pi
    else:
        theta = theta_rad

    return r, theta


def rec_convert(r: float, theta: float, angle_unit: str = "DEG") -> tuple[float, float]:
    """Converts polar (r, θ) to rectangular (x, y)."""
    if angle_unit == "DEG":
        theta_rad = math.radians(theta)
    elif angle_unit == "GRA":
        theta_rad = theta * math.pi / 200
    else:
        theta_rad = theta

    x = r * math.cos(theta_rad)
    y = r * math.sin(theta_rad)
    return x, y


def dms_to_decimal(degrees: float, minutes: float = 0.0, seconds: float = 0.0) -> float:
    """Converts degrees, minutes, seconds to decimal degrees."""
    sign = -1.0 if degrees < 0 else 1.0
    abs_d = abs(degrees)
    return sign * (abs_d + abs(minutes) / 60.0 + abs(seconds) / 3600.0)


def decimal_to_dms(val: float) -> tuple[int, int, float]:
    """Converts decimal degrees to integer degrees, integer minutes, and float seconds."""
    sign = -1 if val < 0 else 1
    total = abs(val)

    deg = int(total)
    rem_min = (total - deg) * 60.0
    minutes = int(rem_min)
    seconds = (rem_min - minutes) * 60.0

    return sign * deg, minutes, round(seconds, 2)


def format_dms(val: float) -> str:
    """Formats decimal degrees as Casio DMS string: e.g. 2°20°30°."""
    d, m, s = decimal_to_dms(val)
    # Format seconds without trailing zero if integer
    sec_str = f"{int(s)}" if s.is_integer() else f"{s:.2f}"
    return f"{d}°{m}°{sec_str}°"
