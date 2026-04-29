# main.py

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from app.main_controller import MainController


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = QMainWindow()
    apply_styles(window)
    controller = MainController(window)
    window.show()

    sys.exit(app.exec())

def apply_styles(window) -> None:
    with open("styles/theme_01_slate_indigo.qss", "r") as f:
        window.setStyleSheet(f.read())

if __name__ == "__main__":
    main()