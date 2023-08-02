# coding=utf-8
from langchain.chat_models import ChatOpenAI
import os
import sys
from llama_index import LLMPredictor, ServiceContext

from query_engine_builder import QueryEngineBuilder
from index_builder import IndexBuilder
from tools.logging_helper import get_logger
import threading
import gradio as gr


def init():
    logger = get_logger()
    # Create global service context
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, max_tokens=512, model_name="gpt-4"))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size=1024)
    
    logger.info('begin to build indices...')
    # call index builder to init indices
    index_builder = IndexBuilder(service_context, logger)
    file_names, index_set = index_builder.build_indices()
    if file_names is None or index_set is None:
        logger.error("build index failed, aborting...")
        return -1
    logger.info('finish building indices...')

    # build query engine
    logger.info('begin to build query engine...')
    query_engine_builder = QueryEngineBuilder(service_context, llm_predictor, index_set, file_names, logger)
    global query_engine
    query_engine = query_engine_builder.build_query_engine()
    logger.info('finish building query engine...')

    query_str = (f"Compare/contrast the risk factors described in the Uber 10-K across years. Give answer in bullet points.")
    response = query_engine.query(query_str)
    print(f'restore query response: {response}')

    # start index building loop
    # watch_file_thread = threading.Thread(target=index_builder.build_index_with_loop)
    # watch_file_thread.start()
    return 0


def chatbot(input_text):
    response = query_engine.query(input_text)
    return response.response


if __name__=="__main__":
    if -1 == init():
        sys.exit(0)
    # iface = gr.Interface(fn=chatbot,
    #                      inputs=gr.inputs.Textbox(lines=7, label="输入您的文本"),
    #                      outputs="text",
    #                      title="10-k file Q&A chatbot")
    # iface.launch(share=True)
