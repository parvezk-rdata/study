from components.layout.main_window import MainWindow
from controllers.main_controller import MainController


class PDFChatApplication:
    def __init__(self) -> None:
        self.window = MainWindow()
        self.main_controller = MainController( window=self.window )

    def start(self) -> None:
        self._apply_styles()
        self.main_controller.initialize()
        self.window.show()

    def _apply_styles(self) -> None:
        with open("styles/theme_slate_indigo.qss", "r") as f:
            self.window.setStyleSheet(f.read())