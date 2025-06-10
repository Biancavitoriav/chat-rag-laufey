# ia_core.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain.schema import HumanMessage, SystemMessage

# Carregando API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# ===== RAG SETUP =====
def setup_rag():
    docs = []
    for nome in os.listdir("documentos"):
        if nome.endswith(".txt"):
            caminho = os.path.join("documentos", nome)
            loader = TextLoader(caminho, encoding="utf-8")
            docs.extend(loader.load())

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs_divididos = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(
        google_api_key=api_key,
        model="models/embedding-001"
    )
    db = FAISS.from_documents(docs_divididos, embeddings)

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5, google_api_key=api_key)

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever(),
        return_source_documents=True
    )

rag_chain = setup_rag()

# ===== AGENTE CONVERSACIONAL =====
def get_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7, google_api_key=api_key)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    system_prompt = """
    Você é um tutor de IA amigável e experiente. Explique conceitos de forma clara e adaptada ao nível técnico médio.
    """
    return initialize_agent(
        llm=llm,
        tools=[],
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        agent_kwargs={"prefix": system_prompt}
    )

agent = get_agent()

# ===== JUÍZ =====
juiz = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3, google_api_key=api_key)

def avaliar_resposta(pergunta, resposta_tutor):
    prompt_juiz = '''
    Você é um avaliador imparcial. Sua tarefa é revisar a resposta de um tutor de IA para uma pergunta de aluno.

    Critérios:
    - A resposta está tecnicamente correta?
    - Está clara para o nível médio técnico?
    - O próximo passo sugerido está bem formulado?

    Se a resposta for boa, diga “✅ Aprovado” e explique por quê.
    Se tiver problemas, diga “⚠️ Reprovado” e proponha uma versão melhorada.
    '''
    mensagens = [
        SystemMessage(content=prompt_juiz),
        HumanMessage(content=f"Pergunta do aluno: {pergunta}\n\nResposta do tutor: {resposta_tutor}")
    ]
    return juiz.invoke(mensagens).content
