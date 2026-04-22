from components.chat.chat_history_component import ChatHistoryComponent


class ChatHistoryController:
    def __init__(self, component: ChatHistoryComponent) -> None:
        self.component = component

    def render_messages(self, items: list[dict[str, str]]) -> None:
        self.component.set_message_items(items)