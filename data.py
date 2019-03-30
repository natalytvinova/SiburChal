from __future__ import print_function, division
import os
import numpy as np
import pandas as pd

np.random.seed(238746)


# Data load
data_path = os.path.join("data", "{file}")

train_data = pd.read_csv(data_path.format(file="train_data.csv.zip"), parse_dates=[0], index_col=0)
print(train_data.head())

runs = pd.read_csv(data_path.format(file="train_runs.csv"), index_col="run_id", parse_dates=["run_start", "run_end"])
print(runs.head())

cokes = pd.read_csv(data_path.format(file="train_coke.csv"), parse_dates=["start", "end"])
print(cokes.head())

sample_submission = pd.read_csv(data_path.format(file="sample_submission.csv"), index_col="frame_id")
print(sample_submission.head())

# Visual
import sibur_utils
for cl in train_data.columns:
    sibur_utils.visualize(train_data[cl], runs, cokes[cokes.sensor==cl], cl)

