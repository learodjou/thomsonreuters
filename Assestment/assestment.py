"""
Casetext Solutions Engineer Coding Exercise
Lea Rodriguez Jouault
"""

import os
from PyPDF2 import PdfReader
from docx import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI

# OpenAI API Key
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"


def read_pdf(file_path):
    """Read and extract text from a PDF file."""
    doc = PdfReader(file_path)
    text = ''
    for page in doc.pages:
        content = page.extract_text()
        if content:
            text += content
    return text


def read_txt(file_path):
    """Read and extract text from a TXT file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def read_docx(file_path):
    """Read and extract text from a DOCX file."""
    doc = Document(file_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text


def read_file(file_path):
    """Read a file based on its type and return its content."""
    ext = file_path.split('.')[-1].lower()
    if ext == 'pdf':
        return read_pdf(file_path)
    elif ext == 'txt':
        return read_txt(file_path)
    elif ext == 'docx':
        return read_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def list_files(directory, allowed_extensions):
    """List files in a directory filtered by allowed extensions."""
    files = []
    for file in os.listdir(directory):
        if file.split('.')[-1].lower() in allowed_extensions:
            files.append(file)
    return files


def get_user_file_choice(directory, allowed_extensions):
    """Choose a file from the allowed extensions in the specified directory."""
    files = list_files(directory, allowed_extensions)
    
    print('===============================\n')
    print("Available files:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    file_choice = int(input("\nEnter the number of the file you want to process: ")) - 1
    file_path = os.path.join(directory, files[file_choice])
    print('\n===============================\n')
    return file_path

def split_text(raw_text):
    """Split text into chunks."""
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,  # Striding over the text
        length_function = len,
    )
    return text_splitter.split_text(raw_text)

def generate_embeddings(texts):
    """Generate embeddings for the given texts."""
    embeddings = OpenAIEmbeddings()
    return embeddings, FAISS.from_texts(texts, embeddings) # vector store

def create_question_answering_chain():
    """Load Question-answering chain using stuff model."""
    return load_qa_chain(OpenAI(), chain_type="stuff")  

def get_user_query():
    """Prompt the user to input their question."""
    return input("How can I help you?: \n")

def main():
    allowed_extensions = ['pdf', 'txt', 'docx']
    directory = input("Please enter the directory to list files from: ")

    file_path = get_user_file_choice(directory, allowed_extensions)
    raw_text = read_file(file_path)

    texts = split_text(raw_text)
    embeddings, docsearch = generate_embeddings(texts)

    chain = create_question_answering_chain()
    query = get_user_query()

    docs = docsearch.similarity_search(query, k=6)
    input_data = {"input_documents": docs, "question": query}
    response = chain.invoke(input=input_data)

    print('\n===============================\n')
    print(response['output_text'])
    print('\n===============================')

if __name__ == "__main__":
    main()
