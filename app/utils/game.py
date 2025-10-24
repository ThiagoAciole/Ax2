import os
import subprocess
import time
from tkinter import filedialog, messagebox

import keyboard
import pygame
from PIL import Image
from utils.constants import *

from .paths import get_cover_path, get_emulator_path, get_rom_path


def start_game(arquivo):
    try:
        pcsx2_dir = get_emulator_path("")
        pcsx2_exe = next(
            (
                os.path.join(pcsx2_dir, f)
                for f in os.listdir(pcsx2_dir)
                if f.lower().startswith("pcsx2") and f.lower().endswith(".exe")
            ),
            None,
        )

        if not pcsx2_exe or not os.path.exists(pcsx2_exe):
            messagebox.showerror("Erro", "PCSX2 não encontrado em /game/.")
            return

        rom = get_rom_path(arquivo)
        if not os.path.exists(rom):
            messagebox.showerror("Erro", GAME_NOT_FOUND.format(arquivo=arquivo))
            return

        process = subprocess.Popen([pcsx2_exe, "-nogui", "-batch", "-fullscreen", "--", rom])
        print(GAME_START_INFO)

        pygame.init()
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0) if pygame.joystick.get_count() else None

        if joystick:
            print(INFO_CONTROLLER_DETECTED.format(nome=joystick.get_name()))
        else:
            print(WARN_NO_CONTROLLER)

        combo_start, combo_duration = None, 1.0
        btn_x, btn_l1 = 2, 4

        while process.poll() is None:
            if keyboard.is_pressed("esc"):
                process.terminate()
                break

            if joystick:
                pygame.event.pump()
                if joystick.get_button(btn_l1) and joystick.get_button(btn_x):
                    if combo_start is None:
                        combo_start = time.time()
                    elif time.time() - combo_start >= combo_duration:
                        print(INFO_COMBO_EXIT)
                        process.terminate()
                        break
                else:
                    combo_start = None
            time.sleep(0.05)

        pygame.quit()

    except Exception as e:
        pygame.quit()
        messagebox.showerror("Erro", GAME_START_ERROR.format(erro=e))


def change_cover(nome_jogo, refresh_callback=None):
    try:
        arquivo_img = filedialog.askopenfilename(
            title=COVER_SELECT_TITLE.format(jogo=nome_jogo),
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.webp")],
        )
        if not arquivo_img:
            return

        destino = get_cover_path(f"{nome_jogo}.png")
        Image.open(arquivo_img).convert("RGBA").save(destino, "PNG")

        messagebox.showinfo("Capa atualizada", COVER_UPDATED.format(jogo=nome_jogo))
        if refresh_callback:
            refresh_callback()

    except Exception as e:
        messagebox.showerror("Erro", COVER_UPDATE_ERROR.format(erro=e))


def delete_game(nome_jogo, refresh_callback=None):
    try:
        if not messagebox.askyesno("Excluir", GAME_DELETE_CONFIRM.format(jogo=nome_jogo)):
            return

        for ext in (".iso", ".bin", ".img", ".cue", ".chd"):
            path = get_rom_path(f"{nome_jogo}{ext}")
            if os.path.exists(path):
                os.remove(path)

        capa = get_cover_path(f"{nome_jogo}.png")
        if os.path.exists(capa):
            os.remove(capa)

        messagebox.showinfo("Removido", GAME_DELETE_SUCCESS.format(jogo=nome_jogo))
        if refresh_callback:
            refresh_callback()

    except Exception as e:
        messagebox.showerror("Erro", GAME_DELETE_ERROR.format(erro=e))


def search_game():
    jogos = []
    for f in os.listdir(get_rom_path("")):
        if f.lower().endswith((".bin", ".iso", ".img", ".cue", ".chd")):
            title = os.path.splitext(f)[0]
            capa = (
                f"{title}.png" if os.path.isfile(get_cover_path(f"{title}.png")) else "default.png"
            )
            jogos.append({"title": title, "file": f, "image": capa})
    return jogos
