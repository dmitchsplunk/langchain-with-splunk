from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from flask import Flask, request
from opentelemetry.instrumentation.langchain import LangchainInstrumentor

app = Flask(__name__)
LangchainInstrumentor().instrument()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

embeddings_model = OpenAIEmbeddings()

db = Chroma(
    persist_directory="../my_embeddings",
    embedding_function=embeddings_model
)

store = {}
config = {"configurable": {"session_id": "test"}}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(model, get_session_history)

@app.route("/askquestion", methods=['POST'])
def ask_question():

    data = request.json
    question = data.get('question')

    # find the documents most similar to the question that we can pass as context
    context = db.similarity_search(question)

    response = with_message_history.invoke(
        [
            SystemMessage(
                content=f'Use the following pieces of context to answer the question: {context}'
            ),
            HumanMessage(
                content=question
            )
        ],
        config=config
    )

    return response.content

