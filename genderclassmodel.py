# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

print "hello"

import csv as csv 
import numpy as np

# Open up the csv file in to a Python object
csv_file_object = csv.reader(open('C:/Titanic/train.csv', 'rb')) 
header = csv_file_object.next()  # The next() command just skips the 
                                 # first line which is a header
data=[]                          # Create a variable called 'data'.
for row in csv_file_object:      # Run through each row in the csv file,
    data.append(row)             # adding each row to the data variable
data = np.array(data) 	         # Then convert from a list to an array
			         # Be aware that each item is currently
                                 # a string in this format

data

print data[0]

print data[-1]

print data[0,3]

# The size() function counts how many elements are in
# in the array and sum() (as you would expects) sums up
# the elements in the array.

number_passengers = np.size(data[0::,1].astype(np.float))
number_survived = np.sum(data[0::,1].astype(np.float))
proportion_survivors = number_survived / number_passengers

print number_passengers 
print number_survived 
print proportion_survivors

women_only_stats = data[0::,4] == "female" # This finds where all 
                                           # the elements in the gender
                                           # column that equals “female”
men_only_stats = data[0::,4] != "female"   # This finds where all the 
                                           # elements do not equal 
                                           # female (i.e. male)
print women_only_stats

# Using the index from above we select the females and males separately
women_onboard = data[women_only_stats,1].astype(np.float)     
men_onboard = data[men_only_stats,1].astype(np.float)

print women_onboard
print men_onboard

proportion_women_survived = \
                       np.sum(women_onboard) / np.size(women_onboard)  
proportion_men_survived = \
                       np.sum(men_onboard) / np.size(men_onboard)
                       
print proportion_women_survived 
print proportion_men_survived    

print 'Proportion of women who survived is %s' % proportion_women_survived
print 'Proportion of men who survived is %s' % proportion_men_survived             

test_file = open('C:/Titanic/test.csv', 'rb')
test_file_object = csv.reader(test_file)
header = test_file_object.next()

prediction_file = open("genderbasedmodel.csv", "wb")
prediction_file_object = csv.writer(prediction_file)

prediction_file_object.writerow(["PassengerId", "Survived"])
for row in test_file_object:       # For each row in test.csv
    if row[3] == 'female':         # is it a female, if yes then                                       
        prediction_file_object.writerow([row[0],'1'])    # predict 1
    else:                              # or else if male,       
        prediction_file_object.writerow([row[0],'0'])    # predict 0
test_file.close()
prediction_file.close()

# So we add a ceiling
fare_ceiling = 40
# then modify the data in the Fare column to = 39, if it is greater or equal to the ceiling
data[ data[0::,9].astype(np.float) >= fare_ceiling, 9 ] = fare_ceiling - 1.0

fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size

# Take the length of an array of unique values in column index 2
number_of_classes = len(np.unique(data[0::,2])) 
print number_of_classes

# Initialize the survival table with all zeros
survival_table = np.zeros((2, number_of_classes, number_of_price_brackets))
print survival_table

for i in xrange(number_of_classes):       #loop through each class
  for j in xrange(number_of_price_brackets):   #loop through each price bin

        women_only_stats = data[                          #Which element           
                             (data[0::,4] == "female")    #is a female
                           &(data[0::,2].astype(np.float) #and was ith class
                                 == i+1)                        
                           &(data[0:,9].astype(np.float)  #was greater 
                                >= j*fare_bracket_size)   #than this bin              
                           &(data[0:,9].astype(np.float)  #and less than
                                < (j+1)*fare_bracket_size)#the next bin    
                              , 1]                        #in the 2nd col                           
     						                                    									
    
    
        men_only_stats = data[                           #Which element           
                             (data[0::,4] != "female")    #is a male
                           &(data[0::,2].astype(np.float) #and was ith class
                                 == i+1)                                       
                           &(data[0:,9].astype(np.float)  #was greater 
                                >= j*fare_bracket_size)   #than this bin              
                           &(data[0:,9].astype(np.float)  #and less than
                                < (j+1)*fare_bracket_size)#the next bin    
                              , 1] 
                        
        survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float)) 
        survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float))   
        
survival_table[ survival_table != survival_table ] = 0.
print survival_table   

survival_table[ survival_table < 0.5 ] = 0
survival_table[ survival_table >= 0.5 ] = 1           
print survival_table

test_file = open('C:/Titanic/test.csv', 'rb')
test_file_object = csv.reader(test_file)
header = test_file_object.next()
predictions_file = open("C:/Titanic/genderclassmodel.csv", "wb")
p = csv.writer(predictions_file)
p.writerow(["PassengerId", "Survived"])

for row in test_file_object:                 # We are going to loop
                                              # through each passenger
                                              # in the test set                     
  for j in xrange(number_of_price_brackets):  # For each passenger we
                                              # loop thro each price bin
    try:                                      # Some passengers have no
                                              # Fare data so try to make
      row[8] = float(row[8])                  # a float
    except:                                   # If fails: no data, so 
      bin_fare = 3 - float(row[1])            # bin the fare according Pclass
      break                                   # Break from the loop
    if row[8] > fare_ceiling:              # If there is data see if
                                              # it is greater than fare
                                              # ceiling we set earlier
      bin_fare = number_of_price_brackets-1   # If so set to highest bin
      break                                   # And then break loop
    if row[8] >= j * fare_bracket_size and row[8] < (j+1) * fare_bracket_size:             # If passed these tests 
                                              # then loop through each bin 
      bin_fare = j                            # then assign index
      break        
  
  if row[3] == 'female':                             #If the passenger is female
        p.writerow([row[0], "%d" %int(survival_table[0, float(row[1])-1, bin_fare])])
  else:                                          #else if male
        p.writerow([row[0], "%d" %int(survival_table[1, float(row[1])-1, bin_fare])])
     
# Close out the files.
test_file.close() 
predictions_file.close()

