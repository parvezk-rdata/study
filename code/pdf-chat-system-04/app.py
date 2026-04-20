import streamlit as st

from controllers.main_controller import MainController
from ui.ui_controller import UIController
from ui.ui_state_store import UIStateStore


def main() -> None:
    st.set_page_config(page_title="PDF Chat", page_icon="📄")
    st.title("Chat with a PDF")

    store = UIStateStore()
    store.init_state()

    ui = UIController()
    controller = MainController(store)

    events = ui.collect_events(has_document=store.get_doc() is not None)

    for event in events:
        controller.handle_event(event)

    # render pdf details if re-run happens
    doc = store.get_doc()
    if doc is not None:
        ui.render_document_info(
            filename=store.get_doc_name(),
            doc=doc,
            is_truncated=store.get_is_truncated(),
        )

    # render old chats if re-run happens
    ui.render_chat_history(store.get_history())


if __name__ == "__main__":
    main()