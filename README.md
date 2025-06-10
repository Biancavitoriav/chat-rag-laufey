# 🐇 Chat da laufey

Um chat feito com flask, rag e a api do gemini

## Como funciona?

![image](https://github.com/user-attachments/assets/3bc90ae1-2d7d-48c8-926a-4abd0fb1633a)


O usuário precisa enviar uma afirmação sobre a Laufey, para que o RAG verifique nos documentos se é verdadeiro ou não. Logo, acionamos a API do gemini para verificar se a mensagem mandada pelo RAG é apropriada

RAG: É o processo de otimizar a saída de um grande modelo de linguagem, de forma que ele faça referência a uma base de conhecimento confiável fora das suas fontes de dados de treinamento antes de gerar uma resposta. Grandes modelos de linguagem (LLMs) são treinados em grandes volumes de dados e usam bilhões de parâmetros para gerar resultados originais para tarefas como responder a perguntas, traduzir idiomas e concluir frases
Fonte: https://aws.amazon.com/pt/what-is/retrieval-augmented-generation/

Importante ressaltar que os documentos só contem informações sobre a Laufey, então se o usuário perguntar algo fora disso, a IA não saberá responder, e isso é válido.

---

## Como rodar?

1. Crie uma chave na API do gemini
https://aistudio.google.com/app/apikey?hl=pt-br

Crie um arquivo .env em praticaFlaskIa/flask_chat/.env com o conteúdo:

GEMINI_API_KEY=<chave>

e substitua <chave> pela chave obtida no gemini

2. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/la-laufey-chat.git
cd praticaFlaskIa
cd flask_chat
```

3. Baixe as dependencias

```bash
pip install -r requirements.txt
```

4. Rode

```bash
venv\Scripts\Activate
flask run
```
