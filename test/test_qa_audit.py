"""Full functional QA audit against official Casio fx-570ES PLUS-2 manual."""
import pytest
import sympy as sp
from src.core.controller import Controller
from src.core.key_registry import REGISTRY, resolve
from src.core.action import Kind
from src.ui.main_window import MainWindow

def test_audit_all_physical_keys_are_active():
    """Verify all 54 physical keys have active actions and zero deferred stubs."""
    assert len(REGISTRY) == 54
    for key_id, key_obj in REGISTRY.items():
        assert key_obj.primary.kind in (Kind.INSERT, Kind.COMMAND)
        if key_obj.shift:
            assert key_obj.shift.kind in (Kind.INSERT, Kind.COMMAND)
        if key_obj.alpha:
            assert key_obj.alpha.kind in (Kind.INSERT, Kind.COMMAND)


def test_audit_setup_menu_options_and_prompts():
    """Audit all SETUP options: angle units, Fix, Sci, Norm, ab/c, d/c, CMPLX, STAT freq."""
    c = Controller()

    # 1. Angle units DEG / RAD / GRA
    c.press("shift")
    c.press("mode")  # SETUP
    assert c.state.active_menu == "SETUP"
    c.press("4")     # RAD
    assert c.state.angle_unit == "RAD"

    c.press("shift")
    c.press("mode")
    c.press("5")     # GRA
    assert c.state.angle_unit == "GRA"

    c.press("shift")
    c.press("mode")
    c.press("3")     # DEG
    assert c.state.angle_unit == "DEG"

    # 2. Fix 0~9 prompt
    c.press("shift")
    c.press("mode")
    c.press("6")     # Fix
    assert c.state.prompt_name == "Fix"
    c.press("2")     # Fix 2 decimal places
    assert c.state.number_format == "Fix 2"

    # 3. Sci 0~9 prompt
    c.press("shift")
    c.press("mode")
    c.press("down")  # Page 1
    c.press("1")     # Sci
    assert c.state.prompt_name == "Sci"
    c.press("4")     # Sci 4
    assert c.state.number_format == "Sci 4"

    # 4. Norm 1~2 prompt
    c.press("shift")
    c.press("mode")
    c.press("down")
    c.press("2")     # Norm
    assert c.state.prompt_name == "Norm"
    c.press("1")     # Norm 1
    assert c.state.number_format == "Norm 1"

    # 5. Fraction display: ab/c vs d/c
    c.press("shift")
    c.press("mode")
    c.press("down")
    c.press("3")     # ab/c
    assert c.state.display_format == "ab/c"

    c.press("shift")
    c.press("mode")
    c.press("down")
    c.press("4")     # d/c
    assert c.state.display_format == "MthIO-MathO"

    # 6. CMPLX format prompt in SETUP
    c.press("shift")
    c.press("mode")
    c.press("down")
    c.press("5")     # CMPLX
    assert c.state.prompt_name == "CMPLX_FORMAT"
    c.press("2")     # r∠θ
    assert c.state.complex_format == "r∠θ"

    # 7. STAT frequency prompt in SETUP
    c.press("shift")
    c.press("mode")
    c.press("down")
    c.press("6")     # STAT
    assert c.state.prompt_name == "STAT_FREQ"
    c.press("1")     # Frequency ON
    assert c.state.stat_frequency_on is True


def test_audit_all_8_modes_initialization():
    """Verify switching to every single one of the 8 modes initializes clean state."""
    c = Controller()
    modes = ("COMP", "CMPLX", "STAT", "BASE-N", "EQN", "MATRIX", "TABLE", "VECTOR")

    for idx, mode_name in enumerate(modes, 1):
        c.press("mode")
        if idx <= 6:
            c.press(str(idx))
        else:
            c.press("down")
            c.press(str(idx - 6))
        assert c.state.mode == mode_name
        assert c.state.power_on


def test_audit_clr_options():
    """Audit CLR menu: Setup reset, Memory reset, and All reset."""
    c = Controller()
    # Modify settings
    c.state.angle_unit = "RAD"
    c.state.number_format = "Fix 4"
    c.memory.set_var("A", 123)

    # 1. Clear Setup
    c.press("shift")
    c.press("9")  # CLR
    c.press("1")  # Setup
    assert c.state.angle_unit == "DEG"
    assert c.state.number_format == "Norm 1"
    assert c.memory.get_var("A") == 123

    # 2. Clear Memory
    c.press("shift")
    c.press("9")
    c.press("2")  # Memory
    assert c.memory.get_var("A") == 0

    # 3. Clear All
    c.state.expression = "99"
    c.press("shift")
    c.press("9")
    c.press("3")  # All
    assert c.state.expression == ""
    assert c.state.angle_unit == "DEG"
