---
name: poo-chat-architecture
description: Regras obrigatórias de POO (Herança, Polimorfismo, Encapsulamento e Abstração) e arquitetura de sessão única para o Chat Acadêmico.
---
# Diretrizes de POO e Negócio do Projeto
1. ENCAPSULAMENTO: Atributos das classes devem ser protegidos/privados (`_id`, `_nome`, `_conteudo`) expostos via `@property`.
2. ABSTRAÇÃO E HERANÇA:
   - Classe abstrata `Usuario(ABC)` com `@abstractmethod def pode_apagar_mensagem(self) -> bool`.
   - Subclasse `UsuarioComum(Usuario)` retornando `False`.
   - Subclasse `Moderador(Usuario)` retornando `True`.
3. POLIMORFISMO:
   - No servidor: validar exclusão chamando `usuario.pode_apagar_mensagem()` sem usar `if tipo == "moderador"`.
   - No cliente: um método polimórfico `renderizar_acao(self, frame, msg_id, callback)` na hierarquia de `Usuario` onde `UsuarioComum` não faz nada (`pass`) e `Moderador` cria o botão `[X]` de apagar.
4. SESSÃO ÚNICA: Nomes podem se repetir. Ao conectar, salva a sessão no Supabase, carrega todo o histórico global da tabela `mensagens` e sincroniza novas mensagens e exclusões via WebSocket broadcast para todos.
