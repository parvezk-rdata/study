import streamlit as st


class SidebarComponent:
    def render(self) -> str | None:
        with st.sidebar:
            st.header("Session")

            if st.button("Clear conversation"):
                return "clear_conversation"

            if st.button("Remove PDF"):
                return "remove_pdf"

        return None