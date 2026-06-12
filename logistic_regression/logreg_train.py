import csv
import sys
import pandas as pd 
import os
import numpy as np
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from helper_functions.min import ft_min
from helper_functions.max import ft_max

#adding bias to the features
def add_bias(x):
     return np.c_[np.ones(x.shape[0]), x]

#used for the logistic regression
def sigmoid(z):
     return 1/ (1 + np.exp(-z))

#need to normalize the features
def normalize(col):
    col_min = np.nanmin(col)
    col_max = np.nanmax(col)
    return [(x - col_min)/ (col_max - col_min) for x in col]

# function to plit the the training set into a training and testing set
def train_test_split(file):
    entries = len(file)

    test_indices = random.sample(
        range(entries),
        int(0.2 * entries)
    )

    train_indices = [
        i for i in range(entries)
        if i not in test_indices
    ]

    file_test = file.loc[test_indices]
    file_train = file.loc[train_indices]

    return file_train, file_test

if (len(sys.argv) != 2):
    exit(1)

file = pd.read_csv(sys.argv[1], sep=",")
print(file)


#getting training and testing set
train, test = train_test_split(file)
print(train)
print(test)

subjects = ['Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 
                'Divination', 'Muggle Studies', 'Ancient Runes', 'History of Magic', 
                'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying']

houses = ["Hufflepuff", "Gryffindor", "Ravenclaw", "Slytherin"]

#Getting a clean matrix from the features
features = train[subjects].to_numpy().reshape(-1, len(subjects))
normalized_features = features.copy().astype(float)
for i in range(features.shape[1]):
        normalized_features[:, i] = normalize(features[:, i])
print(normalized_features)




#Getting clean category matrix
category = {}
for house in houses:
    col = []
    for row in train["Hogwarts House"]:
        if (row == house):
            col.append(1)
        else:
            col.append(0)
    category[house] = col

# print(category)

features= add_bias(features)
print(features)

epoch = 1000
learning_rate = 0.1

def gradient_descent(x, y, learning_rate, iterations):
    weights = np.zeros(x.shape[1])

    for i in range(epoch):
          predictions = sigmoid(x @ weights)
          gradient = (x.T @ (predictions - y)) / len(y)
          weights -= learning_rate * gradient

    return weights