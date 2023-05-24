import os
from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKey
from fastapi.security import APIKeyHeader
from langchain.vectorstores import Chroma
from langchain import OpenAI, PromptTemplate
from langchain.text_splitter import SpacyTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import VectorDBQA
from decouple import config
from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from schemas import Item

os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')

app = FastAPI(title='NiftyBridge AI assistant', debug=True)
llm = OpenAI(model_name='gpt-3.5-turbo')

api_key_header = APIKeyHeader(name="OPENAI_API_KEY", auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    print(api_key_header)
    if api_key_header == config('OPENAI_API_KEY'):
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )


@app.post("/")
async def chat(item: Item, api_key: APIKey = Depends(get_api_key)):
    loader = PyPDFLoader("Untitled 5.pdf")
    doc = loader.load()
    text_splitter = SpacyTextSplitter(chunk_size=1000)
    text_and_embeddings = text_splitter.split_documents(doc)
    embeddings = OpenAIEmbeddings()
    template = ''' 
    Answer only questions that are relevant to the data from file.
    If a user says hello to you answer with "Hello I am NiftyBridge AI assistant.".
    If the question not relevant to the Nifty Bridge answer with "Your question not relevant to Nifty Bridge".
    If the question cannot be answered using the information provided answer
    with "I don't know please contact with support by email support@nifty-bridge.com".
    
    Question: {question}

    Answer: '''
    prompt = PromptTemplate(template=template, input_variables=['question'])
    question = item.dict()['message']
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(text_and_embeddings, embeddings)
    qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=vectordb)
    query = prompt.format(question=question)
    return {"message": qa.run(query)}

