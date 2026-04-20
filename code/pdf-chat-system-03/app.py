import hashlib
import streamlit as st

from llm_client import chat, fit_pdf_to_context
from pdf_extractor import ExtractedDoc, extract
from ui.ui_controller import UIController
from ui.ui_state_store import UIStateStore


def file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def handle_uploaded_pdf(
    uploaded_file,
    store: UIStateStore,
) -> ExtractedDoc | None:
    if uploaded_file is None:
        return store.get_doc()

    data = uploaded_file.getvalue()
    current_hash = file_hash(data)

    if store.get_doc_hash() == current_hash:
        return store.get_doc()

    with st.spinner("Extracting text..."):
        try:
            doc = extract(data)
        except RuntimeError as e:
            st.error(str(e))
            return None

    store.set_doc(doc)
    store.set_doc_hash(current_hash)
    store.set_doc_name(uploaded_file.name)
    store.clear_conversation()
    return doc


def handle_user_prompt(
    doc: ExtractedDoc | None,
    prompt: str | None,
    store: UIStateStore,
) -> None:
    if not prompt:
        return

    if doc is None:
        st.warning("Upload a PDF first.")
        return

    prior_history = list(store.get_history())
    store.append_message("user", prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply = chat(prior_history, doc.text, prompt)
            except RuntimeError as e:
                reply = f"**Error:** {e}"
            except Exception as e:
                reply = f"**Error calling OpenAI:** {e}"

        st.markdown(reply)

    store.append_message("assistant", reply)


def main() -> None:
    st.set_page_config(page_title="PDF Chat", page_icon="📄")
    st.title("Chat with a PDF")

    store = UIStateStore()
    store.init_state()

    ui = UIController()

    sidebar_event = ui.render_sidebar()
    if sidebar_event == "clear_conversation":
        store.clear_conversation()
        st.rerun()
    elif sidebar_event == "remove_pdf":
        store.remove_pdf()
        st.rerun()

    uploaded_file = ui.render_uploader(store.get_uploader_key())
    doc = handle_uploaded_pdf(uploaded_file, store)

    if doc is not None:
        _, truncated = fit_pdf_to_context(doc.text)
        ui.render_document_info(
            filename=store.get_doc_name(),
            doc=doc,
            is_truncated=truncated,
        )

    ui.render_chat_history(store.get_history())

    prompt = ui.render_chat_input(has_document=doc is not None)
    handle_user_prompt(doc, prompt, store)


if __name__ == "__main__":
    main()