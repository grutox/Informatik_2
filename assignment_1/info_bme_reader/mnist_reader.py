
from .reader import Reader
import gzip
import os 
import struct


class MnistReader(Reader): 
    
    def __init__(self, data_path):
        super().__init__(data_path)
        self.features_sample = None
        self.features_data = None
        self.labels_sample = None
        
        
    def _check_magic_number(self, features_magic, labels_data):
        try:
            number = int(self.features_number)
        except ValueError:
            print("Magic Number is no integer!")
            
        try:
            number = int(self.labels_number)
        except ValueError:
            print("Magic Number is no integer!")
            
        if self.features_number != features_magic:   
            magic_false = 1
            return magic_false
         
        if self.labels_number != labels_data:   
            magic_false = 1
            return magic_false
        
    
    def read_data(self, features, labels):
        
        self.features_path = features[0]
        self.features_number = features[1]
        self.labels_path = labels[0]
        self.labels_number = labels[1]
        
        if os.path.isfile(self.features_path):
            with gzip.open(self.features_path, "rb") as image_file_feature:
                image = image_file_feature.read()
                
            features_magic = struct.unpack(">i" , image[0:4])
            features_sample= struct.unpack(">i" , image[4:8])
            features_magic = features_magic[0]
            features_sample = features_sample[0]
            
        else:
            print("File doesn´t exist!")
            return
            
            
        if os.path.isfile(self.labels_path):
            with gzip.open(self.labels_path, "rb") as image_file_label:
                image = image_file_label.read()
                
            labels_data = struct.unpack(">i" , image[0:4])
            labels_sample = struct.unpack(">i" , image[4:8])
            labels_data = labels_data[0]
            labels_sample = labels_sample[0]
        else:
            print("File doesn´t exist!")
            return
        
        magic_false = (self._check_magic_number(features_magic, labels_data))
        
        if magic_false == 1:
            print("The magic number, doesn´t fit!")
            return
            
        
        if features_sample != labels_sample:
            print("The number of samples doesn´t fit!!")
            return
            
        
        with gzip.open(self.labels_path, "rb") as image_file_label:  
            label_list = []
            magic_number = struct.unpack(">i" , image_file_label.read(4))[0]
            samples = struct.unpack(">i" , image_file_label.read(4))[0]
            for counter in range(labels_sample):
                image = image_file_label.read(1)
                data = struct.unpack("B", image)[0]
                label_list.append(data)
                
        self._y = label_list

        with gzip.open(self.features_path, "rb") as image_file_features:  
            magic_number = struct.unpack(">i" , image_file_features.read(4))[0]
            samples = struct.unpack(">i" , image_file_features.read(4))[0]
            
            self._num_cols = struct.unpack(">i" , image_file_features.read(4))[0]
            self._num_rows = struct.unpack(">i" , image_file_features.read(4))[0]
            
            number_of_data = self._num_cols*self._num_rows
            big_list = []
            small_list =[]
            for counter in range(samples):
                small_list = []
                
                for counter in range(number_of_data):
                    
                    image = image_file_features.read(1)
                    data = struct.unpack("B",image)[0]
                    small_list.append(data)
                big_list.append(small_list)
            
           
        self._X = big_list
    