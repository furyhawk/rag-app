# Load
from langchain_community.chat_models import ChatOllama

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain import hub

loader_faq = CSVLoader("docs/faq.csv")  # WebBaseLoader("https://www.uparcel.sg/faq/")
loader_delivery = CSVLoader("docs/del_rate.csv")
loader_txt = TextLoader("docs/surcharge.txt")
load_pdf = PyPDFLoader("docs/uParcel_Rates_13092022.pdf")

loader_all = MergedDataLoader([loader_faq, load_pdf, loader_delivery, loader_txt])
data = loader_all.load()

# Split

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# Add to vectorDB
vectorstore = Chroma.from_documents(
    documents=all_splits,
    collection_name="rag-private",
    embedding=GPT4AllEmbeddings(),
)
retriever = vectorstore.as_retriever()

# Prompt
# Optionally, pull from the Hub
# from langchain import hub
prompt = hub.pull("rlm/rag-prompt-mistral")
# Or, define your own:
# template = """Answer the question based only on the following context:
# {context}

# Question: {question}
# """
# prompt = ChatPromptTemplate.from_template(template)

# LLM
# Select the LLM that you downloaded
ollama_llm = "mistral:latest"  # llama2:7b-chat
model = ChatOllama(model=ollama_llm, temperature=0.5, num_ctx=4096)

# RAG chain
chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | prompt
    | model
    | StrOutputParser()
)


# Add typing for input
class Question(BaseModel):
    __root__: str


chain = chain.with_types(input_type=Question)
