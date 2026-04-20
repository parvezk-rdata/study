import streamlit as st

from ui.events import ClearConversationEvent, RemovePdfEvent


class SidebarComponent:
    def render(self):
        with st.sidebar:
            st.header("Session")

            if st.button("Clear conversation"):
                return ClearConversationEvent()

            if st.button("Remove PDF"):
                return RemovePdfEvent()

        return None