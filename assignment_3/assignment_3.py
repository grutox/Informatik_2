###################################################################### 
# Author: Thomas Gruber 

#Author: Sophie Zentner

#Author: Christina Ebner

# Description: The main file 
# Comments: The handwritten numbers are classified with the nearest-neighbor-
#           algorithm 
######################################################################

from info_bme_reader import PickleReader, MnistReader
from info_bme_classifier import InfoBmeClassifier
from info_bme import InfoBme
import numpy as np

reader = MnistReader(".")
reader.read_data(features=("t10k-images-idx3-ubyte.gz", 2051), \
                 labels=("t10k-labels-idx1-ubyte.gz", 2049))
#reader.plot_sample(2, "pickle.png")
reader.dump("test_dump.p")

pickle_reader = PickleReader(".")
pickle_reader.read_data("test_dump.p")
#pickle_reader.plot_sample(2, "pickle.png")

file_reader = InfoBme(reader)
#file_reader.get_class(3)

#l = np.array([3, 5])
#file_reader.calc_balance(l)
#file_reader.calc_means([3,6,7], plot = True, plot_name = "plot.jpg")
#file_reader.calc_hist([2, 3], plot = True, plot_name = "histogram.jpg")
#file_reader.calc_cosine_similarity(a = [1, 4, 7, 3, 8, 0, 0, 0], \
#                                   b = [3, 8, 65, 43, 21, 4, 0, 0], \
#                                   plot = True, plot_name = "scatter.jpg")
#file_reader.calc_bbox([3524, 43])


classifer = InfoBmeClassifier(file_reader)

empty_list = []
#for i in classifer.info_bme.generate_strat_splits(0.25):
#    empty_list.append(i)
    

#y_true = [0,1,1,2,4,6,2,3,4,5,6,7,8,9]
#y_pred = [0,1,1,2,3,6,2,6,4,5,6,7,8,9]
#tom = classifer.precision(y_true,y_pred)

#print(tom)
    
a = [1,2,3]
b = [5,6,7]    

#classifer.nearest_neighbor(empty_list[0],a,b)
a = classifer.classify(split_size = 0.1, k = 1, sample_length = 1 ,plot_name = "confusion.png")
precision = classifer.precision(a[0],a[1])
print(precision)
recall = classifer.recall(a[0],a[1])
print(recall)
f1 = classifer.f1_score(a[0],a[1])
print(f1)


