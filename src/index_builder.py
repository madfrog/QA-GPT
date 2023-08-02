# coding=utf-8

from llama_index import download_loader, VectorStoreIndex, ServiceContext, StorageContext
from llama_index.vector_stores import PineconeVectorStore
from pathlib import Path
from tools.singleton import Singleton
from tools.file_helper import FileHelper
import os
import shutil
import time

from index_store import IndexStore

all_years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
# TODO: to be set
FILE_FOLDER = "C:/Users/Administrator/Desktop/personal_kb_with_gpt/10k_files"
ARCHIVE_FOLDER = 'archive'
NEWEST_FOLDER = 'newest'

class IndexBuilder(object):
    def __init__(self, service_context, logger):
        self.__service_context = service_context
        self.__storage_context = None
        self.__pinecone_index = None
        self.__logger = logger
        self.__index_store = IndexStore(logger)
        self.__loop_continue_run = True

    def __init_index(self):
        # init index store
        should_restore_index_from_db = False
        if self.__index_store.check_index_exists():
            self.__logger.info('store index exists, no need to create a new one')
            pinecone_index_try = self.__index_store.get_index_by_name()
            if pinecone_index_try is not None:
                self.__pinecone_index = pinecone_index_try
                self.__logger.info('try to get pinecone success')
                should_restore_index_from_db = True
            else:
                self.__logger.error('try to get pinecone failed')
                return False, should_restore_index_from_db
        else:
            self.__logger.info("store index doesn't exists, begin to create a new one")
            pinecone_index = self.__index_store.create_new_index_from_beginning()
            if pinecone_index is None:
                self.__logger.error("create store index failed")
                return False, should_restore_index_from_db
            self.__pinecone_index = pinecone_index
        vector_store = PineconeVectorStore(pinecone_index=self.__pinecone_index)
        self.__storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self.__logger.info(f'should restore index from db? [{should_restore_index_from_db}]')
        return True, should_restore_index_from_db

    def build_indices(self):
        init_success, should_restore_index_from_db = self.__init_index()
        if init_success is not True:
            self.__logger.error('init index failed')
            return None, None
        if should_restore_index_from_db is True:
            return self.restore_index_from_db()
        else:
            return self.__build_indices()

    def __build_indices(self):
        # init index
        file_names = FileHelper.get_all_file_names(f'{FILE_FOLDER}/{NEWEST_FOLDER}')
        if len(file_names) == 0:
            self.__logger.debug('no file in newest folder')
            return None, None
        UnstructuredReader = download_loader("UnstructuredReader", refresh_cache=True)
        loader = UnstructuredReader()
        doc_set = {}
        all_docs = []
        for name in file_names:
            new_docs = loader.load_data(file=Path(f'{FILE_FOLDER}/{NEWEST_FOLDER}/{name}'), split_documents=False) 
            # insert metadata into each doc
            # this metadata is important, 
            # it's used for build different index with different 10-k file
            company, year, company_year = FileHelper.get_company_name_and_year(name)
            for doc in new_docs:
                doc.metadata = {"company": company, "year": year}
            doc_set[company_year] = new_docs
            all_docs.extend(new_docs)
        
        # initialize simpel vector indices + global vector index
        index_set = {}
        for name in file_names:
            _, year, company_year = FileHelper.get_company_name_and_year(name)
            cur_index = VectorStoreIndex.from_documents(
                doc_set[company_year],
                service_context=self.__service_context,
                storage_context=self.__storage_context,
            )
            index_set[company_year] = cur_index
            index_set[company_year].index_struct.index_id = company_year

            # if the index was created and stored successfully,
            # move the used file into archive folder,
            # or skip these one and print some error messages.
            self.__logger.debug(f"try to move {name} to archive folder")
            try:
                shutil.move(f'{FILE_FOLDER}/{NEWEST_FOLDER}/{name}', f'{FILE_FOLDER}/{ARCHIVE_FOLDER}/{name}')
            except Exception as e:
                self.__logger.error(f'move {name} to archive folder failed, reason: {e}')
                del index_set[name]
        return file_names, index_set

    def build_index_with_loop(self):
        while self.__loop_continue_run:
            file_names = os.listdir(f'{FILE_FOLDER}/{NEWEST_FOLDER}')
            if len(file_names) > 0:
                self.__logger.debug('newest folder has new files, begin to build indices')
               # self.__build_indices()
            else:
                self.__logger.debug('no new file, continue to watch')
                time.sleep(10)

    def stop_build_index_loop(self):
        self.__loop_continue_run = False

    def _data_loader(self):
        pass

    def restore_index_from_db(self):
        # TODO: how to get file names
        file_names = ['uber-2019.html', 'uber-2020.html']
        metadata_filters = []
        for file_name in file_names:
            company, year, _ = FileHelper.get_company_name_and_year(file_name)
            metadata_filters.append({'company': company, 'year': year})
        self.__logger.debug(f'restore index, metadata filters: {metadata_filters}')

        index_set = {}
        for filter in metadata_filters:
            self.__logger.debug(f'filter: {filter}')
            vector_store = PineconeVectorStore(
                pinecone_index=self.__pinecone_index,
                metadata_filters=filter
                )
            cur_index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store,
            )

            # query_str = (f"What were some of the biggest risk factors in {filter['year']} for Uber?")
            # response = cur_index.as_query_engine(service_context=self.__service_context).query(query_str)
            # print(f'restore query response: {response}')

            company_year = f"{filter['company']}-{filter['year']}"
            index_set[company_year] = cur_index
            index_set[company_year].index_struct.index_id = company_year
        return file_names, index_set


            


        





