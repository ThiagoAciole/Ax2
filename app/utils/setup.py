import os
import shutil

import py7zr
import requests
from utils.constants import *
from utils.theme import *

from .paths import get_cover_path, get_emulator_path, get_rom_path, get_setting_path


def prepare_emulator(progress_callback=None, status_callback=None):
    game_dir = get_emulator_path("")
    rom_dir = get_rom_path("")
    cover_dir = get_cover_path("")

    os.makedirs(game_dir, exist_ok=True)
    os.makedirs(rom_dir, exist_ok=True)
    os.makedirs(cover_dir, exist_ok=True)

    try:
        # === Copiar arquivos padrão ===
        default_src = get_setting_path("default.png")
        default_dest = os.path.join(cover_dir, "default.png")
        if os.path.exists(default_src) and not os.path.exists(default_dest):
            shutil.copy(default_src, default_dest)

        games_src = get_setting_path("games.json")
        games_dest = os.path.join(rom_dir, "games.json")
        if os.path.exists(games_src) and not os.path.exists(games_dest):
            shutil.copy(games_src, games_dest)

        # === Copiar BIOS → game/bios/
        bios_dir = os.path.join(game_dir, "bios")
        os.makedirs(bios_dir, exist_ok=True)
        bios_files = [
            "scph10000-jp.bin",
            "scph50009-cn.bin",
            "scph77001-us.bin",
            "scph77004-eu.bin",
        ]
        for bios_name in bios_files:
            bios_src = get_setting_path(bios_name)
            bios_dest = os.path.join(bios_dir, bios_name)
            if os.path.exists(bios_src) and not os.path.exists(bios_dest):
                shutil.copy(bios_src, bios_dest)

        # === Copiar PCSX2.ini → game/inis/
        inis_dir = os.path.join(game_dir, "inis")
        os.makedirs(inis_dir, exist_ok=True)
        ini_src = get_setting_path("PCSX2.ini")
        ini_dest = os.path.join(inis_dir, "PCSX2.ini")
        if os.path.exists(ini_src) and not os.path.exists(ini_dest):
            shutil.copy(ini_src, ini_dest)

    except Exception as e:
        print(f"[WARN] Falha ao copiar arquivos padrão: {e}")

    # === Verificar se PCSX2 já existe ===
    pcsx2_exe = next(
        (f for f in os.listdir(game_dir) if f.lower().startswith("pcsx2") and f.endswith(".exe")),
        None,
    )
    if pcsx2_exe:
        if status_callback:
            status_callback("PCSX2 encontrado e pronto.")
        return

    # === Baixar PCSX2 se não estiver presente ===
    if status_callback:
        status_callback("Baixando PCSX2...")

    url = "https://github.com/PCSX2/pcsx2/releases/download/v2.4.0/pcsx2-v2.4.0-windows-x64-Qt.7z"
    temp_path = os.path.join(game_dir, "pcsx2.7z")

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            baixado = 0
            with open(temp_path, "wb") as f:
                for chunk in r.iter_content(1024 * 256):
                    if chunk:
                        f.write(chunk)
                        baixado += len(chunk)
                        if progress_callback and total > 0:
                            progress_callback(baixado / total)

        if status_callback:
            status_callback("Extraindo PCSX2...")

        with py7zr.SevenZipFile(temp_path, mode="r") as z:
            z.extractall(path=game_dir)
        os.remove(temp_path)

    except Exception as e:
        if status_callback:
            status_callback(f"Erro ao baixar PCSX2: {e}")
        return
    
    # === Cria portable.txt ===
    portable_path = os.path.join(game_dir, "portable.txt")
    if not os.path.exists(portable_path):
        open(portable_path, "w").close()

    if status_callback:
        status_callback("PCSX2 instalado e estrutura pronta ✅")
