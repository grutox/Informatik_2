###################################################################### 
# Author: Thomas Gruber 
# MatNr: 01625378
#Author: Sophie Zentner
# MatNr: 01610730
#Author: Christina Ebner
# MatNr: 01431092
# Description: The main file 
# Comments: The handwritten numbers are classified with the nearest-neighbor-
#           algorithm 
######################################################################


from sklearn import metrics
import math
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from info_bme import InfoBme
import numpy as np




class InfoBmeClassifier():
    """Classifies given numbers
    """
    
    def __init__(self, info_bme):
        """checks and makes the parameter, inharits the parameter 
        from InfoBme class to InfoBmeClassifier class
        
        Keyword arguments:
        info_bme -- instance of IfoBme class
        
        """
        if not isinstance(info_bme, InfoBme):
            raise TypeError("info_bme is not part of the the mother class!")
        self.info_bme = info_bme
        self.read_data = self.info_bme.read_data
        
    @property
    def X(self):
        return self.info_bme.X
    
    @property
    def y(self):
        return self.info_bme.y
    
        
    
    def classify(self, split_size, k, sample_length, plot_name):
        """
        Carries out the classification by creating test sets and calling
        the nearest neighbor for each set.
        
        Keyword arguments:
        split size -- the size of each split
        k -- Parameter for the call for the nearest neighbor 
        sample_length -- Parameter for the call for the nearest neighbor 
        plot_name -- Parameter that defines the path and name under which the plot should be saved
        
        The return value is a tuple consisting of y_pred and y_true, which are the predicted labels
        and the true labels. 
        """
        
        
        y_true = []
        y_pred = []
        for splits in self.info_bme.generate_strat_splits(split_size):
            labels = self.nearest_neighbor(splits, k, sample_length) 
            for counter in labels:
                y_pred.append(counter)
                
            for label in splits:
                y_true.append(self.y[label])
                
        y_true = y_true[:len(y_pred)]    
        y_pred = np.array(y_pred)
        y_true = np.array(y_true)
                
        if not plot_name == None:
            length = max(self.y) + 1
            cm = np.zeros((length,length))
            y_true_counter = 0
            for y_pred_counter in y_pred:
                if y_pred_counter == y_true[y_true_counter]:
                    cm[y_pred_counter][y_true[y_true_counter]] += 1   
                else:
                    cm[y_true[y_true_counter]][y_pred_counter] += 1
                y_true_counter += 1
            ax = sns.heatmap(cm,annot = True, cmap="YlGnBu")
            ax.set(xlabel = "Predicted label", ylabel = "Ground Truth label")
            ax.set(title = "Confusion matrix")
            plt.savefig(plot_name)

        return_tuple = (y_pred, y_true)
        return (return_tuple)
        
    
    
    def nearest_neighbor(self, test_indices, k, sample_length): 
        """
        Implements a k-nearest neighbor algorithm by searching for each sample of
        the test indices the next similar sample of the rest
        
        Keyword arguments:
        test_indices -- a list of the indices of the currennt test set 
        k -- k=1
        sample_length -- paramter to change the number of the used features
        
        the return value is a numpay array consisting of y_pred, which are the labels
        of the classification
        """
        
        if not isinstance(test_indices, (list, np.ndarray, np.generic)):
            TypeError("test_indices must be a list/np.array")
        y_pred = []
        for indice in test_indices:
            calc_x = self.X[indice]
            biggest_similarity = 0
            label_biggest_similarity = 0
            cosine_similarity = 0
            for counter, value in enumerate(self.X):
                if counter in test_indices:
                    continue
                else:
                    length = math.ceil(sample_length*len(self.X[indice])) 
                    cosine_similarity = self.info_bme.calc_cosine_similarity(calc_x[:length], value[:length])
                if cosine_similarity > biggest_similarity:
                    label_biggest_similarity = self.y[counter]
                    biggest_similarity = cosine_similarity
            y_pred.append(label_biggest_similarity)
        return(y_pred)
    
   
       
    def list_of_points(self, numberOfPoints, indice, test_indices):
        """
        Creates a list of elements with two values of each element, the similarity and
        the digit. 
        
        return value is a list conisting of the similarity as the first element of 
        the list and the digit as the second element of the list
        """
        if not isinstance(test_indices, (list, np.ndarray, np.generic)):
            TypeError("test_indices must be a list/np.array")

        similarity_list = [] 
        for counter, value in enumerate(self.X[:numberOfPoints]):
            if counter in test_indices:
                pass
            else:
                cosine_similarity = self.info_bme.calc_cosine_similarity(self.X[indice], value)

            similarity_list.append([cosine_similarity, self.y[counter]])
        
        return similarity_list


    def getModeValue(self, aList):
        """
        Gets the mode of a list
        Keyword arguments:
        aList -- a list of values
        Return value is the value which occurs the most 
        """
        return max(set(aList), key=aList.count)


    def k_nearest_neighbor(self, test_indices, k, sample_length):
        """
        Implements a k-nearest neighbor algorithm by searching for each sample of the 
        test indices the k-most similar sample 
        
        Keyword arguments:
        test_indices -- a list of the indices of the currennt test set 
        k -- parameter for the k-most similar sample 
        sample_length -- length of the samples; sample_length = 1
        
        the return value is a list consisting those k-points that have the highest
        similarity
        """
        
        knn=[]
        for indice in test_indices:
            knn.append(self.k_nearest_neighborSingleItem(k,indice, test_indices))
#        print(knn)
        return knn


    def k_nearest_neighborSingleItem (self,k, testItem, test_indices):
        """
        Sorts the values by similarity. 
        
        The return value is the mode in the list; the value which appears
        most often
        """
        
        x = len(self.X)
        someKPoints = self.list_of_points(x, testItem, test_indices)

        def getKey(item):
            return item[0]
        nearest = sorted(someKPoints, key=getKey, reverse=True)
        knn=[]
        for i in range(0,k):
            knn.append(nearest[i][1])
        return self.getModeValue(knn)


    
    
    def precision(self, y_true, y_pred):
        """Calculates the precision score of a classification
        using true positive(tp) and false positive(fp) as 
        precision score = tp/(tp+fp)
    
        Keyword arguments:
        y_true -- the true labels
        y_pred -- the predicted labels
        
        the output is a tuple consisting of the global precision score 
        and a dictionary with key: class and value: precision score
        """
        if not isinstance((y_true, y_pred), (list, np.ndarray, np.generic)):
            TypeError("test_indices must be a list/np.array")
        weights = []
        prec_dict = {}  
        prec_list = []
        max_number = max(y_pred)
        for label in range(max_number+1):
            index_list = []
            for i in range(0, len(y_pred)): #where is this number?
                if y_pred[i] == label:
                    index_list.append(i)
            tp = 0
            fp = 0
            
            if not index_list:
                continue
            for index in index_list:
                if y_pred[index] == y_true[index]:
                    tp += 1
                else:
                    fp += 1
            precision_score = tp/(tp+fp)
            prec_list.append(precision_score)
            prec_dict[label] = precision_score
            weight = len(index_list)/len(y_true)
            weights.append(weight)

        prec_list = np.array(prec_list)
        weights = np.array(weights)
        global_list = prec_list*weights
        global_prec = sum(global_list)
        return(global_prec, prec_dict)
    
    
    
    
    def recall(self, y_true, y_pred):
        """Calculates the recall score of a classification
        using true positive(tp) and false negative(fn) as 
        precision score = tp/(tp+fn)
    
        Keyword arguments:
        y_true -- the true labels
        y_pred -- the predicted labels
        
        the output is a tuple consisting of the global recall score 
        and a dictionary with key: class and value: recall score
        """
        if not isinstance((y_true, y_pred), (list, np.ndarray, np.generic)):
            TypeError("test_indices must be a list/np.array")
            
        weights = []
        rec_dict = {}  
        rec_list = []
        max_number = max(y_true)
        for label in range(max_number+1):
            index_list = []
            for i in range(0, len(y_true)): #where is this number?
                if y_true[i] == label:
                    index_list.append(i)
            tp = 0
            fn = 0
            if not index_list:
                continue
            
            for index in index_list:
                if y_pred[index] == y_true[index]:
                    tp += 1
                else:
                    fn += 1
            try:
                recall_score = tp/(tp+fn)
                rec_list.append(recall_score)
                rec_dict[label] = recall_score
                weight = len(index_list)/len(y_true)
                weights.append(weight)
            except ZeroDivisionError:
                print("Can't divide by zero!")
            
        rec_list = np.array(rec_list)
        weights = np.array(weights)
        global_list = rec_list*weights
        global_rec = sum(global_list)
        return(global_rec, rec_dict)
        
            
    def f1_score(self, y_true, y_pred):
        """Calculates the f1 score of a classification
        using the precision score(ps) and recall score(rs) as 
        f1 score = 2 * (ps*rs)/(ps+rs)
    
        Keyword arguments:
        y_true -- the true labels
        y_pred -- the predicted labels
        
        the output is a tuple consisting of the global f1 score 
        and a dictionary with key: class and value: f1 score of class
        """
        if not isinstance((y_true, y_pred), (list, np.ndarray, np.generic)):
            TypeError("test_indices must be a list/np.array")
            
        precision_tuple = self.precision(y_true, y_pred)
        recall_tuple = self.recall(y_true, y_pred)
        
        
        
        try:
            global_f1_score = 2 * ((precision_tuple[0]*recall_tuple[0]) \
                                   /(precision_tuple[0]+recall_tuple[0]))
            f1_dict = {}
            for key_p, value_p in precision_tuple[1].items() :
                value_r = recall_tuple[1][key_p]
                f1_score =  2 * ((value_p*value_r)/(value_p+value_r))
                f1_dict[key_p]= f1_score
        except ZeroDivisionError:
                print("Can't divide by zero!")
            
        return(global_f1_score, f1_dict)
