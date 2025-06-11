# ia_core.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS  # Atualização de import
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage, SystemMessage

# Carregando API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# ===== RAG SETUP =====
def setup_rag():
    docs = []
    # vendo o nome de todos os arquivos dentro da pasta "documentos"
    for nome in os.listdir("documentos"):
        # selecionando todos arquivos que terminam com ".txt" 1 a 1
        if nome.endswith(".txt"):

            # pegando o caminho relativo deles
            caminho = os.path.join("documentos", nome)

            # transformando texto em um formato entendivel para a IA
            loader = TextLoader(caminho, encoding="utf-8")

            # adiciona o texto ao array que contém os dados dos outros arquivos em conjunto
            docs.extend(loader.load())

    # classe para divisão do conteúdo do arquivo
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    # divide os conteúdos de cada arquivo em partes menores para facilitar a leitura do modelo
    docs_divididos = splitter.split_documents(docs)

    # prepara uma classe para transformação de cada pedaço em um vetor numérico
    embeddings = GoogleGenerativeAIEmbeddings(
        google_api_key=api_key,
        model="models/embedding-001"
    )

    # armazena os vetores em um banco que facilita as buscas de valores dentro de um vetor
    db = FAISS.from_documents(docs_divididos, embeddings)

    # definindo o modelo da IA
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5, google_api_key=api_key)

    # ferramenta para criação de sistemas de perguntas e respostas, que utiliza uma determinada base para basear as suas respostas
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever(),
        return_source_documents=True
    )

# chama a função para criação do modelo com rag
rag_chain = setup_rag()

# ===== JUÍZ =====
juiz = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3, google_api_key=api_key)

def avaliar_resposta(pergunta, resposta):
    # prepara o prompt pra passar pro juiz
    prompt_juiz = '''
    Você é um avaliador imparcial. Sua tarefa é revisar a resposta de um sistema de IA para uma pergunta de aluno.

    Critérios:
    - A resposta está tecnicamente correta?
    - Está clara para o nível médio técnico?
    - O próximo passo sugerido está bem formulado?

    Se a resposta for boa, diga “✅ Aprovado” e explique por quê.
    Se tiver problemas, diga “⚠️ Reprovado” e proponha uma versão melhorada.
    '''

    # separa o contexto do sistema e do usuário
    mensagens = [
        SystemMessage(content=prompt_juiz),
        HumanMessage(content=f"Pergunta do aluno: {pergunta}\n\nResposta do sistema: {resposta}")
    ]

    # solicita o retorno do Juiz
    return juiz.invoke(mensagens).content
