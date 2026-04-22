from components.document.pdf_panel_component import PDFPanelComponent


class PDFPanelController:
    def __init__(self, component: PDFPanelComponent) -> None:
        self.component = component

    def initialize_component(
        self,
        title_text: str,
        upload_button_text: str,
        clear_chat_button_text: str,
        remove_pdf_button_text: str,
        title_style: str,
    ) -> None:
        self.component.set_title_text(title_text)
        self.component.set_upload_button_text(upload_button_text)
        self.component.set_clear_chat_button_text(clear_chat_button_text)
        self.component.set_remove_pdf_button_text(remove_pdf_button_text)
        self.component.get_title_label().setStyleSheet(title_style)

    def handle_no_pdf_state(
        self,
        file_text: str,
        info_text: str,
    ) -> None:
        self.component.set_file_text(file_text)
        self.component.set_info_text(info_text)

        self.component.get_file_label().setVisible(True)
        self.component.get_info_label().setVisible(True)

        self.component.get_clear_chat_button().setEnabled(False)
        self.component.get_remove_pdf_button().setEnabled(False)

    def handle_pdf_loaded(
        self,
        file_text: str,
        info_text: str,
    ) -> None:
        self.component.set_file_text(file_text)
        self.component.set_info_text(info_text)

        self.component.get_file_label().setVisible(True)
        self.component.get_info_label().setVisible(True)

        self.component.get_clear_chat_button().setEnabled(True)
        self.component.get_remove_pdf_button().setEnabled(True)

    def handle_pdf_removed(
        self,
        file_text: str,
        info_text: str,
    ) -> None:
        self.component.set_file_text(file_text)
        self.component.set_info_text(info_text)

        self.component.get_file_label().setVisible(True)
        self.component.get_info_label().setVisible(True)

        self.component.get_clear_chat_button().setEnabled(False)
        self.component.get_remove_pdf_button().setEnabled(False)

    def handle_chat_cleared(
        self,
        file_text: str,
        info_text: str,
    ) -> None:
        self.component.set_file_text(file_text)
        self.component.set_info_text(info_text)

        self.component.get_file_label().setVisible(True)
        self.component.get_info_label().setVisible(True)

        self.component.get_clear_chat_button().setEnabled(True)
        self.component.get_remove_pdf_button().setEnabled(True)