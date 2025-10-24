from tkinter import StringVar

import customtkinter as ctk
from utils.theme import *


class SearchInput(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_change=None,
        on_refresh=None,  # agora opcional
        placeholder="Buscar Jogo...",
        width=400,
        height=40,
        auto_focus=False,
    ):
        super().__init__(
            parent, fg_color=SURFACE_LIGHT, corner_radius=RADIUS, width=width, height=height
        )
        self.pack_propagate(False)

        self.placeholder = placeholder
        self.on_change = on_change
        self.on_refresh = on_refresh
        self.search_var = StringVar(value=placeholder)
        self._bind_id = None

        from utils.icons import load_icons

        icons = load_icons()
        icon_search = icons.get("search")
        icon_refresh = icons.get("refresh")

        # === Ícone da lupa ===
        self.icon_label = ctk.CTkLabel(
            self, text="", image=icon_search, fg_color="transparent", width=30
        )
        self.icon_label.pack(side="left", padx=(10, 0))

        # === Campo de texto ===
        self.entry = ctk.CTkEntry(
            self,
            textvariable=self.search_var,
            font=(FONT_FAMILY, FONT_SIZE_MD),
            text_color=TEXT_MUTED,
            border_width=0,
            fg_color=SURFACE_LIGHT,
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=(6, 4), pady=6)

        # === Botão de refresh (só aparece se on_refresh for passado) ===
        if callable(on_refresh):
            self.refresh_button = ctk.CTkLabel(
                self,
                text="",
                image=icon_refresh,
                cursor="hand2",
                fg_color="transparent",
                width=30,
                corner_radius= 12
            )
            self.refresh_button.pack(side="right", padx=(0, 10))
            self.refresh_button.bind(
                "<Enter>", lambda e: self.refresh_button.configure(fg_color=SURFACE_HOVER)
            )
            self.refresh_button.bind(
                "<Leave>", lambda e: self.refresh_button.configure(fg_color="transparent")
            )
            self.refresh_button.bind("<Button-1>", lambda e: self._on_refresh_click())
        else:
            self.refresh_button = None

        # === Eventos ===
        self.entry.bind("<FocusIn>", self._on_focus_in, add="+")
        self.entry.bind("<FocusOut>", self._on_focus_out, add="+")
        self.entry.bind("<Button-1>", lambda e: self.entry.focus_set(), add="+")
        self.search_var.trace_add("write", self._on_text_change)

        # Bind global para clique fora
        self.after(300, self._bind_click_outside)

        if auto_focus:
            self.after(350, lambda: self.entry.focus_set())

        self.bind("<Destroy>", self._on_destroy, add="+")

    # --- Evento refresh ---
    def _on_refresh_click(self):
        if callable(self.on_refresh):
            self.on_refresh()

    # --- Foco ---
    def _on_focus_in(self, _=None):
        if self.search_var.get() == self.placeholder:
            self.search_var.set("")
        self.entry.configure(text_color=TEXT_PRIMARY, fg_color=SURFACE_LIGHT)

    def _on_focus_out(self, _=None):
        if self.search_var.get().strip() == "":
            self.search_var.set(self.placeholder)
            self.entry.configure(text_color=TEXT_MUTED, fg_color=SURFACE_LIGHT)

    def _on_text_change(self, *_):
        if callable(self.on_change):
            txt = self.search_var.get()
            if txt != self.placeholder:
                self.on_change(txt)

    # --- Clique fora ---
    def _bind_click_outside(self):
        root = self.winfo_toplevel()

        def handle_click(event):
            target = root.winfo_containing(event.x_root, event.y_root)
            if target and (target == self.entry or target in self.winfo_children()):
                return
            if self.entry.focus_get() == self.entry:
                try:
                    root.focus_set()
                except Exception:
                    pass
                self._on_focus_out()

        self._bind_id = root.bind_all("<ButtonRelease-1>", handle_click, add="+")

    def _on_destroy(self, _=None):
        try:
            root = self.winfo_toplevel()
            if self._bind_id:
                root.unbind_all("<ButtonRelease-1>")
                self._bind_id = None
        except Exception:
            pass

    # --- Métodos públicos ---
    def get_value(self):
        val = self.search_var.get()
        return "" if val == self.placeholder else val.strip()

    def clear(self):
        self.search_var.set("")
        self.entry.configure(text_color=TEXT_PRIMARY)
