# coding=utf-8
import unittest
import pinecone
import os

from llama_index import download_loader, VectorStoreIndex, ServiceContext, StorageContext
from pathlib import Path
from llama_index.vector_stores import PineconeVectorStore
from langchain.chat_models import ChatOpenAI
import os
from llama_index import LLMPredictor, ServiceContext

FILE_FOLDER = "C:/Users/Administrator/Desktop/personal_kb_with_gpt/10k_files"
ARCHIVE_FOLDER = 'archive'
NEWEST_FOLDER = 'newest'

class PineconeComplexTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.__10k_index_name = "10k-files"
        self.__pinecone_api_key = os.environ['PINECONE_API_KEY']
        self.__pinecone_environment = os.environ['PINECONE_ENVIRONMENT']
        pinecone.init(api_key=self.__pinecone_api_key, environment=self.__pinecone_environment) 
        self.__pinecone_index = pinecone.Index(self.__10k_index_name)

        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, max_tokens=512, model_name="gpt-4"))
        self.__service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size=1024)

    def test_restore_index_from_db(self):
        vector_store = PineconeVectorStore(
            pinecone_index=self.__pinecone_index,
            metadata_filters = {"company": "uber", "year": "2019"}
            )
        vector_index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store
        )
        query_str = ("What were some of the biggest risk factors in 2019 for Uber?")
        response = vector_index.as_query_engine(service_context=self.__service_context).query(query_str)
        print(f'restore query response: {response}')
'''
    def test_insert_data(self):
        UnstructuredReader = download_loader("UnstructuredReader", refresh_cache=True)
        loader = UnstructuredReader()
        docs = loader.load_data(file=Path(f'{FILE_FOLDER}/{NEWEST_FOLDER}/uber-2020.html'), split_documents=False) 
        for doc in docs:
            doc.metadata = {"company": "uber", "year": "2020"}

        vector_store = PineconeVectorStore(
            pinecone_index=self.__pinecone_index,
             #metadata_filters = {"company": "uber", "year": "2019"}
            )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        vector_index = VectorStoreIndex.from_documents(
            docs,
            service_context=self.__service_context,
            storage_context=storage_context
        )
        vector_index.set_index_id("uber-2020")
'''


if __name__=="__main__":
    unittest.main()



