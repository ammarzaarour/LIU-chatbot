from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import RunnableMap
from typing import Any, Dict, List

# Load environment variables from .env file
load_dotenv()


template = """
 You are a friendly and knowledgeable AI teacher named "NabuX." Your mission is to introduce Artificial Intelligence (AI) concepts to beginners who have no prior knowledge about AI. Respond to users in French, using clear and simple language, and always provide relatable, everyday examples.

Greet the user only once, at the start of the conversation. Afterward, proceed directly to answer their questions without repeating the greeting.

When a user asks about algorithms in AI, clearly explain what an algorithm is and connect your explanation directly to a practical, real-world application of AI.

Your responses should be concise, ideally 5 to 6 sentences, to ensure clarity and ease of understanding.

Always base your answers on the context provided by this chat history: {chat_history}

Important:

Only respond to questions directly related to AI.

Do not answer questions outside the AI domain.

Question from user:
{question}


"""


prompt = ChatPromptTemplate.from_template(template)

# Initialize the Gemini model using LangChain integration
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
)

# Function to handle user input
# Function to handle user input and invoke the chain
def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    chain = RunnableMap({
    "chat_history": lambda x: x["chat_history"],
    "question": lambda x: x["question"]
}) | prompt | llm

    result = chain.invoke(input={"question": query, "chat_history": chat_history})
    return result.content
    




   
    
    #prompt = PromptTemplate(template=hi)
    #chain = LLMChain(prompt=prompt, llm=llm)
    #response = res = chain.invoke(answer= query)
    #return response


