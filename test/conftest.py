import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import pytest
from PySide6.QtWidgets import QApplication
from src.core.controller import Controller

@pytest.fixture(scope="session")
def application():
    app = QApplication.instance() or QApplication([])
    yield app

@pytest.fixture
def controller():
    return Controller()
