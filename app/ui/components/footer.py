import customtkinter as ctk
from utils.theme import *


def create_footer(parent):
    footer = ctk.CTkFrame(parent, fg_color=BACKGROUND, height=40)
    footer.pack(side="bottom", fill="x")

    ctk.CTkLabel(
        footer,
        text="© 2025 Thiago Aciole. Todos os direitos reservados.",
        text_color=TEXT_SECONDARY,
        font=(FONT_FAMILY, FONT_SIZE_SM),
    ).pack(pady=10)

    return footer
