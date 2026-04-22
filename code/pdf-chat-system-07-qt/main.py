import sys

from PyQt6.QtWidgets import QApplication

from app import PDFChatApplication


def main() -> None:
    qt_app = QApplication(sys.argv)
    qt_app.setApplicationName("PDF Chat")

    app = PDFChatApplication()
    app.start()

    sys.exit(qt_app.exec())


if __name__ == "__main__":
    main()