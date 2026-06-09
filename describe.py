from helper_functions.min import ft_min
from helper_functions.max import ft_max
from helper_functions.avg import ft_avg
from helper_functions.percentile import ft_percentile
from helper_functions.std import ft_std
from helper_functions.variance import ft_variance
from helper_functions.range import ft_range
from helper_functions.skewness import ft_skewness

import csv
import sys
import pandas as pd

COLUMN_WIDTH = 12

def shorten_value(value):
    value = f"{value:.5f}"
    return value[:10] if len(value) > 10 else value

def shorten_header(header):
    return header[:10] if len(header) > 10 else header

if len(sys.argv) != 2:
    print("You need a single file path")
    exit(1)
with open(sys.argv[1]) as file:
    csv_reader = csv.DictReader(file, delimiter=",")
    columns = csv_reader.fieldnames

    float_columns = []
    for col in columns:
        if col.lower() == "index":
            continue
        try:
            all_floats = any(float(row[col]) if row[col] else False for row in csv_reader)
            if all_floats:
                float_columns.append(col)
        except ValueError:
            continue

    file.seek(0)
    csv_reader = csv.DictReader(file, delimiter=",")

    column_values = {col: [] for col in float_columns}
    mean = 0
    for row in csv_reader:
        mean += 1
        for col in float_columns:
            value = row.get(col)
            if value:
                try:
                    column_values[col].append(float(value))
                except ValueError:
                    print(f"Skipping invalid value in column {col}: {value}")


# Shorten column headers before printing
shortened_headers = [shorten_header(col) for col in float_columns]

# Define labels for the statistics rows
labels = ["mean", "min", "avg", "std", "25%", "50%", "75%", "max", "range", "variance", "skewness"]
# Prepare the statistics rows with labels
statistics_rows = [
    [label] + [shorten_value(mean) for col in float_columns] if label == "mean" else
    [label] + [shorten_value(ft_min(column_values[col])) for col in float_columns] if label == "min" else
    [label] + [shorten_value(ft_avg(column_values[col])) for col in float_columns] if label == "avg" else
    [label] + [shorten_value(ft_std(column_values[col])) for col in float_columns] if label == "std" else
    [label] + [shorten_value(ft_percentile(column_values[col], 25)) for col in float_columns] if label == "25%" else
    [label] + [shorten_value(ft_percentile(column_values[col], 50)) for col in float_columns] if label == "50%" else
    [label] + [shorten_value(ft_percentile(column_values[col], 75)) for col in float_columns] if label == "75%" else
    [label] + [shorten_value(ft_max(column_values[col])) for col in float_columns]  if label == "max" else
    [label] + [shorten_value(ft_range(column_values[col])) for col in float_columns] if label == "range" else
    [label] + [shorten_value(ft_variance(column_values[col])) for col in float_columns] if label == "variance" else
    [label] + [shorten_value(ft_skewness(column_values[col])) for col in float_columns]
    for label in labels
]

# Print the column names with a label column
print(f"{'Label':<{COLUMN_WIDTH}} | " + " | ".join(f"{col:<{COLUMN_WIDTH}}" for col in shortened_headers))
print("-" * (COLUMN_WIDTH * (len(shortened_headers) + 4)))

# Print each row of statistics with the label
for row in statistics_rows:
    print(" | ".join(f"{value:<{COLUMN_WIDTH}}" for value in row))

# with open("data/dataset_train.csv", "r") as f :
#     df = pd.read_csv(f)
#     print(df.describe())
