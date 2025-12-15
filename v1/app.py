from openai import OpenAI
from flask import Flask, request
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

app = Flask(__name__)
OpenAIInstrumentor().instrument()
client = OpenAI()

@app.route("/askquestion", methods=['POST'])
def ask_question():

    data = request.json
    question = data.get('question')

    completion = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    return completion.choices[0].message.content