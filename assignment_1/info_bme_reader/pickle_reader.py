from .reader import Reader
import os 
import pickle

class PickleReader(Reader):
    def __init__(self, data_path):   
        super().__init__(data_path)
        
        
    def read_data(self, name):

#check if the path exists        
        if not os.path.isfile(self.data_path + "/" + name):
            print("[ERROR] Input pickle '%s' not found."%name)
            return
        
#open the pickle and store the data
        with open(self.data_path + "/" + name, "rb") as input_pickle:
            pickle_data = pickle.load(input_pickle)
            
        self._X = pickle_data["X"]
        self._y = pickle_data["y"]
        self._num_cols = pickle_data["num_cols"]
        self._num_rows = pickle_data["num_rows"]
            


        