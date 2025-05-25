import os

from dotenv import load_dotenv

load_dotenv(override=True)



from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

loader = TextLoader("C:/Users/User/Desktop/liu-chatbot/products/liu.txt", encoding="utf-8")

raw_documents = loader.load()
print(f"loaded {len(raw_documents)} documents")

text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=100)
documents = text_splitter.split_documents(raw_documents)
print(len(documents))

print(f"Going to add {len(documents)} to Pinecone")
PineconeVectorStore.from_documents(documents, embeddings, index_name="liu")
print("****Loading to vectorstore done ***")

