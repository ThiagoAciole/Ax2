import customtkinter as ctk
from ui.components.footer import create_footer
from ui.components.game_card import GameCard
from ui.components.search_input import SearchInput
from ui.control_settings import ControlSettings
from utils.constants import *
from utils.game import change_cover, delete_game, search_game, start_game
from utils.icons import load_icons
from utils.theme import *

root = None
game_frame = None
images = []


# === Atualiza lista de jogos ===
def refresh_callback():
    display_games(search_game())


# === Exibe jogos dinamicamente ===
def display_games(game_list, columns=6):
    global images
    images = []

    for w in game_frame.winfo_children():
        w.destroy()

    scroll = ctk.CTkScrollableFrame(game_frame, fg_color=BACKGROUND_DARK)
    scroll.pack(fill="both", expand=True)

    if not game_list:
        ctk.CTkLabel(
            scroll,
            text=NO_GAMES_FOUND,
            text_color=TEXT_SECONDARY,
            font=(FONT_FAMILY, FONT_SIZE_LG, FONT_WEIGHT_BOLD),
        ).pack(pady=50)
        return

    for idx, item in enumerate(game_list):
        card = GameCard(
            parent=scroll,
            title=item["title"],
            image=item["image"],
            platform="ps1",
            on_click=lambda f=item["file"]: start_game(f),
            on_edit=lambda f=item["title"]: change_cover(f, refresh_callback),
            on_delete=lambda f=item["title"]: delete_game(f, refresh_callback),
        )
        card.grid(row=idx // columns, column=idx % columns, padx=10, pady=10)


def open_control_settings():
    ControlSettings(root)


# === Tela principal ===
def start_home():
    global root, game_frame
    root = create_window(title=APP_NAME)

    # === Ícones ===
    icons = load_icons()
    icon_refresh = icons.get("refresh")
    icon_download = icons.get("store")
    icon_config = icons.get("config")

    # === Estrutura principal ===
    main = ctk.CTkFrame(root, fg_color=BACKGROUND)
    main.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

    main_frame = ctk.CTkFrame(main, fg_color=BACKGROUND)
    main_frame.pack(fill="both", expand=True)

    content = ctk.CTkFrame(main_frame, fg_color=BACKGROUND)
    content.pack(side="left", fill="both", expand=True)

    # === Header ===
    header = ctk.CTkFrame(content, fg_color=BACKGROUND)
    header.pack(fill="x", padx=10, pady=20)

    # === Campo de busca ===
    def filter_games(term):
        term = term.lower().strip()
        if not term:
            display_games(search_game())
        else:
            filtered = [g for g in search_game() if term in g["title"].lower()]
            display_games(filtered)

    search_input = SearchInput(header, on_change=filter_games)
    search_input.pack(side="left", padx=10)

    # === Drawer (Loja lateral) ===
    # drawer = ctk.CTkFrame(main_frame, fg_color=SURFACE, width=0)
    # drawer.pack(side="right", fill="y")
    #  drawer.pack_propagate(False)
    # drawer_visible = False

    # def toggle_store_drawer():
    #      nonlocal drawer_visible
    #      if not drawer_visible:
    #         drawer.configure(width=450)
    #         build_store_drawer(drawer, lambda: display_games(search_game(), columns=3))
    #         display_games(search_game(), columns=3)
    #     else:
    #         drawer.configure(width=0)
    #        for w in drawer.winfo_children():
    #             w.destroy()
    #         display_games(search_game(), columns=6)
    #     drawer_visible = not drawer_visible
    #     main_frame.update_idletasks()

    # === Botões do Header ===
    def create_icon_button(parent, icon, cmd):
        lbl = ctk.CTkLabel(parent, text="", image=icon, fg_color="transparent", cursor="hand2")
        lbl.pack(side="right", padx=8)
        lbl.bind("<Button-1>", lambda e: cmd())

    # Botão de abrir loja
   # create_icon_button(header, icon_download, toggle_store_drawer)

    # Frame de botões (config e refresh)
    config_frame = ctk.CTkFrame(
        header,
        fg_color="#2A2A2A",
        corner_radius=8,
    )
    config_frame.pack(side="right", padx=(0, 10), pady=4)

    # Botões dentro do frame
    create_icon_button(config_frame, icon_config, open_control_settings)
    create_icon_button(config_frame, icon_refresh, lambda: display_games(search_game()))

    # === Título da seção ===
    ctk.CTkLabel(
        content,
        text=DEFAULT_SECTION_TITLE,
        font=(FONT_FAMILY, FONT_SIZE_LG, FONT_WEIGHT_BOLD),
        text_color=TEXT_PRIMARY,
    ).pack(anchor="w", padx=20, pady=(10, 10))

    # === Área principal dos jogos ===
    game_frame = ctk.CTkFrame(content, fg_color=BACKGROUND)
    game_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))

    # === Render inicial ===
    display_games(search_game())

    # === Rodapé ===
    create_footer(root)

    root.mainloop()
