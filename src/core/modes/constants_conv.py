"""Scientific Constants (40 CODATA constants) and Metric Conversions (40 units)."""
from dataclasses import dataclass
from src.core.math.errors import ArgumentError

@dataclass(frozen=True)
class ScientificConstant:
    code: int
    symbol: str
    name: str
    value: float


SCIENTIFIC_CONSTANTS: dict[int, ScientificConstant] = {
    1: ScientificConstant(1, "mp", "proton mass", 1.672621637e-27),
    2: ScientificConstant(2, "mn", "neutron mass", 1.674927211e-27),
    3: ScientificConstant(3, "me", "electron mass", 9.10938215e-31),
    4: ScientificConstant(4, "mμ", "muon mass", 1.88353130e-28),
    5: ScientificConstant(5, "a0", "Bohr radius", 5.2917720859e-11),
    6: ScientificConstant(6, "h", "Planck constant", 6.62606896e-34),
    7: ScientificConstant(7, "μN", "nuclear magneton", 5.05078324e-27),
    8: ScientificConstant(8, "μB", "Bohr magneton", 9.27400915e-24),
    9: ScientificConstant(9, "ħ", "Planck constant, rationalized", 1.054571628e-34),
    10: ScientificConstant(10, "α", "fine-structure constant", 7.2973525376e-3),
    11: ScientificConstant(11, "re", "classical electron radius", 2.8179402894e-15),
    12: ScientificConstant(12, "λc", "Compton wavelength", 2.426310217e-12),
    13: ScientificConstant(13, "γp", "proton gyromagnetic ratio", 2.675222099e8),
    14: ScientificConstant(14, "λcp", "proton Compton wavelength", 1.3214098446e-15),
    15: ScientificConstant(15, "λcn", "neutron Compton wavelength", 1.3195908951e-15),
    16: ScientificConstant(16, "R∞", "Rydberg constant", 10973731.568527),
    17: ScientificConstant(17, "u", "atomic mass unit", 1.660538782e-27),
    18: ScientificConstant(18, "μp", "proton magnetic moment", 1.410606662e-26),
    19: ScientificConstant(19, "μe", "electron magnetic moment", -9.28476377e-24),
    20: ScientificConstant(20, "μn", "neutron magnetic moment", -9.6623641e-27),
    21: ScientificConstant(21, "μμ", "muon magnetic moment", -4.4904478e-26),
    22: ScientificConstant(22, "F", "Faraday constant", 96485.3399),
    23: ScientificConstant(23, "e", "elementary charge", 1.602176487e-19),
    24: ScientificConstant(24, "NA", "Avogadro constant", 6.02214179e23),
    25: ScientificConstant(25, "k", "Boltzmann constant", 1.3806504e-23),
    26: ScientificConstant(26, "Vm", "molar volume of ideal gas", 0.022413996),
    27: ScientificConstant(27, "R", "molar gas constant", 8.314472),
    28: ScientificConstant(28, "c0", "speed of light in vacuum", 299792458.0),
    29: ScientificConstant(29, "c1", "first radiation constant", 3.74177118e-16),
    30: ScientificConstant(30, "c2", "second radiation constant", 0.014387752),
    31: ScientificConstant(31, "σ", "Stefan-Boltzmann constant", 5.670400e-8),
    32: ScientificConstant(32, "ε0", "electric constant", 8.854187817e-12),
    33: ScientificConstant(33, "μ0", "magnetic constant", 1.2566370614e-6),
    34: ScientificConstant(34, "Φ0", "magnetic flux quantum", 2.067833667e-15),
    35: ScientificConstant(35, "g", "standard acceleration of gravity", 9.80665),
    36: ScientificConstant(36, "G0", "conductance quantum", 7.7480917004e-5),
    37: ScientificConstant(37, "Z0", "characteristic impedance of vacuum", 376.730313461),
    38: ScientificConstant(38, "t", "Celsius temperature", 273.15),
    39: ScientificConstant(39, "G", "Newtonian constant of gravitation", 6.67428e-11),
    40: ScientificConstant(40, "atm", "standard atmosphere", 101325.0),
}


def get_constant(code: int) -> ScientificConstant:
    if code not in SCIENTIFIC_CONSTANTS:
        raise ArgumentError(f"Constant code must be 1-40 (got {code})")
    return SCIENTIFIC_CONSTANTS[code]


def convert_metric(code: int, value: float) -> float:
    """Applies metric conversion pair 01-40 on input value."""
    if code == 1:   return value * 2.54             # in -> cm
    if code == 2:   return value / 2.54             # cm -> in
    if code == 3:   return value * 0.3048           # ft -> m
    if code == 4:   return value / 0.3048           # m -> ft
    if code == 5:   return value * 0.9144           # yd -> m
    if code == 6:   return value / 0.9144           # m -> yd
    if code == 7:   return value * 1.609344         # mile -> km
    if code == 8:   return value / 1.609344         # km -> mile
    if code == 9:   return value * 1852.0           # n mile -> m
    if code == 10:  return value / 1852.0           # m -> n mile
    if code == 11:  return value * 4046.8564224     # acre -> m²
    if code == 12:  return value / 4046.8564224     # m² -> acre
    if code == 13:  return value * 3.785411784      # gal(US) -> L
    if code == 14:  return value / 3.785411784      # L -> gal(US)
    if code == 15:  return value * 4.54609          # gal(UK) -> L
    if code == 16:  return value / 4.54609          # L -> gal(UK)
    if code == 17:  return value * 3.085677581e13   # pc -> km
    if code == 18:  return value / 3.085677581e13   # km -> pc
    if code == 19:  return value / 3.6              # km/h -> m/s
    if code == 20:  return value * 3.6              # m/s -> km/h
    if code == 21:  return value * 28.349523125     # oz -> g
    if code == 22:  return value / 28.349523125     # g -> oz
    if code == 23:  return value * 0.45359237       # lb -> kg
    if code == 24:  return value / 0.45359237       # kg -> lb
    if code == 25:  return value * 101325.0         # atm -> Pa
    if code == 26:  return value / 101325.0         # Pa -> atm
    if code == 27:  return value * 133.322          # mmHg -> Pa
    if code == 28:  return value / 133.322          # Pa -> mmHg
    if code == 29:  return value * 0.74569987158    # hp -> kW
    if code == 30:  return value / 0.74569987158    # kW -> hp
    if code == 31:  return value * 98066.5          # kgf/cm² -> Pa
    if code == 32:  return value / 98066.5          # Pa -> kgf/cm²
    if code == 33:  return value * 9.80665          # kgf·m -> J
    if code == 34:  return value / 9.80665          # J -> kgf·m
    if code == 35:  return value * 6.894757         # lbf/in² -> kPa
    if code == 36:  return value / 6.894757         # kPa -> lbf/in²
    if code == 37:  return (value - 32.0) * 5.0 / 9.0  # °F -> °C
    if code == 38:  return value * 9.0 / 5.0 + 32.0    # °C -> °F
    if code == 39:  return value / 4.184            # J -> cal
    if code == 40:  return value * 4.184            # cal -> J

    raise ArgumentError(f"Conversion code must be 1-40 (got {code})")
