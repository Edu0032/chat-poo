from abc import ABC, abstractmethod

# [POO: Abstração]
class Usuario(ABC):
    def __init__(self, nome: str):
        self._nome = nome

    # [POO: Encapsulamento]
    @property
    def nome(self) -> str:
        return self._nome

    # [POO: Polimorfismo]
    @abstractmethod
    def renderizar_botao_apagar(self, parent_frame, msg_id: int, callback_apagar, tk_module):
        pass

# [POO: Herança]
class UsuarioComum(Usuario):
    # [POO: Polimorfismo]
    def renderizar_botao_apagar(self, parent_frame, msg_id: int, callback_apagar, tk_module):
        pass

# [POO: Herança]
class Moderador(Usuario):
    # [POO: Polimorfismo]
    def renderizar_botao_apagar(self, parent_frame, msg_id: int, callback_apagar, tk_module):
        btn = tk_module.Button(
            parent_frame,
            text="X",
            fg="red",
            command=lambda: callback_apagar(msg_id)
        )
        btn.pack(side=tk_module.RIGHT, padx=5)

def criar_usuario(nome: str, tipo: str) -> Usuario:
    if tipo.lower() == "moderador":
        return Moderador(nome)
    return UsuarioComum(nome)
