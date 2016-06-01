# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:37:53 2016

@author: keunoo.chang
"""


data_test = train_df[['Gender', 'Age', 'Fare']].values
survived = train_df["Survived"].values
model = LogisticRegression()
model.fit(data_train,survived)
predicted = model.predict(data_test)

predictions_file = open("C:/Titanic/mylogit.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["PassengerId","Survived"])
open_file_object.writerows(zip(ids, predicted))
predictions_file.close()
    
    
   