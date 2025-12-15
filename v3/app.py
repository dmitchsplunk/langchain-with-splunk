from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from flask import Flask, request
from opentelemetry.instrumentation.langchain import LangchainInstrumentor

app = Flask(__name__)
LangchainInstrumentor().instrument()
model = ChatOpenAI(model="gpt-5-nano")

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

    response = with_message_history.invoke(
        [
            SystemMessage(content="You are a helpful assistant"),
            HumanMessage(content=question)
        ],
        config=config
    )

    return response.content

