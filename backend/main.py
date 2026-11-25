import os
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from supabase import create_client, Client
from models import Mensagem, criar_usuario

load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("As variáveis de ambiente SUPABASE_URL e SUPABASE_KEY devem ser definidas.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

conexoes: list[WebSocket] = []

# [POO: Lista de Objetos]
lista_mensagens: list[Mensagem] = []

async def broadcast(dados: dict):
    inativas: list[WebSocket] = []
    for conexao in list(conexoes):
        try:
            await conexao.send_json(dados)
        except Exception:
            inativas.append(conexao)

    for conexao in inativas:
        if conexao in conexoes:
            conexoes.remove(conexao)

@app.get("/")
def healthcheck():
    return {"status": "ok"}

@app.websocket("/ws/{nome}/{tipo}")
async def websocket_endpoint(websocket: WebSocket, nome: str, tipo: str):
    await websocket.accept()
    conexoes.append(websocket)
    usuario = criar_usuario(nome, tipo)
    mensagens_sessao: set[int] = set()

    try:
        supabase.table("sessoes").insert({"nome": usuario.nome, "tipo": tipo}).execute()
        historico = supabase.table("mensagens").select("*").order("id").execute()

        # [POO: Lista de Objetos - Consultar]
        lista_mensagens.clear()
        for item in historico.data:
            autor_obj = criar_usuario(item["autor"], item["tipo_autor"])
            # [POO: Agregação]
            msg_obj = Mensagem(item["id"], autor_obj, item["tipo_autor"], item["conteudo"])
            lista_mensagens.append(msg_obj)

        await websocket.send_json({
            "acao": "historico",
            "mensagens": [m.to_dict() for m in lista_mensagens]
        })

        while True:
            dados = await websocket.receive_json()
            acao = dados.get("acao")

            if acao == "enviar":
                res = supabase.table("mensagens").insert({
                    "autor": usuario.nome,
                    "tipo_autor": tipo,
                    "conteudo": dados["conteudo"]
                }).execute()
                if res.data:
                    item = res.data[0]
                    # [POO: Agregação]
                    nova_msg = Mensagem(item["id"], usuario, tipo, item["conteudo"])
                    # [POO: Lista de Objetos - Inserir]
                    lista_mensagens.append(nova_msg)
                    mensagens_sessao.add(nova_msg.id)
                    await broadcast({"acao": "nova_mensagem", "mensagem": nova_msg.to_dict()})

            elif acao == "editar":
                msg_id = dados["id"]
                novo_conteudo = dados["conteudo"]
                if msg_id in mensagens_sessao:
                    # [POO: Lista de Objetos - Alterar]
                    for m in lista_mensagens:
                        if m.id == msg_id:
                            # [POO: Encapsulamento]
                            m.conteudo = novo_conteudo
                            supabase.table("mensagens").update({"conteudo": novo_conteudo}).eq("id", msg_id).execute()
                            await broadcast({"acao": "editada", "id": msg_id, "conteudo": novo_conteudo})
                            break

            elif acao == "apagar":
                # [POO: Polimorfismo]
                if usuario.pode_apagar_mensagem():
                    msg_id = dados["id"]
                    # [POO: Lista de Objetos - Excluir]
                    for m in list(lista_mensagens):
                        if m.id == msg_id:
                            lista_mensagens.remove(m)
                            break
                    supabase.table("mensagens").delete().eq("id", msg_id).execute()
                    await broadcast({"acao": "removida", "id": msg_id})
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        if websocket in conexoes:
            conexoes.remove(websocket)
