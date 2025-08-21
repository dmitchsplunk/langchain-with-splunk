# v7:  Using Azure OpenAI for Embeddings

This version of the application builds on v6 but uses Azure OpenAI to calculate 
embeddings for the user prompt, while using OpenAI for responding to user prompts. 

## Prerequisites

* Python 3.9+
* [Splunk Distribution of the OpenTelemetry Collector](https://docs.splunk.com/observability/en/gdi/opentelemetry/opentelemetry.html#otel-intro-install)
* An OpenAI account (set via the `OPENAI_API_KEY` environment variable) that has access to utilize the API
* An Azure OpenAI account (set via the `AZURE_OPENAI_API_KEY` environment variable) that has access to utilize the API

## Run the Application

Execute the following commands to run the application:

````
# clone the repo if you haven't already
git clone https://github.com/dmitchsplunk/langchain-with-splunk.git

# navigate to the directory repo
cd langchain-with-splunk/v7-azure

# create a virtual environment 
python3.12 -m venv openai-env

# activate the virtual environment
source openai-env/bin/activate

# install the required packages
pip3.12 install -r ./requirements.txt

# define the service name and environment
export OTEL_SERVICE_NAME=my-llm-app
export OTEL_RESOURCE_ATTRIBUTES='deployment.environment=test'
export OTEL_PYTHON_DISABLED_INSTRUMENTATIONS=fastapi

# set the Azure endpoints for the OpenAI Embeddings model

AZURE_OPENAI_ENDPOINT=<your endpoint>
AZURE_OPENAI_API_KEY=<your API token> 
AZURE_OPENAI_API_VERSION="2023-05-15"

# load the customer data into Chroma DB 
# Note:  Running the customer_data.py program multiple times will result in 
# duplicate embeddings stored in the vector database. If needed, you can 
# delete the my_embeddings folder and run this program once to start fresh.
python3 customer_data.py

# now we can run the application that uses embeddings to answer questions 
splunk-py-trace flask run -p 8080
````

## Test the Application

We can use the UI to ask the following question:

> Which customers are associated with the company Cherry and Sons?

It will respond with something like the following:

![Response to Question 1](../v6/images/response_to_question_1.png)

Since the application is retaining message history, it should be able to answer the following up
question correctly as well:

> And Giles LLC?

It will respond with something like:

![Response to Question 2](../v6/images/response_to_question_2.png)

You should see a trace in Splunk Observability Cloud such as the following:

![v6 Trace](../v6/images/v6_trace.png)