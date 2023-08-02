# coding=utf-8

from typing import List
from langchain.schema.document import Document
from langchain.vectorstores.base import VectorStore
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings


class VectorStoreWrapper(object):
    def __init__(self):
        self.__collection_name = "docs_store"
        self.__persisted_dir = "./vector_storage"
        self.__vector_store = None

    def init_vector_store(self):
        '''Should be called for the first time'''
        self.__vector_store = Chroma(
            collection_name=self.__collection_name,
            embedding_function = OpenAIEmbeddings(),
            persist_directory = self.__persisted_dir)
        return self.__vector_store

    def add_docs_to_vector_store(self, docs: List[Document]) -> VectorStore:
        # self.__vector_store = Chroma.from_documents(documents=docs, 
        #                                             collection_name=self.__collection_name,
        #                                             persist_directory=self.__persisted_dir)
        self.__vector_store.add_documents(documents=docs)
        return self.__vector_store
    
    def persist(self):
        self.__vector_store.persist()


