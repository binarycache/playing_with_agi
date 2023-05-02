import faiss
import numpy as np
import os

class FaissHelper:
    def __init__(self, index_path='diet_plans.index'):
        self.index_path = index_path
        if not os.path.exists(index_path):
            self.index = faiss.IndexFlatL2(768)
            faiss.write_index(self.index, self.index_path)
        else:
            self.index = faiss.read_index(self.index_path)

    def store_vector(self, username, vector):
        self.index.add(vector)
        faiss.write_index(self.index, self.index_path)

    def retrieve_vector(self, index):
        stored_index = faiss.read_index(self.index_path)
        return stored_index.reconstruct(index)
