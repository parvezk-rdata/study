from components.chat.chat_input_component import ChatInputComponent


class ChatInputController:
    def __init__(self, component: ChatInputComponent) -> None:
        self.component = component

    def initialize_component(self, send_button_text: str) -> None:
        self.component.set_send_button_text(send_button_text)

    def handle_no_pdf_state(self, placeholder_text: str) -> None:
        self.component.set_placeholder_text(placeholder_text)
        self.component.get_input().setEnabled(False)
        self.component.get_send_button().setEnabled(False)

    def handle_pdf_loaded(self, placeholder_text: str) -> None:
        self.component.set_placeholder_text(placeholder_text)
        self.component.get_input().setEnabled(True)
        self.component.get_send_button().setEnabled(True)

    def handle_pdf_removed(self, placeholder_text: str) -> None:
        self.component.set_placeholder_text(placeholder_text)
        self.component.get_input().setEnabled(False)
        self.component.get_send_button().setEnabled(False)
        self.component.clear_input()

    def handle_message_sent(self) -> None:
        self.component.clear_input()

    def handle_chat_cleared(self) -> None:
        self.component.clear_input()