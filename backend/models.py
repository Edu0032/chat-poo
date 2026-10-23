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
    def pode_apagar_mensagem(self) -> bool:
        pass

# [POO: Herança]
class UsuarioComum(Usuario):
    # [POO: Polimorfismo]
    def pode_apagar_mensagem(self) -> bool:
        return False

# [POO: Herança]
class Moderador(Usuario):
    # [POO: Polimorfismo]
    def pode_apagar_mensagem(self) -> bool:
        return True

class Mensagem:
    def __init__(self, id: int, autor: str, tipo_autor: str, conteudo: str):
        self._id = id
        self._autor = autor
        self._tipo_autor = tipo_autor
        self._conteudo = conteudo

    # [POO: Encapsulamento]
    @property
    def id(self) -> int:
        return self._id

    @property
    def autor(self) -> str:
        return self._autor

    @property
    def tipo_autor(self) -> str:
        return self._tipo_autor

    @property
    def conteudo(self) -> str:
        return self._conteudo

def criar_usuario(nome: str, tipo: str) -> Usuario:
    if tipo.lower() == "moderador":
        return Moderador(nome)
    return UsuarioComum(nome)
