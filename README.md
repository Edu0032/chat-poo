# Chat POO

Sistema de chat em tempo real desenvolvido em Python aplicando os pilares de Programação Orientada a Objetos (**Abstração**, **Encapsulamento**, **Herança** e **Polimorfismo**), com comunicação via WebSockets e persistência no Supabase.

[Baixar Executáveis (Releases)](../../releases)

## Estrutura do Projeto

```text
chat-poo/
├── backend/
│   ├── main.py            # Servidor FastAPI e gerenciamento de WebSockets
│   ├── models.py          # Modelos de domínio e regras de negócio (POO)
│   └── requirements.txt   # Dependências do servidor
├── client/
│   ├── app.py             # Interface gráfica (Tkinter) e cliente WebSocket
│   ├── models.py          # Modelos do cliente e renderização polimórfica (POO)
│   └── requirements.txt   # Dependências do cliente
├── .env.example           # Modelo de variáveis de ambiente
└── .gitignore
```

## Configuração de Ambiente (Backend)

1. Copie o arquivo de exemplo para criar seu `.env`:
   ```bash
   cp .env.example .env
   ```
2. Preencha as variáveis `SUPABASE_URL` e `SUPABASE_KEY` no arquivo `.env`.
3. Instale as dependências e inicie o servidor:
   ```bash
   pip install -r backend/requirements.txt
   uvicorn main:app --app-dir backend --reload
   ```

## Como Abrir o Cliente (Executáveis)

### Windows
- Dê 2 cliques em `ChatClient-Windows.exe`.

### Linux
- Abra o terminal na pasta do arquivo e execute:
  ```bash
  chmod +x ChatClient-Linux && ./ChatClient-Linux
  ```
