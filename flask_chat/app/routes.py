from flask import Blueprint, render_template, request
from datetime import datetime
import os
from app import ia_core

rag_chain = ia_core.rag_chain
avaliar_resposta = ia_core.avaliar_resposta

bp = Blueprint("chat", __name__)

def registrar_log(rota, mensagem):
    os.makedirs("logs", exist_ok=True)
    caminho = "logs/conversa.log"
    mensagem = mensagem.strip()
    if mensagem:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        origem = "USUÁRIO" if rota == "usuario" else "ATENDENTE"
        with open(caminho, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{origem}] {mensagem}\n")

def carregar_historico():
    caminho = "logs/conversa.log"
    historico = []
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f.readlines():
                if "[USUÁRIO]" in linha:
                    origem = "usuario"
                elif "[ATENDENTE]" in linha:
                    origem = "atendente"
                else:
                    origem = "outro"
                historico.append({
                    "texto": linha.strip(),
                    "origem": origem
                })
    return historico

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "enviar" in request.form:
            msg = request.form["mensagem"]
            registrar_log("usuario", msg)

            rag_result = rag_chain.invoke({"query": msg})
            resposta = rag_result["result"]

            avaliacao = avaliar_resposta(msg, resposta)

            registrar_log("atendente", f"RAG: {resposta}")
            registrar_log("atendente", f"AVALIAÇÃO: {avaliacao}")

        elif "encerrar" in request.form:
            registrar_log("usuario", "CONVERSA ENCERRADA PELO USUÁRIO")

    historico = carregar_historico()
    return render_template("index.html", historico=historico)
