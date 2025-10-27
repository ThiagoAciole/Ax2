import os

import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageOps
from utils.icons import load_icons
from utils.paths import get_asset_path, get_cover_path
from utils.theme import *


class GameCard(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        title: str,
        image: str,
        platform: str = "ps1",
        on_click=None,
        on_edit=None,
        on_delete=None,
        width=130,  # 🔹 Largura ajustada
        height=180,  # 🔹 Altura ajustada
        *args,
        **kwargs,
    ):
        super().__init__(
            parent,
            fg_color=BACKGROUND_DARK,
            corner_radius=8,
            width=width + 20,
            height=height + 40,
        )

        self.pack_propagate(False)
        self.title = title
        self.image = image
        self.platform = platform
        self.on_click = on_click
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.root = self.winfo_toplevel()

        # === Caminhos ===
        cover_path = get_cover_path(self.image)
        if not os.path.exists(cover_path):
            cover_path = get_cover_path("default.png")

        frame_path = get_asset_path("ps1_path.png")
        if not os.path.exists(frame_path):
            raise FileNotFoundError(f"Frame not found: {frame_path}")

        # === Carrega imagens ===
        cover = Image.open(cover_path).convert("RGBA")
        frame = Image.open(frame_path).convert("RGBA")

        margin = 2
        inner_width = width - (margin * 2)
        inner_height = height - (margin * 2)

        # Ajusta proporcionalmente mantendo o aspecto
        cover_fit = ImageOps.contain(cover, (inner_width, inner_height), Image.LANCZOS)

        # Centraliza a capa no espaço total
        composed = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        x = (width - cover_fit.width) // 2
        y = (height - cover_fit.height) // 2
        composed.paste(cover_fit, (x, y))
        frame = frame.resize((width, height), Image.LANCZOS)
        composed.paste(frame, (0, 0), mask=frame)

        # === Cria imagem final ===
        self.tk_image = CTkImage(light_image=composed, dark_image=composed, size=(width, height))

        # === Texto do card ===
        title_text = title if len(title) <= 18 else title[:15] + "..."

        # === Botão principal ===
        self.button = ctk.CTkButton(
            self,
            image=self.tk_image,
            text=title_text,
            compound="top",
            fg_color=TRANSPARENT,
            hover_color="#1D1D1D",
            width=width,
            height=height,
            text_color="white",
            font=TITLE_GAME,
            command=self.on_click,
        )
        self.button.pack(expand=True, fill="both")

        # === Bind botão direito ===
        self.button.bind("<Button-3>", self.open_context_menu)

    # === Menu de contexto (botão direito) ===
    def open_context_menu(self, event):
        root = self.root

        # Fecha qualquer menu existente
        for w in root.winfo_children():
            if isinstance(w, ctk.CTkFrame) and getattr(w, "is_context_menu", False):
                w.destroy()

        menu = ctk.CTkFrame(root, fg_color=BACKGROUND, corner_radius=8)
        menu.is_context_menu = True

        icons = load_icons()
        icon_edit = icons.get("edit")
        icon_trash = icons.get("trash")

        # === Opções ===
        if self.on_edit:
            ctk.CTkButton(
                menu,
                image=icon_edit,
                text="Change Game Cover",
                compound="left",
                font=("Segoe UI", 13, "bold"),
                text_color="white",
                fg_color=BACKGROUND,
                hover_color=SURFACE_LIGHT,
                corner_radius=6,
                width=230,
                height=40,
                anchor="w",
                command=lambda: (menu.destroy(), self.on_edit(self.title)),
            ).pack(padx=1, pady=(6, 3))

        if self.on_delete:
            ctk.CTkButton(
                menu,
                image=icon_trash,
                text="Delete Game",
                compound="left",
                font=("Segoe UI", 13, "bold"),
                text_color="#ff6666",
                fg_color=BACKGROUND,
                hover_color=SURFACE_LIGHT,
                corner_radius=6,
                width=230,
                height=40,
                anchor="w",
                command=lambda: (menu.destroy(), self.on_delete(self.title)),
            ).pack(padx=1, pady=(3, 6))

        # === Posicionamento do menu ===
        widget = event.widget
        widget_x = widget.winfo_rootx() - root.winfo_rootx()
        widget_y = widget.winfo_rooty() - root.winfo_rooty()
        widget_w = widget.winfo_width()
        menu_w = menu.winfo_reqwidth()
        window_w = root.winfo_width()

        pos_x = (
            max(widget_x - menu_w - 10, 0)
            if widget_x + widget_w + menu_w + 20 > window_w
            else widget_x + widget_w + 10
        )

        menu.place(x=pos_x, y=widget_y)

        # Fecha o menu ao clicar fora
        def close_menu(ev):
            if not (
                menu.winfo_x()
                <= ev.x_root - root.winfo_rootx()
                <= menu.winfo_x() + menu.winfo_width()
                and menu.winfo_y()
                <= ev.y_root - root.winfo_rooty()
                <= menu.winfo_y() + menu.winfo_height()
            ):
                menu.destroy()
                root.unbind("<Button-1>")

        root.bind("<Button-1>", close_menu)
