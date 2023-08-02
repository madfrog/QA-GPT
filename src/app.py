from llama_index import StorageContext, SimpleDirectoryReader, LangchainEmbedding, GPTListIndex, GPTVectorStoreIndex, PromptHelper, LLMPredictor, ServiceContext, load_index_from_storage
from langchain import OpenAI
import gradio as gr
import sys
import os
import logging
os.chdir(r'.')  # 文件路径
#os.environ["OPENAI_API_KEY"] = 'sk-xxxx'

logging.basicConfig(stream = sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream = sys.stdout))


def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 2000
    max_chunk_overlap = 0.1
    chunk_size_limit = 600
    prompt_helper = PromptHelper(
        max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=OpenAI(
        temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))
    documents = SimpleDirectoryReader(directory_path).load_data()
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    index = GPTVectorStoreIndex.from_documents(
        documents, service_context=service_context)
    # index.save_to_disk('index.json')
    index.storage_context.persist('./index')
    return index


def chatbot(input_text):
    # index = GPTVectorStoreIndex.load_from_disk('index.json')
    storage_context = StorageContext.from_defaults(persist_dir='./index')
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    # response = index.query(input_text, response_mode="compact")
    print(response)
    return response.response


iface = gr.Interface(fn=chatbot,
                     inputs=gr.inputs.Textbox(lines=7, label="输入您的文本"),
                     outputs="text",
                     title="AI 知识库聊天机器人")
index = construct_index("docs")
iface.launch(share=True)
