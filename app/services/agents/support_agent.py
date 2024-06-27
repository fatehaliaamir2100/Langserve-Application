from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import os
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate

# Set up Pinecone index
index = "bae360"
os.environ["OPENAI_API_KEY"] = ""
os.environ["PINECONE_API_KEY"] = ""

pinecone = Pinecone(api_key="")

chat_llm = ChatOpenAI(
    openai_api_key="",
    model= "gpt-3.5-turbo",
    temperature=0,
    verbose=True,
)      

llm = ChatOpenAI(model="gpt-3.5-turbo")

# Set up OpenAI Embeddings model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1536)

# Load Pinecone index and create vector store
vector_store = PineconeVectorStore(index_name=index, embedding=embedding_model)

# Initialize conversation memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="question",
    return_messages=True
)

# Define template for prompts
prompt_template = """You are an assistant specializing in writing resolution tickets based on data scraped from websites. Your task is to analyze the provided data and compose clear, concise, and effective resolution tickets.

CONTEXT:
{context}

QUESTION: 
{question}
"""

rag_prompt = ChatPromptTemplate.from_template(prompt_template)


# Perform similarity search in vector store
retriever = vector_store.as_retriever()

entry_point_chain = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
)

support_chain = entry_point_chain | rag_prompt | llm | StrOutputParser()
