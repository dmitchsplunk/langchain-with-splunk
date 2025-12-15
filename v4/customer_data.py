from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

file_path = (
   "./customers-1000.csv"
)

loader = CSVLoader(file_path=file_path)
customer_data = loader.load()

embeddings_model = OpenAIEmbeddings()

db = Chroma.from_documents(
   customer_data,
   embedding=embeddings_model,
   persist_directory="../my_embeddings"
)

results = db.similarity_search(
   "Which customers are associated with the company Cherry and Sons?"
)

for result in results:
   print("\n")
   print(result.page_content)