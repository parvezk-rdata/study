from components.chat.chat_input_component import ChatInputComponent


class ChatInputController:
    def __init__(self, component: ChatInputComponent) -> None:
        self.component = component

    def set_static_texts(self, send_button_text: str) -> None:
        self.component.set_send_button_text(send_button_text)

    def set_placeholder_text(self, text: str) -> None:
        self.component.set_placeholder_text(text)

    def set_input_enabled(self, enabled: bool) -> None:
        self.component.get_input().setEnabled(enabled)

    def set_send_enabled(self, enabled: bool) -> None:
        self.component.get_send_button().setEnabled(enabled)

    def clear_input(self) -> None:
        self.component.clear_input()