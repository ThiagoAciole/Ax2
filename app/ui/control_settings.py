import configparser
import os
import threading

import customtkinter as ctk
import pygame
from PIL import Image
from utils.constants import *
from utils.icons import load_button_image, load_icons
from utils.paths import get_asset_path, get_emulator_path
from utils.theme import *


class ControlSettings:
    def __init__(self, parent=None):
        # === Dimensões fixas ===
        self.base_width = 800
        self.base_height = 600

        # === Janela ===
        self.root = create_window(
            parent=parent,
            title="Configuração de Controle",
            width=self.base_width,
            height=self.base_height,
            min_width=self.base_width,
            min_height=self.base_height,
            resizable=False,
            bg=BACKGROUND_DARK,
        )

        if parent:
            self.root.transient(parent)
            self.root.grab_set()
        self.root.focus_force()
        self.root.lift()

        # === Estado ===
        self.mapping = {}
        self.buttons = {}
        # 🔹 Caminho ajustado para o formato PCSX2.ini
        self.settings_path = os.path.join(get_emulator_path("inis"), "PCSX2.ini")
        self.running = True
        self.active_capture = None
        self.joystick_id = 0

        # === Joysticks ===
        pygame.init()
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for js in self.joysticks:
            js.init()

        print(f"[DEBUG] Joysticks detectados: {[js.get_name() for js in self.joysticks]}")

        self.load_current_mapping()
        self.build_ui()

        # === Thread de eventos ===
        self.thread = threading.Thread(target=self.listen_joystick_events, daemon=True)
        self.thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.button_map = {
            2: "Cross",      # A
            1: "Circle",     # B
            3: "Square",     # X
            0: "Triangle",   # Y
            4: "L1",
            5: "R1",
            6: "L2",
            7: "R2",
            8: "Select",
            9: "Start",
            10: "L3",
            11: "R3",
        }
    # ==================================
    # 📥 Ler e salvar o [Pad1]
    # ==================================
    def load_current_mapping(self):
        config = configparser.ConfigParser()
        config.optionxform = str  # Mantém maiúsculas (CamelCase)

        if not os.path.exists(self.settings_path):
            os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
            default_pad = {
                "Type": "DualShock2",
                "Up": "",
                "Right": "",
                "Down": "",
                "Left": "",
                "Triangle": "",
                "Circle": "",
                "Cross": "",
                "Square": "",
                "Select": "",
                "Start": "",
                "L1": "",
                "L2": "",
                "R1": "",
                "R2": "",
                "L3": "",
                "R3": "",
                "LLeft": "",
                "LRight": "",
                "LDown": "",
                "LUp": "",
                "RLeft": "",
                "RRight": "",
                "RDown": "",
                "RUp": "",
                "Analog": "",
            }
            config["Pad1"] = default_pad
            with open(self.settings_path, "w", encoding="utf-8") as f:
                config.write(f)
            print(f"[INFO] Criado PCSX2.ini padrão em {self.settings_path}")

        config.read(self.settings_path, encoding="utf-8")
        if "Pad1" in config:
            self.mapping = {k: v for k, v in config["Pad1"].items()}
            print("[DEBUG] Configuração carregada:")
            for k, v in self.mapping.items():
                print(f"  {k} = {v}")

    def save_mapping(self):
        try:
            config = configparser.ConfigParser()
            config.optionxform = str  # Mantém CamelCase

            if os.path.exists(self.settings_path):
                config.read(self.settings_path, encoding="utf-8")

            if config.has_section("Pad1"):
                config.remove_section("Pad1")

            # Base automática do controle (fixa)
            base_pad = {
                "Analog": f"SDL-{self.joystick_id}/Guide",
                "LLeft": f"SDL-{self.joystick_id}/-LeftX",
                "LRight": f"SDL-{self.joystick_id}/+LeftX",
                "LDown": f"SDL-{self.joystick_id}/+LeftY",
                "LUp": f"SDL-{self.joystick_id}/-LeftY",
                "RLeft": f"SDL-{self.joystick_id}/-RightX",
                "RRight": f"SDL-{self.joystick_id}/+RightX",
                "RDown": f"SDL-{self.joystick_id}/+RightY",
                "RUp": f"SDL-{self.joystick_id}/-RightY",
                "Type": "DualShock2",
            }

            non_empty = {k: v for k, v in self.mapping.items() if v.strip()}
            config["Pad1"] = {**non_empty, **base_pad}

            with open(self.settings_path, "w", encoding="utf-8") as f:
                config.write(f)

            print("[INFO] Configuração salva com sucesso!")
            for k, v in config["Pad1"].items():
                print(f"  {k} = {v}")

        except Exception as e:
            print(f"[ERRO] Falha ao salvar configurações: {e}")

    # ==================================
    # 🧱 Interface
    # ==================================
    def build_ui(self):
        self.px = 20
        self.py = 16

        self.header = ctk.CTkFrame(self.root, fg_color=TRANSPARENT)
        self.header.pack(fill="x", pady=(self.py, self.py // 2), padx=self.px)

        icons = load_icons()
        icon_refresh = icons["refresh"]
        icon_auto = icons["auto"]
        icon_clear = icons["clear"]

        pad_names = [f"{i}: {js.get_name()}" for i, js in enumerate(self.joysticks)]
        self.device_menu = ctk.CTkOptionMenu(
            self.header,
            values=pad_names or ["Nenhum joystick detectado"],
            width=600,
            height=36,
            fg_color=SURFACE,
            button_color=PRIMARY_COLOR,
            text_color=TEXT_PRIMARY,
            font=(FONT_FAMILY, 14),
            command=self.change_joystick,
        )
        self.device_menu.pack(side="left", padx=(0, 10))

        def create_icon_button(icon, command):
            lbl = ctk.CTkLabel(
                self.header, text="", image=icon, fg_color="transparent", cursor="hand2"
            )
            lbl.pack(side="right", padx=5)
            lbl.bind("<Button-1>", lambda e: command())

        create_icon_button(icon_clear, self.reset_buttons)
        create_icon_button(icon_refresh, self.refresh_devices)
        create_icon_button(icon_auto, self.auto_configure)

        # === Corpo ===
        self.body = ctk.CTkFrame(self.root, fg_color=BACKGROUND_DARK)
        self.body.pack(fill="both", expand=True, padx=self.px, pady=self.py)

        self.left = ctk.CTkFrame(self.body, fg_color=BACKGROUND_DARK)
        self.left.pack(side="left", fill="y", padx=(self.px, 10), pady=self.py)

        self.center = ctk.CTkFrame(self.body, fg_color=BACKGROUND_DARK)
        self.center.pack(side="left", expand=True, padx=10, pady=self.py)

        self.right = ctk.CTkFrame(self.body, fg_color=BACKGROUND_DARK)
        self.right.pack(side="right", fill="y", padx=(10, self.px), pady=self.py)

        rbuttons = (34, 28)
        startButtos=(28, 22)
        dpads=(24, 24)
        actions=(28, 28)
        self.icons = {
            "L1": load_button_image("l1.png", rbuttons),
            "L2": load_button_image("l2.png", rbuttons),
            "R1": load_button_image("r1.png", rbuttons),
            "R2": load_button_image("r2.png", rbuttons),
            "Cross": load_button_image("cross.png",actions),
            "Circle": load_button_image("circle.png", actions),
            "Square": load_button_image("square.png", actions),
            "Triangle": load_button_image("triangle.png",actions),
            "Up": load_button_image("up.png", dpads),
            "Down": load_button_image("down.png", dpads),
            "Left": load_button_image("left.png", dpads),
            "Right": load_button_image("right.png", dpads),
            "Select": load_button_image("select.png", startButtos),
            "Start": load_button_image("start.png", startButtos),
        }

        self.img_path = get_asset_path("joystick.png")
        img = ctk.CTkImage(Image.open(self.img_path), size=(360, 250))
        self.img_label = ctk.CTkLabel(self.center, text="", image=img)
        self.img_label.pack(pady=20)

        left_buttons = ["L1", "L2", "Up", "Down", "Left", "Right", "Select"]
        right_buttons = ["R1", "R2", "Cross", "Square", "Circle", "Triangle", "Start"]

        for name in left_buttons:
            self.create_icon_button(self.left, name)
        for name in right_buttons:
            self.create_icon_button(self.right, name)

        # === Rodapé ===
        self.footer = ctk.CTkFrame(self.root, fg_color=BACKGROUND)
        self.footer.pack(side="bottom", fill="x")

        button_frame = ctk.CTkFrame(self.footer, fg_color="transparent")
        button_frame.pack(side="right", pady=(10, 10), padx=(self.px, self.px))

        ctk.CTkButton(
            button_frame,
            text="Confirmar",
            fg_color=PRIMARY_COLOR,
            hover_color=PRIMARY_HOVER,
            text_color=TEXT_PRIMARY,
            font=(FONT_FAMILY, 15, FONT_WEIGHT_BOLD),
            corner_radius=10,
            height=40,
            width=120,
            command=self.confirm,
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Cancelar",
            fg_color=SURFACE_LIGHT,
            hover_color=ERROR,
            text_color=TEXT_PRIMARY,
            font=(FONT_FAMILY, 15, FONT_WEIGHT_BOLD),
            corner_radius=10,
            height=40,
            width=120,
            command=self.on_close,
        ).pack(side="right", padx=5)

        self.status_label = ctk.CTkLabel(
            self.footer,
            text="",
            text_color=TEXT_SECONDARY,
            font=(FONT_FAMILY, 13),
            fg_color=BACKGROUND,
        )
        self.status_label.pack(side="left", padx=self.px, pady=(0, 5))

    # ==================================
    # 🔄 Funções auxiliares
    # ==================================
    def reset_buttons(self):
        for name, btn in self.buttons.items():
            btn.configure(text="Press Button")
        self.mapping = {}
        self.status_label.configure(text="🧹 Todos os botões foram limpos.", text_color=WARNING)
        self.root.after(2500, lambda: self.status_label.configure(text=""))

    def change_joystick(self, value: str):
        try:
            self.joystick_id = int(value.split(":")[0])
            print(f"[INFO] Controle selecionado: SDL-{self.joystick_id}")
        except Exception:
            self.joystick_id = 0
            print("[WARN] Falha ao identificar ID do controle.")

    def create_icon_button(self, parent, name):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=8)

        icon = self.icons.get(name)
        ctk.CTkLabel(frame, image=icon, text="", fg_color="transparent").pack(
            side="left", padx=(0, 8)
        )

        value = self.mapping.get(name, "")
        display = value.split("/", 1)[-1] if "/" in value else value or "Press Button"

        btn = ctk.CTkButton(
            frame,
            text=display,
            fg_color=SURFACE_LIGHT,
            hover_color=PRIMARY_COLOR,
            text_color=TEXT_PRIMARY,
            corner_radius=8,
            width=120,
            height=40,
            font=(FONT_FAMILY, 13, FONT_WEIGHT_BOLD),
            command=lambda n=name: self.start_capture(n),
        )
        btn.pack(side="left")
        self.buttons[name] = btn

    # ==================================
    # 🎮 Captura e eventos
    # ==================================
    def pulse_button(self, button, color=PRIMARY_HOVER, duration=180):
        """Faz o botão piscar rapidamente ao ser pressionado."""
        original_color = button.cget("fg_color")

        def restore():
            button.configure(fg_color=original_color)

        button.configure(fg_color=color)
        self.root.after(duration, restore)
        
    def listen_joystick_events(self):
        
        while self.running:
            for event in pygame.event.get():
                prefix = f"SDL-{self.joystick_id}/"

                # 🎯 Se está capturando um botão específico (modo gravação)
                if self.active_capture:
                    btn_name = self.active_capture

                    # Direcional (DPad)
                    if event.type == pygame.JOYHATMOTION and event.value != (0, 0):
                        hat_map = {
                            (0, 1): prefix + "DPadUp",
                            (1, 0): prefix + "DPadRight",
                            (0, -1): prefix + "DPadDown",
                            (-1, 0): prefix + "DPadLeft",
                        }
                        code = hat_map.get(event.value)
                        if code:
                            self.mapping[btn_name] = code
                            if btn_name in self.buttons:
                                self.buttons[btn_name].configure(
                                    text=code.split("/")[-1],
                                    fg_color=SURFACE_LIGHT,
                                )
                            self.active_capture = None

                    # Botão físico pressionado (modo gravação)
                    elif event.type == pygame.JOYBUTTONDOWN:
                        code = prefix + f"Button{event.button}"
                        self.mapping[btn_name] = code
                        if btn_name in self.buttons:
                            self.buttons[btn_name].configure(
                                text=code.split("/")[-1],
                                fg_color=SURFACE_LIGHT,
                            )
                        print(f"[DEBUG] {btn_name} -> {code}")
                        self.active_capture = None

                # 🎮 Modo normal (sem captura): pulse visual ao pressionar botão real
                elif event.type == pygame.JOYBUTTONDOWN:
                    button_id = event.button
                    if button_id in self.button_map:
                        name = self.button_map[button_id]
                        if name in self.buttons:
                            self.pulse_button(self.buttons[name])

                # 🎮 Direcional também pisca
                elif event.type == pygame.JOYHATMOTION and event.value != (0, 0):
                    hat_map = {
                        (0, 1): "Up",
                        (1, 0): "Right",
                        (0, -1): "Down",
                        (-1, 0): "Left",
                    }
                    btn_name = hat_map.get(event.value)
                    if btn_name and btn_name in self.buttons:
                        self.pulse_button(self.buttons[btn_name])

            pygame.time.wait(10)



    # ==================================
    # 💾 Ações
    # ==================================
    def start_capture(self, name):
        for btn in self.buttons.values():
            btn.configure(fg_color=SURFACE_LIGHT)
        self.active_capture = name
        self.buttons[name].configure(fg_color=PRIMARY_HOVER, text="Aguardando...")

    def confirm(self):
        self.running = False
        self.save_mapping()
        self.status_label.configure(text="✅ Configuração salva com sucesso!", text_color=SUCCESS)
        self.root.after(2500, lambda: self.status_label.configure(text=""))

    def on_close(self):
        self.running = False
        pygame.quit()
        self.root.destroy()

    def refresh_devices(self):
        pygame.joystick.quit()
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for js in self.joysticks:
            js.init()

        pad_names = [f"{i}: {js.get_name()}" for i, js in enumerate(self.joysticks)]
        self.device_menu.configure(values=pad_names or ["Nenhum joystick detectado"])
        self.status_label.configure(
            text="🔄 Lista de controles atualizada.", text_color=PRIMARY_HOVER
        )
        self.root.after(2500, lambda: self.status_label.configure(text=""))

    def auto_configure(self):
        if not self.joysticks:
            self.status_label.configure(text="⚠️ Nenhum controle detectado.", text_color=WARNING)
            return

        try:
            js = self.joysticks[self.joystick_id]
            prefix = f"SDL-{self.joystick_id}/"
            self.mapping = {
                "Up": prefix + "DPadUp",
                "Right": prefix + "DPadRight",
                "Down": prefix + "DPadDown",
                "Left": prefix + "DPadLeft",
                "Triangle": prefix + "FaceNorth",
                "Circle": prefix + "FaceEast",
                "Cross": prefix + "FaceSouth",
                "Square": prefix + "FaceWest",
                "Select": prefix + "Back",
                "Start": prefix + "Start",
                "L1": prefix + "LeftShoulder",
                "R1": prefix + "RightShoulder",
                "L2": prefix + "+LeftTrigger",
                "R2": prefix + "+RightTrigger",
                "L3": prefix + "LeftStick",
                "R3": prefix + "RightStick",
            }

            for name, btn in self.buttons.items():
                if name in self.mapping:
                    btn.configure(text=self.mapping[name].split("/")[-1])

            self.status_label.configure(
                text=f"⚙️ Controle '{js.get_name()}' configurado automaticamente.",
                text_color=SUCCESS,
            )
            self.root.after(2500, lambda: self.status_label.configure(text=""))
        except Exception as e:
            print(f"[ERRO] Falha ao configurar controle automaticamente: {e}")
            self.status_label.configure(text="❌ Erro ao configurar controle.", text_color=ERROR)
