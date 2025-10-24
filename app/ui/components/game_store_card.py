import os

import customtkinter as ctk
from services.download import download_game
from utils.paths import get_rom_path


class GameStoreCard(ctk.CTkFrame):

    def __init__(self, parent, game, icons, update_log, refresh_callback):
        super().__init__(parent, fg_color="#1e1e1e", corner_radius=10, height=70)
        self.pack(fill="x", pady=6, padx=10)
        self.pack_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # === Game Info ===
        self.name = game.get("name", "Unnamed Game")
        self.link = game.get("game", "")
        self.cover = game.get("cover", "")
        self.size = game.get("size", "")
        self.icons = icons
        self.update_log = update_log
        self.refresh_callback = refresh_callback

        # === Info Section ===
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="w", padx=15, pady=(8, 8))

        ctk.CTkLabel(
            info_frame,
            text=self.name,
            font=("Segoe UI", 14, "bold"),
            text_color="white",
        ).pack(anchor="w")

        if self.size:
            ctk.CTkLabel(
                info_frame,
                text=self.size,
                font=("Segoe UI", 12),
                text_color="#aaa",
            ).pack(anchor="w", pady=(0, 2))

        # === Download Button ===
        roms_available = {
            os.path.splitext(f)[0]
            for f in os.listdir(get_rom_path(""))
            if f.lower().endswith(".chd")
        }

        downloaded = self.name in roms_available
        self.btn = ctk.CTkButton(
            self,
            text="",
            image=self.icons["check"] if downloaded else self.icons["download"],
            width=40,
            height=30,
            fg_color="transparent",
        )
        self.btn.grid(row=0, column=1, padx=(0, 20))

        if not downloaded:
            self.btn.configure(command=self._download)
        else:
            self.btn.configure(state="disabled")

    # === Download Function ===
    def _download(self):
        game = {
            "name": self.name,
            "game": self.link,
            "cover": self.cover,
            "size": self.size or "0 MB",
        }

        download_game(
            game,
            self.btn,
            self.update_log,
            self.refresh_callback,
            self,
            self.icons["check"],
        )
