from langchain_openai import AzureOpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores.chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.callbacks import StdOutCallbackHandler
from flask import Flask, request
from gradio import gradio as gr
import openlit
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
openlit.init(
  otlp_endpoint="http://localhost:4318",
)

embeddings_model = AzureOpenAIEmbeddings()

vector_db = Chroma(
    persist_directory="../my_embeddings",
    embedding_function=embeddings_model
)

MODEL = "gpt-4o-mini"
llm = ChatOpenAI(temperature=0.7, model_name=MODEL)
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
# allow the retrieve to send up to 15 related chunks from the vector DB
retriever = vector_db.as_retriever(search_kwargs={"k": 15})
# enable stdout callbacks for debugging
conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory, callbacks=[StdOutCallbackHandler()])

def chat(message, history):
    logger.info("Invoking the conversation chain")
    result = conversation_chain.invoke({"question": message})
    return result["answer"]

view = gr.ChatInterface(chat, type="messages").launch(inbrowser=True)

