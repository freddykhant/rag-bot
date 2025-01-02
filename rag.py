from langchain_ollama import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_nomic.embeddings import NomicEmbeddings

# load LLM model
local_llm = "llama3.2:1b"
llm = ChatOllama(model=local_llm, temperature=0)
llm_json_mode = ChatOllama(model=local_llm, temperature=0, output_format="json")

# vector store
files = [
  "data/coffee_heaven_sales.csv",
  "data/tech_emporium_sales.csv",
  "data/green_grocers_sales.csv"
]

# load documents
docs = []
for file in files:
  loader = CSVLoader(file)
  docs += loader.load()

# split documents
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
  chunk_size=1000, chunk_overlap=200
)
doc_splits = text_splitter.split_documents(docs)

# add to vector database
vectorstore = SKLearnVectorStore.from_documents(
  documents=doc_splits,
  embedding=NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local")
)

# create retriever
k = min(3, len(doc_splits)) # ensure k does not exceed available chunks
retriver = vectorstore.as_retriever(k=k)
