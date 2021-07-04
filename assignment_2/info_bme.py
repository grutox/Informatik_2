######################################################################
# Author: Thomas Gruber

# Description: The main file Assignment_2
# Comments:
######################################################################

from info_bme_reader import PickleReader, MnistReader, reader
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import os
import math
import numpy as np


class InfoBme:
    def __init__(self,info_bme_reader):
        self.info_bme_reader = info_bme_reader
        self.read_data = reader.abstractmethod
        
        if not isinstance(info_bme_reader,reader.Reader):
            print("Sorry this isn´t a Instance from the Class")
             
    @property
    def X(self):
        return self.info_bme_reader.X
        
    @X.setter
    def X (self, new_X):
        print("Please do not change X!!")
    
    @property
    def y(self):
        return self.info_bme_reader.y
    @property
    def num_rows(self):
        return self.info_bme_reader.num_rows
    
    @property
    def num_cols(self):
        return self.info_bme_reader.num_cols
    
#returned the indices of the label
    def get_class(self,label):
        list_array = []
        
        if not label in self.y:
            print("please enter a correct label!!")
            return
            
        else:
            counter = 0
            for pointer in self.y:
                if label == pointer:
                    list_array.append(counter)
                counter += 1
            
        numpy_array = np.array(list_array)  
        return numpy_array
#returned a dict 
    def calc_balance(self,indices):
        new_list = dict()
        if type(indices) == str:
            if indices == "all":
                for number in range(10):
                    counter = 0
                    for counter_y in self.y:
                        if number == counter_y:
                            counter += 1
                    new_list[number] = counter
                            
            else:
                print("please enter the correct indices")
                return
        else:
            for number in range(10):
                counter = 0
                for number_indices in indices:
                    if self.y[number_indices] == number:
                        counter += 1
                        
                new_list[number] = counter
        return(new_list)
                
  
#returned  array with the mean pixels     
    def calc_means(self,indices, plot, plot_name):
        all_pictures =[]
        
        new_picture = []            
        for pixel in range(self.num_cols * self.num_rows):
            mean = 0
            for number_indices in indices:
                mean = mean + self.X[number_indices][pixel]
            mean = mean/len(indices)
            new_picture.append(mean)
        all_pictures.append(new_picture)
            
        all_pictures_np = np.array(all_pictures)

        if plot == True:
            if plot_name != None:
                if len(plot_name.split("/")) > 1:
                    directory_list = plot_name.split("/")
                    directory = ""
                    for counter in directory_list[:-1]:
                        directory = directory + counter + "/"
           
                    if not os.path.isdir(directory[:-1]):
                        print("Folder doesn´t exist")
                        return
                
                matrix = np.reshape(all_pictures,(self.num_cols,self.num_rows))
                figure = plt.imshow(matrix)  
                plt.imsave(plot_name, matrix)
                plt.close("all")
                  
            else:
                raise FileNotFoundError 
                
        return all_pictures_np    
        
# returned a dict how often the value is in the label      
    def calc_hist(self, indices, plot, plot_name):
        
        list_pixel = dict()

        for number_indices in indices:
            for pixel in self.X[number_indices]:      
                if not pixel in list_pixel:
                    list_pixel[pixel] = 1          
                else:
                    list_pixel[pixel] +=1
        
        
        x_values = sorted(list_pixel.keys())
        y_values = []
        for counter in x_values:
            y_values.append(list_pixel[counter])

        summe = 0
        for i in list_pixel.values():
            summe = summe + i


        if plot == True:
            if plot_name != None:
                if len(plot_name.split("/")) > 1:
                    directory_list = plot_name.split("/")
                    directory = ""
                    for counter in directory_list[:-1]:
                        directory = directory + counter + "/"
           
                    if not os.path.isdir(directory[:-1]):
                        print("Folder doesn´t exist")
                        return

                figure, axis = plt.subplots()
                axis.set_yscale("log")
                axis.fill_between(x_values,y_values, step = "mid")
                figure.savefig(plot_name)
                plt.close("all")
                
            else:
                raise FileNotFoundError 
        return(list_pixel)
        
# calc the smallest box for the samples    
    def calc_bbox(self, indices):
        if type(indices) == str:
            if indices == "all":
                indices = self.y

            else:
                print("Please enter the Correct Indices")
                return

        big_list = []
        for number in indices:  
            list_p0 = []
            list_p1 = []
            list_tuples = []
            
            array = np.reshape(self.X[number],(self.num_cols, self.num_rows))
            rows_counter = 0
            found_pixel = False
            small_row = self.num_rows
            small_col = self.num_cols
            
            for rows in array:
                cols_counter = 0
                for pixel in rows:
                    if pixel != 0:
                        
                        if rows_counter < small_row:
                            small_row = rows_counter

                        if cols_counter < small_col:
                            small_col = cols_counter 
                        break
                    cols_counter += 1
                rows_counter += 1
                
            row_po = small_row 
            col_po = small_col 
            
            list_p0.append(row_po)
            list_p0.append(col_po)
            
            list_tuples.append(list_p0)
            rows_counter = self.num_rows
            big_col = 0
            big_row = 0
            
            for rows in array[::-1]:
                cols_counter = self.num_cols
                for pixel in rows[::-1]:
                    if pixel != 0:
                        if rows_counter > big_row:
                            big_row = rows_counter
                        
                        if cols_counter > big_col:
                            big_col = cols_counter
                        break
                    cols_counter -= 1
                rows_counter -= 1
            
            row_p1 = big_row - 1
            col_p1 = big_col - 1
            
            list_p1.append(row_p1)
            list_p1.append(col_p1)
            
            list_tuples.append(list_p1)
            big_list.append(list_tuples)
            
        row_p0 = self.num_rows
        col_p0 = self.num_cols
        row_p1 = 0
        col_p1 = 0
        
        for tuples in big_list:
            if tuples[0][0] < row_p0:
                row_p0 = tuples[0][0]
                
            if tuples[0][1] < col_p0:
                col_p0 = tuples[0][1]
                
            if tuples[1][0] > row_p1:
                row_p1 = tuples[1][0]
                
            if tuples[1][1] > col_p1:
                col_p1 = tuples[1][1]

        list_p0 = [row_p0,col_p0]
        list_p1 = [row_p1, col_p1]
        big_list = [list_p0,list_p1]  
        return(big_list)

# returned the cosine similariry  
    def calc_cosine_similarity(self, a, b, plot, plot_name):
        
        if len(a) != len(b):
            print("a & b must have the same size")
            return

        sum_1 = 0
        for counter in range(len(a)):
            sum_1 = sum_1 +(a[counter]*b[counter])
            
        sum_a = 0
        for counter in range(len(a)):
            sum_a = sum_a + (a[counter]**2)
            
        sum_b = 0
        for counter in range(len(b)):
            sum_b = sum_b + (b[counter]**2)
            
        similarity = sum_1/((sum_a**(1/2))*(sum_b**(1/2)))

        
        if plot == True:
            if plot_name != None:
                if len(plot_name.split("/")) > 1:
                    directory_list = plot_name.split("/")
                    directory = ""
                    for counter in directory_list[:-1]:
                        directory = directory + counter + "/"
           
                    if not os.path.isdir(directory[:-1]):
                        print("Folder doesn´t exist")
                        return
                
                fig = plt.figure()
                plt.scatter(a,b)
                
                fig.savefig(plot_name)
                plt.close("all")
                
                
            else:
                raise FileNotFoundError 
        return similarity
# generates splits of the labels    
    def generate_strat_splits(self,size):
        all_labels = self.calc_balance("all")
        small_label = sorted(all_labels.values())[0]
        number_samples = math.ceil(small_label * size) - 1
        indices = dict()
        indices_split = dict()
        
        for indices_counter in all_labels.keys():
            indices[indices_counter] = self.get_class(indices_counter)

        for split_counter in range(math.ceil(1/size)):
            list_indices = []
            for sample in range(number_samples):
                indices_counter = (split_counter * number_samples) + sample
                for number in all_labels.keys():
                    list_indices.append(indices[number][indices_counter])
                    
            indices_split[split_counter] = list_indices
        
        for split in indices_split.values():
            np_array = np.array(split)
            yield np_array
        
       
            
            
        
        
        
            
       
            

   
  
