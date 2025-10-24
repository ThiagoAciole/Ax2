from customtkinter import CTkImage
from PIL import Image

from .paths import get_button_path, get_icon_path


def load_ctk_image(name: str, size=(24, 24)):
    try:
        img = Image.open(get_icon_path(name))
        return CTkImage(light_image=img, dark_image=img, size=size)
    except Exception:
        return None


def load_button_image(name: str, size=(24, 24)):
    try:
        img = Image.open(get_button_path(name))
        return CTkImage(light_image=img, dark_image=img, size=size)
    except Exception:
        return None


def load_icons():
    return {
        "refresh": load_ctk_image("icon_refresh.png", (32, 32)),
        "search": load_ctk_image("icon_search.png", (32, 32)),
        "edit": load_ctk_image("icon_edit.png", (24, 24)),
        "trash": load_ctk_image("icon_trash.png", (24, 24)),
        "download": load_ctk_image("icon_download.png", (32, 32)),
        "config": load_ctk_image("icon_settings.png", (32, 32)),
        "check": load_ctk_image("icon_check.png", (40, 40)),
        "store": load_ctk_image("icon_store.png", (32, 32)),
        "auto": load_ctk_image("icon_auto.png", (32, 32)),
        "clear": load_ctk_image("icon_clear.png", (32, 32)),
    }
