# coding=utf-8
import os
import pinecone

class IndexStore(object):
    def __init__(self, logger):
        self.__logger = logger
        self.__10k_index_name = "10k-files"
        self.__pinecone_api_key = os.environ['PINECONE_API_KEY']
        self.__pinecone_environment = os.environ['PINECONE_ENVIRONMENT']
        pinecone.init(api_key=self.__pinecone_api_key, environment=self.__pinecone_environment) 

    def create_new_index_from_beginning(self):
        try:
            pinecone.create_index(self.__10k_index_name, dimension=1536, metric="euclidean", pod_type="p1")
            pinecone_index = pinecone.Index(self.__10k_index_name)
        except Exception as e:
            self.__logger.error(f'create pinecone index {self.__10k_index_name} failed, reason: {e}')
            return None
        return pinecone_index

    def check_index_exists(self):
        '''
        Set this flag by hand, to controll should create a new index or not
        TODO: Read this flag from config.
        '''
        # pinecone.delete_index(self.__10k_index_name)
        should_create_index = True
        return should_create_index

    def get_index_by_name(self):
        pinecone_index = pinecone.Index(self.__10k_index_name)
        if pinecone_index is None:
            return None
        else:
            return pinecone_index
    
    def delete_index(self):
        all_pinecone_indices = pinecone.list_indexes()
        print(all_pinecone_indices)
        if self.__10k_index_name in all_pinecone_indices:
            try:
                pinecone.delete_index(self.__10k_index_name)
            except Exception as e:
                self.__logger.error(f'delete index {self.__10k_index_name} failed, reason: {e}')
                return False
        self.__logger.info(f'delete index {self.__10k_index_name} successfully')
        return True


