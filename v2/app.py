from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from flask import Flask, request
from opentelemetry.instrumentation.langchain import LangchainInstrumentor

app = Flask(__name__)
LangchainInstrumentor().instrument()
model = ChatOpenAI(model="gpt-5-nano")

@app.route("/askquestion", methods=['POST'])
def ask_question():

    data = request.json
    question = data.get('question')

    messages = [
        SystemMessage(content="You are a helpful assistant!"),
        HumanMessage(content=question),
    ]

    return model.invoke(messages).content
