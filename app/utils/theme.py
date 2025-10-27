import os

import customtkinter as ctk
from utils.constants import *
from utils.paths import get_asset_path

# 🎨 COLORS
PRIMARY_COLOR = "#1F7FFF"  # Roxo principal
PRIMARY_HOVER = "#48B7FF"  # Hover / destaque
SURFACE_HOVER = "#3D3D3D"
BACKGROUND = "#202020"
BACKGROUND_DARK = "#121212"  # Fundo base
SURFACE = "#1e1e1e"  # Containers, frames
SURFACE_LIGHT = "#2b2b2b"  # Barras, inputs, etc
TEXT_PRIMARY = "#ffffff"  # Texto principal
TEXT_SECONDARY = "#aaaaaa"  # Texto secundário
TEXT_MUTED = "#777777"  # Texto apagado
SUCCESS = "#50fa7b"  # Verde de sucesso
ERROR = "#ff5555"  # Vermelho
CLEAR = "#eba8a8"
WARNING = "#f1fa8c"  # Amarelo
TRANSPARENT = "transparent"  # Transparente

# 🧱 SPACING AND BORDERS
RADIUS = 10
PADDING = 10
SPACING = 8

# 🖋️ FONTS
FONT_FAMILY = "Segoe UI"
FONT_SIZE_SM = 12
FONT_SIZE_MD = 14
FONT_SIZE_LG = 18
FONT_WEIGHT_BOLD = "bold"
TITLE_GAME = (FONT_FAMILY, FONT_SIZE_SM, FONT_WEIGHT_BOLD)


def create_window(
    parent=None,
    title: str = APP_NAME,
    width: int = 1100,
    height: int = 800,
    min_width: int = 800,
    min_height: int = 600,
    resizable: bool = True,
    fullscreen: bool = False,
    bg: str = BACKGROUND,
):
    # === Define o tipo de janela ===
    window = ctk.CTkToplevel(parent) if parent else ctk.CTk()

    ctk.set_appearance_mode("dark")
    window.title(title)
    window.configure(fg_color=bg)

    # === Centraliza a janela ===
    def center_window():
        window.update_idletasks()
        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
        pos_x = (screen_w // 2) - (width // 2)
        pos_y = (screen_h // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    if fullscreen:
        window.attributes("-fullscreen", True)
    else:
        center_window()

    window.minsize(min_width, min_height)
    window.resizable(resizable, resizable)

    # === Ícone da janela ===
    try:
        icon_path = get_asset_path(ICON_NAME)
        if os.path.exists(icon_path):
            window.iconbitmap(icon_path)
        else:
            alt_icon = get_asset_path(ICON_NAME)
            if os.path.exists(alt_icon):
                from PIL import Image, ImageTk

                icon_img = Image.open(alt_icon)
                window.iconphoto(False, ImageTk.PhotoImage(icon_img))
    except Exception as e:
        print(f"[WARN] Failed to set window icon: {e}")

    # === Configuração adicional para janelas filhas ===
    if parent:
        window.transient(parent)
        window.grab_set()
        window.focus_force()
        window.lift()
        window.attributes("-topmost", True)
        window.after(200, lambda: window.attributes("-topmost", False))
        try:
            window.iconbitmap(get_asset_path(ICON_NAME))
        except Exception:
            pass

    return window
