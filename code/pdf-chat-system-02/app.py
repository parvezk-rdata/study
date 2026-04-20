import hashlib
import streamlit as st

from llm_client import chat, fit_pdf_to_context
from pdf_extractor import ExtractedDoc, extract
from ui.ui_controller import UIController


def file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def init_state() -> None:
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("uploader_key", 0)
    st.session_state.setdefault("doc", None)
    st.session_state.setdefault("doc_hash", None)
    st.session_state.setdefault("doc_name", None)


def clear_conversation() -> None:
    st.session_state["history"] = []


def remove_pdf() -> None:
    st.session_state["doc"] = None
    st.session_state["doc_hash"] = None
    st.session_state["doc_name"] = None
    st.session_state["history"] = []
    st.session_state["uploader_key"] += 1


def handle_uploaded_pdf(uploaded_file) -> ExtractedDoc | None:
    if uploaded_file is None:
        return st.session_state.get("doc")

    data = uploaded_file.getvalue()
    current_hash = file_hash(data)

    if st.session_state.get("doc_hash") == current_hash:
        return st.session_state.get("doc")

    with st.spinner("Extracting text..."):
        try:
            doc = extract(data)
        except RuntimeError as e:
            st.error(str(e))
            return None

    st.session_state["doc"] = doc
    st.session_state["doc_hash"] = current_hash
    st.session_state["doc_name"] = uploaded_file.name
    st.session_state["history"] = []
    return doc


def handle_user_prompt(doc: ExtractedDoc | None, prompt: str | None) -> None:
    if not prompt:
        return

    if doc is None:
        st.warning("Upload a PDF first.")
        return

    prior_history = list(st.session_state["history"])
    st.session_state["history"].append({"role": "user", "content": prompt})

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

    st.session_state["history"].append({"role": "assistant", "content": reply})


def main() -> None:
    st.set_page_config(page_title="PDF Chat", page_icon="📄")
    st.title("Chat with a PDF")

    init_state()

    ui = UIController()

    sidebar_event = ui.render_sidebar()
    if sidebar_event == "clear_conversation":
        clear_conversation()
        st.rerun()
    elif sidebar_event == "remove_pdf":
        remove_pdf()
        st.rerun()

    uploaded_file = ui.render_document_uploader(st.session_state["uploader_key"])
    doc = handle_uploaded_pdf(uploaded_file)

    if doc is not None:
        _, truncated = fit_pdf_to_context(doc.text)
        ui.render_document_summary(
            filename=st.session_state.get("doc_name"),
            doc=doc,
            is_truncated=truncated,
        )

    ui.render_chat_history(st.session_state["history"])

    prompt = ui.render_chat_input(has_document=doc is not None)
    handle_user_prompt(doc, prompt)


if __name__ == "__main__":
    main()