#!/bin/bash

# Fow powershell
$env:OPENAI_API_KEY="xxxxxxxxxxx"
$env:OPENAI_API_BASE="xxxxxxxxxxx"
$env:PINECONE_API_KEY="xxxxxxxxxxxxx"
$env:PINECONE_ENVIRONMENT="xxxxxxxxxxxxxxx"

# For MacOS
export OPENAI_API_KEY="xxxxxxxx"
export OPENAI_API_BASE="xxxxxxxxxx"
export PINECONE_API_KEY="xxxxxxx"
export PINECONE_ENVIRONMENT="xxxxx"

# start the project
python ./src/qa_lc_app.py







