from components.system.file_dialog_component import FileDialogComponent


class FileDialogController:
    def __init__(self, component: FileDialogComponent) -> None:
        self.component = component

    def handle_open_pdf_dialog(self, parent) -> None:
        self.component.open_pdf_dialog(parent)