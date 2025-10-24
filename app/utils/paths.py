import os
import sys


def get_base_path():
    """Retorna o caminho base da aplicação."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_external_root():
    """Raiz das pastas externas (/roms, /covers, /game)."""
    base = get_base_path()
    if base.endswith("app"):
        base = os.path.dirname(base)
    return base


def get_app_path(subdir: str, name: str = ""):
    return os.path.join(get_base_path(), subdir, name)


def _resolve_asset(subfolder: str, name: str):
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        path = os.path.join(base, "app", "assets", subfolder, name)
    else:
        path = os.path.join(os.path.dirname(__file__), "..", "assets", subfolder, name)
    return os.path.abspath(path)


def get_asset_path(name: str = ""):
    return _resolve_asset("", name)


def get_icon_path(name: str):
    return _resolve_asset("icons", name)


def get_button_path(name: str):
    return _resolve_asset(os.path.join("icons", "buttons"), name)


def get_setting_path(name: str = ""):
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        path = os.path.join(base, "app", "settings", name)
    else:
        path = os.path.join(os.path.dirname(__file__), "..", "settings", name)
    return os.path.abspath(path)


def get_rom_path(name: str = ""):
    path = os.path.join(get_external_root(), "roms")
    os.makedirs(path, exist_ok=True)
    return os.path.join(path, name)


def get_cover_path(name: str = ""):
    path = os.path.join(get_external_root(), "covers")
    os.makedirs(path, exist_ok=True)
    return os.path.join(path, name)


def get_emulator_path(name: str = ""):
    path = os.path.join(get_external_root(), "game")
    os.makedirs(path, exist_ok=True)
    return os.path.join(path, name)
