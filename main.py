import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header
from langchain import OpenAI, PromptTemplate
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from message import Message

MAX_TOKENS = 4096

load_dotenv()

app = FastAPI()

# Load the PDF document
pdf_loader = UnstructuredPDFLoader(file_path='text.pdf')
documents = pdf_loader.load()

# Split the documents into chunks for processing
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(documents)


@app.post("/api/send")
def send_message(message: Message, x_api_key_token: str = Header(...)):
    """
    Endpoint for sending a message and receiving a response.

    Parameters:
    - message: The message to be sent (input)
    - x_api_key_token: API key token provided in the request header

    Returns:
    - response: The generated response message
    """
    api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the OpenAI embeddings and vectorstore
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectorstore = Chroma.from_documents(documents, embeddings)

    if x_api_key_token != api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    query = message.message

    # Define the prompt template for generating the response
    template = prompt = """Answer the question based on the vectorstore. If the
    question cannot be answered using the information provided answer
    with "I don't know. Please contact support by email support@nifty-bridge.com".

    Context: Always introduce yourself as NiftyBridge AI assistant when greeting. {vectorstore}

    Question: {query}

    Answer: """
    prompt_template = PromptTemplate(template=template, input_variables=["query", "vectorstore"])

    # Initialize the OpenAI model
    openai = OpenAI(model_name='gpt-3.5-turbo', openai_api_key=api_key, max_tokens=MAX_TOKENS)

    # Perform similarity search in the vectorstore and generate the answer
    docs = vectorstore.similarity_search(query)
    vectorstore_sim = docs[0].page_content

    answer = openai(
        prompt_template.format(
            query=query,
            vectorstore=vectorstore_sim
        )
    )

    if openai.get_num_tokens(answer) > MAX_TOKENS:

    # Handle the message and generate the response
    response = {"message": answer}
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=3000, reload=True)
