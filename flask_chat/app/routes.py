from flask import Blueprint, render_template, request
from datetime import datetime
import os
from app import ia_core

# busca o rag_chain que está dentro de ia_core
rag_chain = ia_core.rag_chain

# puxa a função de avaliar_resposta do ia_core
avaliar_resposta = ia_core.avaliar_resposta

bp = Blueprint("chat", __name__)

# salva um novo log no sistema
def registrar_log(rota, mensagem):
    # cria uma pasta de logs, se não existir
    os.makedirs("logs", exist_ok=True)

    # cria o log para o sistema
    caminho = "logs/conversa.log"
    mensagem = mensagem.strip()
    if mensagem:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        origem = "USUÁRIO" if rota == "usuario" else "ATENDENTE"
        with open(caminho, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{origem}] {mensagem}\n")

# carrega as informações que foram geradas dentro do arquivo de log
def carregar_historico():
    caminho = "logs/conversa.log"
    historico = []
    
    # verifica se há um arquivo de log criado, se sim, retorna os registros dentro do arquivo de maneira formatada
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

# rota que será acessada pelo front end
@bp.route("/", methods=["GET", "POST"])
def index():

    # caso método seja POST, cria, e avalia a resposta do usuário
    if request.method == "POST":
        if "enviar" in request.form:

            # recebe a mensagem enviada pelo usuário
            msg = request.form["mensagem"]

            # registra a mensagem do usuário dentro do arquivo de log
            registrar_log("usuario", msg)

            print(f"Mensagem recebida: {msg}")  # Log para depuração

            # pede a resposta da API para pergunta do usuário
            rag_result = rag_chain.invoke({"query": msg})

            # pega o resultado em sí do retorno da API
            resposta = rag_result["result"]

            # solicita que o juiz faça a avaliação do modelo da resposta
            avaliacao = avaliar_resposta(msg, resposta)

            # registra a mensagem dada pelo modelo
            registrar_log("atendente", f"RAG: {resposta}")

            # registra a resposta dada pelo juiz
            registrar_log("atendente", f"AVALIAÇÃO: {avaliacao}")

        # caso o usuário tenha optado por terminar a conversa, registra este momento
        elif "encerrar" in request.form:
            # registra saída do usuário
            registrar_log("usuario", "CONVERSA ENCERRADA PELO USUÁRIO")

    # carrega as alterações que foram realizadas no arquivo de logs
    historico = carregar_historico()

    # renderiza a tela HTML com o histórico salvo no sistema
    return render_template("index.html", historico=historico)
