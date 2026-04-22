import tkinter as tk
import pyautogui
import threading
import time
import keyboard
from pynput import mouse


class AutoClickerSuave:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("300x620")
        self.root.configure(bg="#2d2d2d")
        self.root.attributes("-topmost", True)

        # Estilos
        self.bg_color = "#2d2d2d"
        self.fg_color = "#e0e0e0"
        self.font_main = ("Segoe UI", 9)
        self.entry_style = {"bg": "#3d3d3d", "fg": "#ffffff", "borderwidth": 0, "insertbackground": "white"}

        # --- Layout ---
        tk.Label(root, text="AÇÃO", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 10, "bold")).pack(
            pady=(15, 0))

        self.var_tipo = tk.StringVar(value="Mouse")
        self.menu = tk.OptionMenu(root, self.var_tipo, "Mouse", "Teclado", command=self.ajustar_interface)
        self.menu.config(bg="#3d3d3d", fg=self.fg_color, borderwidth=0, highlightthickness=0)
        self.menu.pack(pady=5)

        # Frame de Coordenadas (Logo abaixo do menu)
        self.frame_coords = tk.Frame(root, bg=self.bg_color)
        self.frame_coords.pack(pady=5)

        self.create_entry_in_frame(self.frame_coords, "Coordenada X", "entry_x")
        self.create_entry_in_frame(self.frame_coords, "Coordenada Y", "entry_y")
        self.btn_capturar = tk.Button(self.frame_coords, text="Capturar Posição (5s)", command=self.ativar_modo_captura,
                                      bg="#4a4a4a", fg="white", borderwidth=0, padx=10)
        self.btn_capturar.pack(pady=5)

        # --- Campos Gerais ---
        self.create_entry("Tecla (Ação)", "entry_tecla")
        self.create_entry("Intervalo (s)", "entry_int", "1.0")
        self.create_entry("Repetições", "entry_rep", "5")

        self.var_infinito = tk.BooleanVar()
        tk.Checkbutton(root, text="Repetir Indefinidamente", variable=self.var_infinito,
                       bg=self.bg_color, fg=self.fg_color, selectcolor="#2d2d2d", font=self.font_main).pack()

        # Botões Principais
        self.btn_iniciar = tk.Button(root, text="INICIAR (5s p/ trocar janela)", command=self.iniciar_processo,
                                     bg="#388e3c", fg="white", borderwidth=0, font=("Segoe UI", 9, "bold"))
        self.btn_iniciar.pack(pady=15, ipadx=5)

        tk.Button(root, text="PARAR (Tecla ESC)", command=self.parar, bg="#d32f2f", fg="white", borderwidth=0).pack()

        keyboard.add_hotkey('esc', self.parar)

    def ajustar_interface(self, value):
        if value == "Mouse":
            self.frame_coords.pack(pady=5)
        else:
            self.frame_coords.pack_forget()

    def create_entry_in_frame(self, parent, label, attr_name):
        tk.Label(parent, text=label, bg=self.bg_color, fg=self.fg_color, font=self.font_main).pack()
        entry = tk.Entry(parent, **self.entry_style, justify='center')
        entry.pack(pady=2)
        setattr(self, attr_name, entry)

    def create_entry(self, label, attr_name, default=""):
        tk.Label(self.root, text=label, bg=self.bg_color, fg=self.fg_color, font=self.font_main).pack()
        entry = tk.Entry(self.root, **self.entry_style, justify='center')
        entry.insert(0, default)
        entry.pack(pady=2)
        setattr(self, attr_name, entry)

    def ativar_modo_captura(self):
        self.btn_capturar.config(text="Aguardando clique...", bg="#f57c00")
        listener = mouse.Listener(on_click=self.on_click)
        listener.start()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.entry_x.delete(0, tk.END);
            self.entry_x.insert(0, str(x))
            self.entry_y.delete(0, tk.END);
            self.entry_y.insert(0, str(y))
            self.btn_capturar.config(text="Capturar Posição (5s)", bg="#4a4a4a")
            return False

    def parar(self):
        self.rodando = False

    def iniciar_processo(self):
        time.sleep(5)
        self.rodando = True
        threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):
        repeticoes = int(self.entry_rep.get()) if not self.var_infinito.get() else float('inf')
        contagem = 0
        while self.rodando and (contagem < repeticoes):
            try:
                if self.var_tipo.get() == "Mouse":
                    pyautogui.click(x=int(self.entry_x.get()), y=int(self.entry_y.get()))
                else:
                    pyautogui.press(self.entry_tecla.get())
                time.sleep(float(self.entry_int.get()))
                contagem += 1
            except:
                self.rodando = False


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerSuave(root)
    root.mainloop()