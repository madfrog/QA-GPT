# QA-GPT

## Introduction

QA-GPT is a Q&A project based on chat-GPT, which can be used to build custom Q&A systems. With QA-GPT you can build your own knowledge base and question on your knowledge base. All you need to do is uploading your documents, QA-GPT will split these documents into chunks and transform them into embeddings automatically. Then users can submit questions and get answers about these documents.

Currently, QA-GPT allows users to submit documents in the following formats:

- txt
- pdf
- markdown

It uses Chromadb as an embeddings storage backend, but you can also change it to other vector databases. Once the vectors are created, they will be loaded from the vector database directly when the system starts the next time. This will save the quota of OpenAI API calls.

Use screenshots are showed as following:
![这是图片](./md_files/upload_files.png 'Uploading documents')
![这是图片](./md_files/qa.png 'Q&A')

## Installation

### Install dependencies

```
pip install llama-index==0.7.0
pip install langchain==0.0.223
pip install gradio==3.35.2
pip install openai==0.27.7
pip install chromadb==0.4.3
```

### Set environment variables

Replace variables in start.sh with your own keys, then execute start.sh. Access the portal throught http://127.0.0.1:7860.

## Technical detail

### Documents splitter

### Indexes builder

### Q&A engine builder

## 遗留问题
