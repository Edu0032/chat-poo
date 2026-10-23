import os
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from supabase import create_client, Client
from models import criar_usuario

load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nsnwmhsmcdgabjvurpmp.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_T6LkHAHISJnzol8QwjtOlw_UTMjHofU")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

conexoes: list[WebSocket] = []

async def broadcast(dados: dict):
    for conexao in list(conexoes):
        await conexao.send_json(dados)

@app.get("/")
def healthcheck():
    return {"status": "ok"}

@app.websocket("/ws/{nome}/{tipo}")
async def websocket_endpoint(websocket: WebSocket, nome: str, tipo: str):
    await websocket.accept()
    conexoes.append(websocket)
    usuario = criar_usuario(nome, tipo)

    supabase.table("sessoes").insert({"nome": usuario.nome, "tipo": tipo}).execute()
    historico = supabase.table("mensagens").select("*").order("id").execute()
    await websocket.send_json({"acao": "historico", "mensagens": historico.data})

    try:
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
                    await broadcast({"acao": "nova_mensagem", "mensagem": res.data[0]})

            elif acao == "apagar":
                # [POO: Polimorfismo]
                if usuario.pode_apagar_mensagem():
                    msg_id = dados["id"]
                    supabase.table("mensagens").delete().eq("id", msg_id).execute()
                    await broadcast({"acao": "removida", "id": msg_id})
    except WebSocketDisconnect:
        conexoes.remove(websocket)
    except Exception:
        if websocket in conexoes:
            conexoes.remove(websocket)
