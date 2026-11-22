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

# [POO: Agregação]
class Mensagem:
    def __init__(self, id: int, autor: Usuario, tipo_autor: str, conteudo: str):
        self._id = id
        # [POO: Agregação]
        self._autor = autor
        self._tipo_autor = tipo_autor
        self._conteudo = conteudo

    # [POO: Encapsulamento]
    @property
    def id(self) -> int:
        return self._id

    # [POO: Encapsulamento]
    @property
    def autor(self) -> Usuario:
        return self._autor

    # [POO: Encapsulamento]
    @property
    def tipo_autor(self) -> str:
        return self._tipo_autor

    # [POO: Encapsulamento]
    @property
    def conteudo(self) -> str:
        return self._conteudo

    # [POO: Encapsulamento]
    @conteudo.setter
    def conteudo(self, novo_conteudo: str):
        self._conteudo = novo_conteudo

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "autor": self.autor.nome,
            "tipo_autor": self.tipo_autor,
            "conteudo": self.conteudo
        }

def criar_usuario(nome: str, tipo: str) -> Usuario:
    if tipo.lower() == "moderador":
        return Moderador(nome)
    return UsuarioComum(nome)
