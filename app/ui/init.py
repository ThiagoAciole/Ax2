import os
import threading

import customtkinter as ctk
from PIL import Image
from ui.home import start_home
from utils.constants import *
from utils.paths import get_asset_path, get_cover_path, get_rom_path
from utils.setup import prepare_emulator
from utils.theme import *


def start_init():
    window = create_window(
        title=APP_NAME,
        width=600,
        height=400,
        min_width=600,
        min_height=400,
        resizable=False,
    )

    # === CONTAINER PRINCIPAL ===
    container = ctk.CTkFrame(window, fg_color=TRANSPARENT)
    container.pack(expand=True, fill="both")

    # === LOGO OU TEXTO PADRÃO ===
    logo_path = get_asset_path("logo.png")
    if os.path.exists(logo_path):
        logo_image = ctk.CTkImage(Image.open(logo_path), size=(140, 140))
        ctk.CTkLabel(container, image=logo_image, text="").pack(expand=True, pady=(40, 10))
    else:
        ctk.CTkLabel(
            container,
            text=DEFAULT_LABEL,
            font=(FONT_FAMILY, FONT_SIZE_LG, "bold"),
            text_color=PRIMARY_COLOR,
        ).pack(expand=True, pady=(40, 10))

    # === STATUS LABEL ===
    status_label = ctk.CTkLabel(
        container,
        text=STATUS_PREPARING,
        text_color=TEXT_PRIMARY,
        font=(FONT_FAMILY, FONT_SIZE_MD),
    )
    status_label.pack(pady=(10, 8))

    # === BARRA DE PROGRESSO ===
    progress_bar = ctk.CTkProgressBar(
        container,
        width=400,
        height=6,
        corner_radius=20,
        fg_color=SURFACE_LIGHT,
        progress_color=PRIMARY_COLOR,
        mode="indeterminate",
    )
    progress_bar.pack(pady=(0, 20))
    progress_bar.start()

    # === CALLBACKS VISUAIS ===
    def update_progress(value: float):
        window.after(0, lambda: progress_bar.set(value))

    def update_status(text: str):
        window.after(0, lambda: status_label.configure(text=text))

    # === FLUXO DE INICIALIZAÇÃO ===
    def prepare():
        os.makedirs(get_rom_path(""), exist_ok=True)
        os.makedirs(get_cover_path(""), exist_ok=True)

        update_status(STATUS_LOADING)
        prepare_emulator(progress_callback=update_progress, status_callback=update_status)

        def close_window():
            try:
                progress_bar.stop()
            except Exception:
                pass

            try:
                for after_id in window.tk.call("after", "info"):
                    window.after_cancel(after_id)
            except Exception:
                pass

            if window.winfo_exists():
                window.destroy()
            start_home()

        # Fecha a janela após 1 segundo
        window.after(1000, close_window)

    threading.Thread(target=prepare, daemon=True).start()
    window.mainloop()


if __name__ == "__main__":
    start_init()
