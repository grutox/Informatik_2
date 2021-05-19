######################################################################
# Author: Thomas Gruber
# MatNr: 1625378
# Description: The main file Assignment_1
# Comments: Enter the inputfiles and the magic number!
######################################################################

#from abc import ABC,abstractmethod
from info_bme_reader import PickleReader, MnistReader

            
if __name__ == "__main__":
    reader = MnistReader(".")
    reader.read_data(features=("train-images-idx3-ubyte.gz", 2051),
                      labels=("train-labels-idx1-ubyte.gz", 2049))
    reader.plot_sample(0, "info_bme_reader/mnist.png")
    reader.dump("test_dump.p")
 
    pickle_reader = PickleReader(".")
    pickle_reader.read_data("test_dump.p")
    pickle_reader.plot_sample(10, "pickle.png")
    
