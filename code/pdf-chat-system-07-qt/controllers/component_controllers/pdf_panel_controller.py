from components.document.pdf_panel_component import PDFPanelComponent


class PDFPanelController:
    def __init__(self, component: PDFPanelComponent) -> None:
        self.component = component

    def set_static_texts(
        self,
        title_text: str,
        upload_button_text: str,
        clear_chat_button_text: str,
        remove_pdf_button_text: str,
    ) -> None:
        self.component.set_title_text(title_text)
        self.component.set_upload_button_text(upload_button_text)
        self.component.set_clear_chat_button_text(clear_chat_button_text)
        self.component.set_remove_pdf_button_text(remove_pdf_button_text)

    def apply_title_style(self, style: str) -> None:
        self.component.get_title_label().setStyleSheet(style)

    def render_file_text(self, text: str) -> None:
        self.component.set_file_text(text)

    def render_info_text(self, text: str) -> None:
        self.component.set_info_text(text)

    def set_file_visible(self, visible: bool) -> None:
        self.component.get_file_label().setVisible(visible)

    def set_info_visible(self, visible: bool) -> None:
        self.component.get_info_label().setVisible(visible)

    def set_clear_chat_enabled(self, enabled: bool) -> None:
        self.component.get_clear_chat_button().setEnabled(enabled)

    def set_remove_pdf_enabled(self, enabled: bool) -> None:
        self.component.get_remove_pdf_button().setEnabled(enabled)