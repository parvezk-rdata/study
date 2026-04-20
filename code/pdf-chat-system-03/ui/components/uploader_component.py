import streamlit as st


class UploaderComponent:
    def render(self, uploader_key: int):
        return st.file_uploader(
            "Upload a PDF",
            type=["pdf"],
            key=f"uploader_{uploader_key}",
        )