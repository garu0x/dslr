import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from helper_functions.min import ft_min
from helper_functions.max import ft_max
from helper_functions.avg import ft_avg
from helper_functions.percentile import ft_percentile
from helper_functions.std import ft_std
from sklearn.metrics import accuracy_score

import sys
import pandas as pd
import numpy  as np

def normalize(col):
    col_min = ft_min(col)
    col_max = ft_max(col)
    return [(x - col_min)/ (col_max - col_min) for x in col]

if len(sys.argv) != 2:
    exit(1)

file = pd.read_csv(sys.argv[1], sep=",")

subjects = ['Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 
                'Divination', 'Muggle Studies', 'Ancient Runes', 'History of Magic', 
                'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying']

col1 = []
col2 = []
house_col = []

#creation d'une matrice regroupant par matiere chaque eleve avec sa maison et sa note respective
feature_cols = []
for subject in subjects:
    col = []
    for house, val in zip(file["Hogwarts House"], file[subject]):
        if not pd.isna(val):
            col.append((house, val))
    feature_cols.append(col)

data = file[["Hogwarts House"] + subjects].dropna()
house_col = list(data["Hogwarts House"])


possible_houses = ["Hufflepuff", "Gryffindor", "Ravenclaw", "Slytherin"]
# normalisation
feature_matrix = []
for subject in subjects:
    col = list(data[subject])
    feature_matrix.append(normalize(col))
print(feature_matrix)
features = np.column_stack(feature_matrix)  # shape (n_samples, 13)
print(features)
n_features = features.shape[1]

# labelisation
labeled_houses = {house: [] for house in possible_houses}
for x in house_col:
    for house in possible_houses:
        labeled_houses[house].append(1 if x == house else 0)



for x, y, z, q in zip(labeled_houses["Hufflepuff"], labeled_houses["Gryffindor"], labeled_houses["Ravenclaw"], labeled_houses["Slytherin"]):
    print(f"{x} {y} {z} {q}")

#initialisation des poids du modele
weights = {house: np.zeros(n_features) for house in possible_houses}
biases = {house: 0 for house in possible_houses}

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

learning_rate = 0.1
n_epochs = 1000

for epoch in range(n_epochs):
    print(f"=== epoch {epoch} ===")
    for house in possible_houses:
        labels = np.array(labeled_houses[house])

        z = np.dot(features, weights[house]) + biases[house]
        y_pred = sigmoid(z)
        print(f"==={house}===")
        print(f"z {z}")
        print(f"y_pred {y_pred}")
        error = y_pred - labels
        print(f"error {error}")
        dw = np.dot(features.T, error) / len(labels)
        print(dw)
        db = np.mean(error)
        print(db)

        weights[house] -= dw * learning_rate
        biases[house] -= db * learning_rate
        print(biases[house])
        print(weights[house])

# predicition
# multiplications des weights avec features + biases puis comparaison entre les 4 maisons pour trouver le plus probable
pred = {}
for house in possible_houses:
    z = np.dot(features, weights[house]) + biases[house]
    pred[house] = sigmoid(z)

winner = []
for i in range(len(features)):
    scores = {house: pred[house][i] for house in possible_houses}
    winner.append(max(scores, key=scores.get))
    # print(f"Étudiant {i} → {winner[i]} (score: {scores[winner[i]]:.3f})")


# print(winner)
# print(house_col)
# verification
# print(accuracy_score(winner, house_col))