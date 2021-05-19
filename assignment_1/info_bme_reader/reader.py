from abc import ABC, abstractmethod
import os 
import pickle
import matplotlib.pyplot as plt
import numpy as np


class Reader(ABC):
    
    """ 
        This is the abstract Basic Class
    """
    
    def __init__(self, data_path):
   
        self.data_path = data_path
        self._X = None
        self._y = None
        self._num_rows = None
        self._num_cols = None 
        
# look if the data_path exists        
        if not os.path.isdir(data_path):
            raise FileNotFoundError 
                   

    @abstractmethod        
    def read_data(self):
        raise NotImplementedError
        
        
    def dump(self, dump_path):
        self.dump_path = dump_path
        
        dump_data = {
            "X": self.X,
            "y": self.y, 
            "num_rows": self.num_rows, 
            "num_cols": self.num_cols, 
            }

# split the path in the dictionarys, and the file        
        if len(dump_path.split("/")) > 1:
            directory_list = dump_path.split("/")
            directory = ""
            for counter in directory_list[:-1]:
                directory = directory + counter + "/"
   
            if os.path.isdir(directory[:-1]):
                try:
                    with open(dump_path, "wb") as dump_file:
                        data = pickle.dump(dump_data, dump_file)
                except:  
                    print("[ERROR] Loading input pickle failed")
                    return False
                
            else:
                print("Folder doesn´t exist")
                return
        else:
            try:
                with open(dump_path, "wb") as dump_file:
                    data = pickle.dump(dump_data, dump_file)
            except:  
                print("[ERROR] Loading input pickle failed")
                return False
            
            
    @property
    def X(self):
        return self._X  
        
    @property
    def y(self):
        return self._y
    
    @property
    def num_rows(self):
        return self._num_rows
    
    @property
    def num_cols(self):
        return self._num_cols
    
    @X.setter
    def X (self, new_X):
        print("Please do not change X!!")
   

#plot the sample         
    def plot_sample(self, index, store_path):
        self.index = index
        self.store_path = store_path

        matrix = np.reshape(self.X[index],(self._num_cols,self._num_rows))
        figure = plt.imshow(matrix)
        plt.imsave(self.store_path, matrix)
        
