"""Interactive tabular editor for STAT, MATRIX, VECTOR, and TABLE modes."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from src.core.state import CalculatorState

class TableView(QTableWidget):
    """Grid display and editor for matrix, statistical, and tabular data."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("grid_editor")
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setDefaultSectionSize(28)
        self.setAlternatingRowColors(True)
        self.setStyleSheet("""
            QTableWidget#grid_editor {
                background: #cbdac7;
                color: #17271f;
                font: 14px 'Consolas';
                border: 2px solid #859b8b;
                border-radius: 6px;
                gridline-color: #a8bba8;
            }
            QHeaderView::section {
                background: #b2c5af;
                color: #17271f;
                font: bold 12px 'Consolas';
                border: 1px solid #859b8b;
                padding: 2px;
            }
        """)

    def update_grid(self, state: CalculatorState) -> None:
        """Refreshes table content based on calculator state."""
        if not state.table_editor_active or not state.grid_data:
            self.setVisible(False)
            return

        self.setVisible(True)
        rows = len(state.grid_data)
        cols = len(state.grid_headers) if state.grid_headers else (len(state.grid_data[0]) if rows > 0 else 0)

        self.setRowCount(rows)
        self.setColumnCount(cols)

        if state.grid_headers:
            self.setHorizontalHeaderLabels(state.grid_headers)

        for r_idx, row in enumerate(state.grid_data):
            for c_idx, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(r_idx, c_idx, item)

        # Highlight current active cell
        if 0 <= state.grid_row < rows and 0 <= state.grid_col < cols:
            self.setCurrentCell(state.grid_row, state.grid_col)
