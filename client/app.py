import json
import threading
import tkinter as tk
from tkinter import messagebox
import websocket
from models import criar_usuario

# Modifique aqui a URL do backend (ex: wss://seu-backend.onrender.com/ws ou ws://localhost:8000/ws)
WS_URL = "wss://chat-poo.onrender.com/ws"

class ChatApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Chat POO")
        self.root.geometry("450x500")

        self.ws = None
        self.usuario = None
        self.mensagens_widgets = {}

        self.tela_login()

    def tela_login(self):
        self.frame_login = tk.Frame(self.root, padx=20, pady=20)
        self.frame_login.pack(expand=True)

        tk.Label(self.frame_login, text="Nome:").pack(anchor="w")
        self.entry_nome = tk.Entry(self.frame_login, width=30)
        self.entry_nome.pack(pady=5)

        self.tipo_var = tk.StringVar(value="comum")
        tk.Radiobutton(self.frame_login, text="Usuário Comum", variable=self.tipo_var, value="comum").pack(anchor="w")
        tk.Radiobutton(self.frame_login, text="Moderador", variable=self.tipo_var, value="moderador").pack(anchor="w")

        tk.Button(self.frame_login, text="Entrar", command=self.conectar).pack(pady=10)

    def tela_chat(self):
        self.frame_login.destroy()
        self.frame_chat = tk.Frame(self.root)
        self.frame_chat.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame_chat)
        self.scrollbar = tk.Scrollbar(self.frame_chat, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas)

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        frame_input = tk.Frame(self.frame_chat, pady=5)
        frame_input.pack(side=tk.BOTTOM, fill=tk.X, padx=5)

        self.entry_msg = tk.Entry(frame_input)
        self.entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry_msg.bind("<Return>", lambda e: self.enviar_mensagem())

        tk.Button(frame_input, text="Enviar", command=self.enviar_mensagem).pack(side=tk.RIGHT)

    def conectar(self):
        nome = self.entry_nome.get().strip()
        tipo = self.tipo_var.get()
        if not nome:
            messagebox.showwarning("Aviso", "Informe um nome.")
            return

        self.usuario = criar_usuario(nome, tipo)
        self.tela_chat()

        url = f"{WS_URL}/{self.usuario.nome}/{tipo}"
        self.ws = websocket.WebSocketApp(
            url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        threading.Thread(
            target=lambda: self.ws.run_forever(ping_interval=25, ping_timeout=10),
            daemon=True
        ).start()

    def on_message(self, ws, message):
        dados = json.loads(message)
        acao = dados.get("acao")
        if acao == "historico":
            self.root.after(0, self.carregar_historico, dados.get("mensagens", []))
        elif acao == "nova_mensagem":
            self.root.after(0, self.adicionar_mensagem, dados.get("mensagem", {}))
        elif acao == "removida":
            self.root.after(0, self.remover_mensagem, dados.get("id"))

    def on_error(self, ws, error):
        pass

    def on_close(self, ws, close_status_code, close_msg):
        pass

    def carregar_historico(self, mensagens: list):
        for msg in mensagens:
            self.adicionar_mensagem(msg)

    def adicionar_mensagem(self, msg: dict):
        msg_id = msg.get("id")
        autor = msg.get("autor", "")
        conteudo = msg.get("conteudo", "")

        row = tk.Frame(self.scroll_frame)
        row.pack(fill=tk.X, padx=5, pady=2)
        self.mensagens_widgets[msg_id] = row

        lbl = tk.Label(row, text=f"{autor}: {conteudo}", anchor="w")
        lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # [POO: Polimorfismo]
        self.usuario.renderizar_botao_apagar(row, msg_id, self.solicitar_apagar, tk)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def remover_mensagem(self, msg_id: int):
        widget = self.mensagens_widgets.pop(msg_id, None)
        if widget:
            widget.destroy()

    def enviar_mensagem(self):
        texto = self.entry_msg.get().strip()
        if texto and self.ws:
            self.ws.send(json.dumps({"acao": "enviar", "conteudo": texto}))
            self.entry_msg.delete(0, tk.END)

    def solicitar_apagar(self, msg_id: int):
        if self.ws:
            self.ws.send(json.dumps({"acao": "apagar", "id": msg_id}))

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
