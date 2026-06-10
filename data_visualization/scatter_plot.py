import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from helper_functions.min import ft_min
from helper_functions.max import ft_max
from helper_functions.avg import ft_avg
from helper_functions.percentile import ft_percentile
from helper_functions.std import ft_std

import matplotlib.pyplot as plt
import sys
import csv

def ft_correlation(x, y):
    # Pearson correlation
    if len(x) == 0:
        return 0
    
    mean_x = ft_avg(x)
    mean_y = ft_avg(y)
    
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
    denominator = (sum((x[i] - mean_x) ** 2 for i in range(len(x))) * 
                   sum((y[i] - mean_y) ** 2 for i in range(len(y)))) ** 0.5
    
    if denominator == 0:
        return 0
    
    return numerator / denominator

if len(sys.argv) != 2:
    print("You need a single file path")
    exit(1)

with open(sys.argv[1]) as file:
    csv_reader = csv.DictReader(file, delimiter=",")
    
   
    subjects = ['Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 
                'Divination', 'Muggle Studies', 'Ancient Runes', 'History of Magic', 
                'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying']
    
    subject_data = {subject: [] for subject in subjects}
    
    for row in csv_reader:
        for subject in subjects:
            value = row.get(subject)
            if value:
                try:
                    subject_data[subject].append(float(value))
                except ValueError:
                    subject_data[subject].append(None)
            else:
                subject_data[subject].append(None)

max_corr = 0
best_pair = None

max_corr2 = -1
best_pair2 = None

for i, subject1 in enumerate(subjects):
    for j, subject2 in enumerate(subjects):
        if i < j:  # Only check each pair once
            # Filter out None values
            valid_pairs = [(x, y) for x, y in zip(subject_data[subject1], subject_data[subject2]) 
                          if x is not None and y is not None]
            
            if len(valid_pairs) > 0:
                x_vals, y_vals = zip(*valid_pairs)
                corr = ft_correlation(list(x_vals), list(y_vals))
                
                if abs(corr) > abs(max_corr):
                    max_corr = corr
                    best_pair = (subject1, subject2)
                
                if corr > max_corr2:
                    max_corr2 = corr
                    best_pair2 = (subject1, subject2)

print(f"Highest absolute correlation: {best_pair[0]} and {best_pair[1]} (correlation: {max_corr:.4f})")
print(f"Highest positive correlation: {best_pair2[0]} and {best_pair2[1]} (correlation: {max_corr2:.4f})")

# Plot the best pair
valid_pairs = [(x, y) for x, y in zip(subject_data[best_pair[0]], subject_data[best_pair[1]]) 
               if x is not None and y is not None]
x_vals, y_vals = zip(*valid_pairs)

plt.figure(figsize=(8, 6))
plt.scatter(x_vals, y_vals, alpha=0.5)
plt.xlabel(best_pair[0])
plt.ylabel(best_pair[1])
plt.title(f'Scatter Plot: {best_pair[0]} vs {best_pair[1]}\nCorrelation: {max_corr:.4f}')
plt.grid(True, alpha=0.3)
plt.savefig("scatter_plot_positive.png")
plt.show()

valid_pairs2 = [(x, y) for x, y in zip(subject_data[best_pair2[0]], subject_data[best_pair2[1]]) 
               if x is not None and y is not None]
x_vals2, y_vals2 = zip(*valid_pairs2)

plt.figure(figsize=(8, 6))
plt.scatter(x_vals2, y_vals2, alpha=0.5)
plt.xlabel(best_pair2[0])
plt.ylabel(best_pair2[1])
plt.title(f'Scatter Plot: {best_pair2[0]} vs {best_pair2[1]}\nCorrelation: {max_corr2:.4f}')
plt.grid(True, alpha=0.3)
plt.savefig("scatter_plot_absolute.png")
plt.show()
