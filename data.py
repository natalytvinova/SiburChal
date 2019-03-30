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
# import sibur_utils
# for cl in train_data.columns:
#     sibur_utils.visualize(train_data[cl], runs, cokes[cokes.sensor==cl], cl)

import sibur_utils
ws = sibur_utils.select_windows(runs.loc[0, "run_start"], runs.loc[0, "run_end"], 40, verbose=False)
print(ws)


def get_window(train_size=0.7):
    ratio = .9
    windows = []

    for run_id, run in runs.iterrows():
        days = (run["run_end"] - run["run_start"]).total_seconds() / (24. * 3600.)
        num_windows = int(days * ratio)

        print("Run %i, duration:" % run_id, run["run_end"] - run["run_start"], days)
        print("Generating windows (%i)..." % num_windows)

        # Note, we use no_overlaps=False for training set
        ws = sibur_utils.select_windows(run["run_start"], run["run_end"], num_windows,
                                        no_overlaps=False, verbose=False)
        ws["run_id"] = run_id
        ws["run_start"] = run["run_start"]
        ws["run_end"] = run["run_end"]
        ws["since_run_start"] = (ws["start"] - run["run_start"]).dt.total_seconds() / (24. * 3600.)
        windows.append(ws)
    windows = pd.concat(windows, axis=0, ignore_index=True)

    train_windows = windows.sample(int(windows.shape[0] * train_size), replace=False).sort_index()
    print("================================================")
    print(train_windows.head())
    print(windows.head())

    cv_windows = windows[~windows.index.isin(train_windows.index)]
    print(cv_windows.head())

    return train_windows


train_windows = get_window()

from features import get_features
train_features = train_windows.apply(lambda row: get_features(train_data.loc[row["start"]:row["end"]]), axis=1)
print(train_features['norm'])
