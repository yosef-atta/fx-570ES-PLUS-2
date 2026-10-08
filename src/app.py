"""Run with: uv run python -m src.app"""
import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main() -> int:
    application = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return application.exec()

if __name__ == "__main__":
    raise SystemExit(main())
