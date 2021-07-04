######################################################################
# Author: Thomas Gruber

# Description: The main file Assignment_2
# Comments: Enter the inputfiles
######################################################################

#from abc import ABC,abstractmethod
from info_bme_reader import PickleReader, MnistReader
import info_bme
import numpy as np

            
if __name__ == "__main__":

    reader = MnistReader(".")
    pickle_reader = PickleReader(".")
    pickle_reader.read_data("test_dump.p")

#    tom = info_bme.InfoBme(pickle_reader)
#    array = np.array([1,2])
#    array = tom.get_class(2)[:1000]
#    array = range(1000)

#    indices = tom.get_class(2)
#    tom.calc_balance([1,2,3,4])
#    tom.calc_balance(array)
#    tom.calc_balance("all")
#    tom.calc_means(array, plot = True, plot_name = "new_number.png")
#    tom.calc_hist(array, plot = True, plot_name = "hist.png")
#    tom.calc_bbox(array)
#    
#    
#    a = [1,2,3]
#    b = [4,5,6]
#    
#    a = tom.calc_means(tom.get_class(2), plot = False, plot_name = None)
#    b = tom.calc_means(tom.get_class(3), plot = False, plot_name = None)
#    print(a)
#    tom.calc_cosine_similarity(a, b, plot=True, plot_name = "info_bme_reader/similarity.png")
#    
#    tom.generate_strat_splits(0.001) 
 

    
