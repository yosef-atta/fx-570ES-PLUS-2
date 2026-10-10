"""Tests for Phase 5 Windows Release: versioning, preferences, icon, and shortcuts."""
import os
from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QIcon, QPixmap, QKeyEvent
from src.version import (
    APP_NAME,
    VERSION,
    VERSION_TUPLE,
    AUTHOR,
    ORGANIZATION,
    COPYRIGHT,
    DESCRIPTION,
)
from src.core.state import CalculatorState
from src.core.preferences import PreferencesManager
from src.input.keyboard import (
    register_custom_shortcut,
    clear_custom_shortcuts,
    key_to_id,
)
from src.ui.main_window import MainWindow


def test_version_metadata():
    """Verify application metadata and versioning are properly defined."""
    assert VERSION == "2.0.0"
    assert VERSION_TUPLE == (2, 0, 0, 0)
    assert "Casio" in APP_NAME
    assert "fx-570ES" in APP_NAME
    assert AUTHOR == "OpenScientific Team"
    assert ORGANIZATION == "OpenScientific"
    assert "2026" in COPYRIGHT
    assert len(DESCRIPTION) > 10


def test_icon_assets_exist_and_valid():
    """Verify icon.png and icon.ico exist and load properly as valid image assets."""
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "src", "ui", "assets")
    png_path = os.path.join(assets_dir, "icon.png")
    ico_path = os.path.join(assets_dir, "icon.ico")

    assert os.path.exists(png_path), f"Missing icon asset: {png_path}"
    assert os.path.exists(ico_path), f"Missing icon asset: {ico_path}"

    pixmap = QPixmap(png_path)
    assert not pixmap.isNull()
    assert pixmap.width() == 256
    assert pixmap.height() == 256

    icon = QIcon(png_path)
    assert not icon.isNull()


def test_preferences_save_and_load():
    """Verify settings persistence across calculator state sessions."""
    test_settings = QSettings("OpenScientific_Test", "TestPreferences")
    test_settings.clear()

    prefs = PreferencesManager(test_settings)

    # 1. Save custom state
    state = CalculatorState(
        angle_unit="RAD",
        display_format="LineIO",
        number_format="Fix 4",
        complex_format="r∠θ",
        stat_frequency_on=True,
    )
    prefs.save_state(state)

    # 2. Load into fresh state
    fresh_state = CalculatorState()
    prefs.load_into_state(fresh_state)

    assert fresh_state.angle_unit == "RAD"
    assert fresh_state.display_format == "LineIO"
    assert fresh_state.number_format == "Fix 4"
    assert fresh_state.complex_format == "r∠θ"
    assert fresh_state.stat_frequency_on is True

    # 3. Geometry persistence
    prefs.save_window_geometry(width=520, height=800, x=150, y=120)
    geom = prefs.get_window_geometry()
    assert geom is not None
    assert geom["width"] == 520
    assert geom["height"] == 800
    assert geom["x"] == 150
    assert geom["y"] == 120

    # 4. Clean up
    prefs.reset_defaults()
    assert prefs.get_window_geometry() is None
    test_settings.clear()


def test_configurable_keyboard_shortcuts():
    """Verify custom user shortcut overrides function properly."""
    clear_custom_shortcuts()

    # Register custom shortcut: 'q' -> 'sqrt'
    register_custom_shortcut("q", "sqrt")

    event_q = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Q, Qt.KeyboardModifier.NoModifier, "q")
    assert key_to_id(event_q) == "sqrt"

    # Reset shortcuts
    clear_custom_shortcuts()
    assert key_to_id(event_q) is None


def test_main_window_with_preferences_and_icon(application):
    """Verify MainWindow initializes with preferences, icon, and handles close event."""
    test_settings = QSettings("OpenScientific_Test", "TestMainWindow")
    test_settings.clear()
    prefs = PreferencesManager(test_settings)

    window = MainWindow(preferences=prefs)
    window.show()
    application.processEvents()

    assert window.isVisible()
    assert not window.windowIcon().isNull()

    # Close and verify geometry saved
    window.close()
    application.processEvents()

    geom = prefs.get_window_geometry()
    assert geom is not None
    assert geom["width"] >= 470
    assert geom["height"] >= 690

    test_settings.clear()
