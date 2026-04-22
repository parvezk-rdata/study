from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QWidget


class FileDialogComponent(QWidget):
    file_selected = pyqtSignal(str)

    def open_pdf_dialog(self, parent: QWidget) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Select PDF",
            "",
            "PDF Files (*.pdf)",
        )

        if file_path:
            self.file_selected.emit(file_path)