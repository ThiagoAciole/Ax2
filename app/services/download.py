import os
import re
import subprocess
import tempfile
import threading

from utils.paths import get_cover_path, get_rom_path


def normalize_name(texto: str):
    # Remove caracteres inválidos e mantém nome limpo.
    texto = re.sub(r'[<>:"/\\|?*]', "", texto)
    return texto.strip() or "Jogo"


def cleanup_files(base_nome):
    # Remove CHD e capa se download for cancelado ou falhar.
    caminhos = [
        os.path.join(get_rom_path(""), f"{base_nome}.chd"),
        os.path.join(get_cover_path(""), f"{base_nome}.png"),
    ]
    for caminho in caminhos:
        try:
            if os.path.exists(caminho):
                os.remove(caminho)
        except Exception:
            pass


def download_game(jogo, botao, update_log, refresh_callback, linha, icon_check):

    def run():
        nome = jogo.get("name", "Jogo")
        link_chd = jogo.get("game", "")
        capa_link = jogo.get("cover", "")
        base_nome = normalize_name(nome)

        try:
            linha.after(0, lambda: botao.configure(state="disabled"))

            rom_dir = os.path.abspath(get_rom_path(""))
            capa_dir = os.path.abspath(get_cover_path(""))

            os.makedirs(rom_dir, exist_ok=True)
            os.makedirs(capa_dir, exist_ok=True)

            destino_final = os.path.join(rom_dir, f"{base_nome}.chd")
            os.path.join(capa_dir, f"{base_nome}.png")

            # === Centralizar CMD ===
            try:
                import tkinter as tk

                root = tk.Tk()
                root.withdraw()
                screen_w = root.winfo_screenwidth()
                screen_h = root.winfo_screenheight()
                root.destroy()
            except Exception:
                screen_w, screen_h = 1280, 720

            cols, lines = 90, 25
            px_w, px_h = cols * 9, lines * 16
            (screen_w - px_w) // 2
            (screen_h - px_h) // 2

            # === Criar script .BAT completo ===
            script_path = os.path.join(tempfile.gettempdir(), f"download_{base_nome}.bat")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(
                    f"""@echo off
chcp 65001 >nul
title Baixando {nome}
mode con: cols={cols} lines={lines}
color 0A

echo =====================================================
echo   🎮 Baixando: {nome}
echo =====================================================
echo.
cd /d "{rom_dir}"

echo Baixando jogo principal (.CHD)...
python -m gdown "{link_chd}" -O "{destino_final}" --fuzzy --no-cookies
if not exist "{destino_final}" (
    echo [ERRO] Falha no download do jogo.
    pause
    exit /b 1
)
"""
                )

                # === Baixar capa dentro do CMD ===
                if capa_link:
                    f.write(
                        f"""
echo.
echo Baixando capa...
cd /d "{capa_dir}"
python -m gdown "{capa_link}" -O "{base_nome}.png" --fuzzy --no-cookies
if not exist "{base_nome}.png" (
    echo [ERRO] Falha ao baixar capa.
    pause
    exit /b 1
)
cd /d "{rom_dir}"
"""
                    )

                f.write(
                    """
echo.
echo =====================================================
echo ✅ Jogo e capa baixados com sucesso!
echo =====================================================
timeout /t 2 >nul
exit /b 0
"""
                )

            # === Executar CMD e aguardar ===
            cmd_command = f'start /WAIT "" cmd /c "{script_path}"'
            processo = subprocess.Popen(
                cmd_command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            processo.wait()

            # === Após CMD ===
            if os.path.exists(destino_final):
                linha.after(
                    0,
                    lambda: (
                        update_log(f"Instalação concluída: {nome}"),
                        botao.configure(state="disabled", image=icon_check),
                        refresh_callback() if refresh_callback else None,
                    ),
                )
            else:
                cleanup_files(base_nome)
                linha.after(
                    0,
                    lambda: (
                        update_log(f"Falha ao instalar {nome}."),
                        botao.configure(state="normal"),
                    ),
                )

        except Exception:
            cleanup_files(base_nome)
            linha.after(
                0, lambda: (update_log("Erro ao baixar jogo."), botao.configure(state="normal"))
            )

    threading.Thread(target=run, daemon=True).start()
