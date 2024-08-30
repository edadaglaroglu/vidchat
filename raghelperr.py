from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get OpenAI API key from environment variables
my_key_openai = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI ChatGPT-4 model
llm_openai = ChatOpenAI(api_key=my_key_openai, model="gpt-4o")  # Model chosen is 'gpt-4o'
embeddings = OpenAIEmbeddings(api_key=my_key_openai)

# 1. Ask a question to the language model
def ask_openai(prompt):
    AI_Response = llm_openai.invoke(prompt)
    return AI_Response.content

# 2. Retrieval-Augmented Generation (RAG) process using video transcript documents
def rag_with_video_transcript(transcript_docs, prompt):
    # Split the text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len
    )

    splitted_documents = text_splitter.split_documents(transcript_docs)

    # Create a vector store from the split documents
    vectorstore = FAISS.from_documents(splitted_documents, embeddings)
    retriever = vectorstore.as_retriever()

    # Retrieve relevant documents based on the prompt
    relevant_documents = retriever.get_relevant_documents(prompt)

    # Combine the context data from the relevant documents
    context_data = ""
    for document in relevant_documents:
        context_data += " " + document.page_content

    # Formulate the final prompt with context data
    final_prompt = f"""I have the following question: {prompt}
    To answer this question, we have the following information: {context_data}.
    Please answer the question using only the information provided here. Do not go beyond these details. 
    """

    AI_Response = ask_openai(final_prompt)

    return AI_Response, relevant_documents

