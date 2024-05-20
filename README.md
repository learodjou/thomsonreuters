# Casetext Solutions Engineer Coding Exercise

This project provides a solution to extract the text content from the files and demonstrates a semantic text search. It reads PDF, TXT, and DOCX files, generates embeddings using OpenAI, and performs question-answering tasks.

## Author
Lea Rodriguez Jouault

## Overview

This script allows you to:
- Read and extract text from PDF, TXT, and DOCX files.
- Split the extracted text into chunks.
- Generate embeddings for the text chunks using OpenAI.
- Perform a similarity search on the text chunks.
- Answer user questions based on the text content.

The code is written in Python using OpenAI API

## Prerequisites

Before running the script, ensure you have the following dependencies installed:
- `os`
- `PyPDF2`
- `python-docx`
- `langchain-openai`
- `langchain`
- `langchain-community`

To run this code, you'll need an OpenAI account and associated API key ([`create a free account here`](https://beta.openai.com/signup)).Set an environment variable called OPENAI_API_KEY with your API key. 
