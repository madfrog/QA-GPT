# coding=utf-8

import unittest

from index_store import IndexStore

class IndexStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.index_store = IndexStore()
        
    def test_create_new_index(self):
        pinecone_index = self.index_store.create_new_index_from_beginning()
        self.assertIsNotNone(pinecone_index)

    def test_check_index_exists(self):
        exists = self.index_store.check_index_exists()
        self.assertEqual(exists, True)

    def test_delete_index(self):
        result = self.index_store.delete_index()
        self.assertEqual(result, True)


if __name__=="__main__":
    unittest.main()