import unittest
import os
import pinecone
import numpy as np

class PineconeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__10k_index_name = "10k-files"
        self.__pinecone_api_key = os.environ['PINECONE_API_KEY']
        self.__pinecone_environment = os.environ['PINECONE_ENVIRONMENT']
        pinecone.init(api_key=self.__pinecone_api_key, environment=self.__pinecone_environment) 
        self.__index = pinecone.Index(self.__10k_index_name)

    def test_get_index(self):
        stats_response = self.__index.describe_index_stats()
        print(f'stats response: {stats_response}')
        self.assertEqual(0, 0)

    def test_fetch_index(self):
        response = self.__index.fetch(["uber"])
        print(f'fetch index: {response}')

    def test_fetch_vector_ids(self):
        response = self.__index.query(
            top_k=3,
            vector=[0] * 1536, # embedding dimension
            namespace='',
            include_values=False,
            include_metadata=True,
            filter={"company": "uber", "year": "2020"}
        )
        print(f'fetch vector id: {response}')

'''
    def insert_data(self):
        # Insert sample data (5 8-dimensional vectors)
        a_vector = np.full([1536], fill_value=1)
        b_vector = np.full([1536], fill_value=2)
        self.__index.upsert([
            ("A", a_vector.tolist()),
            ("B", b_vector.tolist())
        ])
        response = self.__index.fetch(["A", "B"])
        print(f'afeter insert, fetch index: {response}')
'''




if __name__=="__main__":
    unittest.main()