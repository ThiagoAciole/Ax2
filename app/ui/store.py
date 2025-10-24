import json
import os
import zipfile
from tkinter import messagebox

import customtkinter as ctk
import gdown
from ui.components.game_store_card import GameStoreCard
from ui.components.search_input import SearchInput
from utils.constants import *
from utils.icons import load_icons
from utils.paths import get_rom_path


def build_store_drawer(frame, refresh_callback=None):
    """Constrói o drawer da loja de jogos com busca e listagem."""
    # --- Limpa o conteúdo existente ---
    for w in frame.winfo_children():
        w.destroy()

    frame.configure(fg_color="#121212")

    # --- Ícones e cores ---
    icons = load_icons()

    # --- HEADER ---
    header = ctk.CTkFrame(frame, fg_color="#121212", height=70)
    header.pack(fill="x", pady=(10, 0))
    header.pack_propagate(False)

    header_inner = ctk.CTkFrame(header, fg_color="transparent")
    header_inner.pack(fill="x", expand=True, padx=20, pady=10)

    # === Atualizar lista de jogos via Google Drive ===
    def update_game_list():
        try:
            rom_dir = get_rom_path("")
            zip_path = os.path.join(rom_dir, "games.zip")

            update_log(STATUS_UPDATING_LIST)

            file_id = "1kK8h2n9696iZH9pN5HV2KTIwYHj5W2p3"
            url = f"https://drive.google.com/uc?id={file_id}"

            # Baixar o arquivo ZIP
            gdown.download(url, zip_path, quiet=False, fuzzy=True)

            if not os.path.exists(zip_path):
                raise FileNotFoundError(FILE_NOT_FOUND.format(nome="games.zip"))

            # Extrair o JSON dentro de /roms
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(rom_dir)
            os.remove(zip_path)

            update_log(STATUS_UPDATE_SUCCESS)

            # Recarregar lista após atualização
            nonlocal all_games
            all_games = load_local_list()
            filter_and_display()

        except Exception as e:
            messagebox.showerror("Erro", STATUS_UPDATE_ERROR + f"\n{e}")

    # --- Campo de busca ---
    def on_search_change(text: str):
        filter_and_display(text)

    search_input = SearchInput(
        header_inner,
        on_change=on_search_change,
        on_refresh=update_game_list,  # callback do botão de atualizar
    )
    search_input.pack(side="left", fill="x", expand=True)

    # --- SCROLL CONTAINER ---
    frame_scroll = ctk.CTkScrollableFrame(frame, fg_color="#121212", corner_radius=12)
    frame_scroll.pack(fill="both", expand=True, padx=10, pady=5)

    # --- LABEL DE STATUS ---
    status_label = ctk.CTkLabel(frame, text="", font=("Segoe UI", 12), text_color="gray")
    status_label.pack(pady=(4, 4))

    def update_log(msg):
        status_label.configure(text=msg)
        status_label.update_idletasks()

    # === Carregar lista local ===
    def load_local_list():
        try:
            json_path = os.path.join(get_rom_path(""), "games.json")

            if not os.path.exists(json_path):
                messagebox.showerror("Erro", FILE_NOT_FOUND.format(nome="games.json"))
                return []

            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                messagebox.showerror("Erro", INVALID_JSON)
                return []

            valid_games = [j for j in data if all(k in j for k in ("game", "name", "size"))]
            return valid_games

        except Exception as e:
            messagebox.showerror("Erro", JSON_LOAD_ERROR.format(erro=e))
            return []

    # === Renderizar jogos ===
    def render_game_list(games):
        for widget in frame_scroll.winfo_children():
            widget.destroy()

        if not games:
            ctk.CTkLabel(
                frame_scroll,
                text=NO_GAMES_FOUND,
                font=("Segoe UI", 14),
                text_color="#888",
            ).pack(pady=20)
            return

        for game in games:
            GameStoreCard(frame_scroll, game, icons, update_log, refresh_callback)

    # === Buscar e listar ===
    all_games = load_local_list()

    def filter_and_display(filter_text=""):
        search_term = filter_text.strip().lower()
        filtered = [g for g in all_games if search_term in g.get("name", "").lower()]
        status_label.configure(text=f"{len(filtered)} jogo(s) encontrado(s)")
        render_game_list(filtered)

    # === Render inicial ===
    filter_and_display()
