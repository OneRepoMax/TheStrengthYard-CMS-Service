from os import environ
import openai
import sys
from dotenv import load_dotenv
# from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import numpy as np
from langchain.vectorstores import Chroma
from tabulate import tabulate

print("Loading environment variables...")
load_dotenv()

openai.api_key = environ.get("OPENAI_API_KEY")

############### PDF LOADER ###############
# Loads all documents from folder and stores them in a variable called <pages> 
# print("Loading all documents from folder and stores them in a variable called <pages>")
# loader = PyPDFDirectoryLoader(path="./docs")
# pages = loader.load()

# # print loaded pages
# sources = [(doc.metadata['source'], doc.metadata['page']) for doc in pages]
# for source, page in sources:
#     print(f'loaded document - {source} - page {page}')

# print("Total pages loaded - ", len(pages))

# print("Page content: ", pages[0].page_content)

############### TEXT LOADER ###############
# Define the path to your scraped text file
print("Loading text document from  and stores them in a variable called <text>")
text_file_path = "./tsy_web_contents.txt"

# Load the text from the specified file
with open(text_file_path, "r", encoding="utf-8") as file:
    text = file.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    length_function=len
)

print("Splitting documents into chunks...")
splits = text_splitter.split_documents(text)

# Import necessary functionality to perform embeddings and store it in a vectorstore
print("Storing files as vector db...")
embedding = OpenAIEmbeddings()

# Define directory to store the vectors
persist_directory = './vectordb'

# Perform embeddings and store the vectors in the above directory in G Drive
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory=persist_directory
)

# Print the number of vectors stored
print(f"Number of vectors stored in the database: {vectordb._collection.count()}")

print("Testing a sample question...")

# Define question and top k chucks to retrieve
question="Who are TSY Trainers?"
k=2

# Retrieve the chucks based on the question and top k chucks
docs = vectordb.similarity_search(question, k)

# The code below prints the top k chucks based on the retrived chucks
# Assuming you have docs as a list of dictionaries, and k is the number of elements in docs
# Also assuming that each doc is a dictionary with the keys 'metadata' and 'page_content'
table_data = []

for i in range(k):
    metadata = docs[i].metadata
    page_content = docs[i].page_content
    source = metadata['source']
    page = metadata['page']
    chunk_data = [i, source, page, page_content]
    table_data.append(chunk_data)

table_headers = ["Chunk", "Source", "Page", "Content"]
table_str = tabulate(table_data, headers=table_headers, tablefmt="grid")

