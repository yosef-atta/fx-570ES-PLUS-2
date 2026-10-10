"""Persistent settings and user preference manager for fx-570ES PLUS 2."""
import os
from PySide6.QtCore import QSettings
from src.core.state import CalculatorState
from src.version import ORGANIZATION, APP_SHORT_NAME


class PreferencesManager:
    """Handles persistent settings across application launches using QSettings."""

    def __init__(self, settings: QSettings | None = None):
        if settings is not None:
            self.settings = settings
        elif os.environ.get("PYTEST_CURRENT_TEST"):
            # Isolate settings during automated testing to avoid polluting host registry
            self.settings = QSettings("OpenScientific_TestRunner", "IsolatedScope")
            self.settings.clear()
        else:
            self.settings = QSettings(ORGANIZATION, APP_SHORT_NAME)

    def load_into_state(self, state: CalculatorState) -> None:
        """Applies stored preferences to the given calculator state."""
        state.angle_unit = str(self.settings.value("setup/angle_unit", state.angle_unit))
        state.display_format = str(self.settings.value("setup/display_format", state.display_format))
        state.number_format = str(self.settings.value("setup/number_format", state.number_format))
        state.complex_format = str(self.settings.value("setup/complex_format", state.complex_format))
        freq = self.settings.value("setup/stat_frequency_on", state.stat_frequency_on)
        if isinstance(freq, str):
            state.stat_frequency_on = freq.lower() in ("true", "1")
        else:
            state.stat_frequency_on = bool(freq)

    def save_state(self, state: CalculatorState) -> None:
        """Persists setup options from calculator state."""
        self.settings.setValue("setup/angle_unit", state.angle_unit)
        self.settings.setValue("setup/display_format", state.display_format)
        self.settings.setValue("setup/number_format", state.number_format)
        self.settings.setValue("setup/complex_format", state.complex_format)
        self.settings.setValue("setup/stat_frequency_on", state.stat_frequency_on)
        self.settings.sync()

    def save_window_geometry(self, width: int, height: int, x: int | None = None, y: int | None = None) -> None:
        """Saves window dimensions and screen coordinates."""
        self.settings.setValue("window/width", width)
        self.settings.setValue("window/height", height)
        if x is not None and y is not None:
            self.settings.setValue("window/x", x)
            self.settings.setValue("window/y", y)
        self.settings.sync()

    def get_window_geometry(self) -> dict | None:
        """Retrieves previously saved window geometry, if available."""
        if self.settings.contains("window/width") and self.settings.contains("window/height"):
            width = int(self.settings.value("window/width", 500))
            height = int(self.settings.value("window/height", 780))
            x = self.settings.value("window/x", None)
            y = self.settings.value("window/y", None)
            return {
                "width": max(470, width),
                "height": max(690, height),
                "x": int(x) if x is not None else None,
                "y": int(y) if y is not None else None,
            }
        return None

    def reset_defaults(self) -> None:
        """Clears all stored preferences and restores factory defaults."""
        self.settings.clear()
        self.settings.sync()
