from __future__ import annotations

from pydantic import BaseModel


class SidebarEvent(BaseModel):
    """Raw values captured from every sidebar widget in a single render pass."""
    mode: str = "API key"
    model: str = ""
    sign_in_clicked: bool = False
    sign_out_clicked: bool = False
    cancel_login_clicked: bool = False
    clear_conversation_clicked: bool = False
    remove_pdf_clicked: bool = False
