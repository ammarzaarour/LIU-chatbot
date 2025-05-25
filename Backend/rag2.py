from dotenv import load_dotenv


# Load environment variables
load_dotenv(override=True)
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from typing import Any, Dict, List

from langchain import hub
from langchain.prompts import PromptTemplate  # Import PromptTemplate class
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Initialize embeddings and document search
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
docsearch = PineconeVectorStore(index_name="liu", embedding=embeddings)

# Initialize the chat model
chat = ChatOpenAI(verbose=True, temperature=0)


def run_llm2(query: str):
    # Define the prompt template
    prompt_template = PromptTemplate(
        input_variables=["input", "context"],
        template="""
You are LIU Chatbot, a knowledgeable and friendly assistant for the Lebanese International University (LIU). 
Your role is to help students, applicants, and visitors by answering any questions they may have about LIU.

Your responses must:
- Be written in clear and helpful English.
- Be accurate, concise, and easy to understand.
- Provide useful information about LIU's programs, campuses, admissions, fees, student life, instructors, and more.

{context}

If the user asks something outside the scope of LIU, politely inform them that your role is limited to LIU-related topics.

Question: {input}
Assistant Response:
"""
    )

    # Create document chain
    stuff_documents_chain = create_stuff_documents_chain(chat, prompt_template)

    # Manually retrieve relevant documents
    retriever = docsearch.as_retriever()
    docs = retriever.get_relevant_documents(query)

    # --- 🔍 Print retrieved context ---
    print("\n🔍 Retrieved Context\n" + "-"*60)
    for i, doc in enumerate(docs, start=1):
        print(f"\n📄 Document {i}:\n{doc.page_content}\n" + "-"*60)

    # Generate final answer with context
    result = stuff_documents_chain.invoke({
        "context": docs,
        "input": query
    })

    return result


