import numpy as np
import pandas as pd


def jitter(d):
    """
    Calculate jitter.
    """
    a = d.values[1:] - d.values[:-1]
    b = d.values[1:]
    c = d.values[:-1]
    return pd.Series(np.mean(np.abs(d.values[1:] - d.values[:-1]), axis=0),
                     index=["_".join([cl, "jitter"]) for cl in d.columns])


def mean_window(d):
    """
    Calculate jitter.
    """

    return pd.Series(d.values[1:], axis=0,
                     index=["_".join([cl, "jitter"]) for cl in d.columns]).rolling(5, min_periods=1).mean()


def variance(d):
    """
    Calculate variance .
    """
    # # calculate mean
    # m = sum(results) / len(results)
    # calculate variance using a list comprehension
    # var_res = sum([(xi - m) ** 2 for xi in results]) / len(results)
    return pd.Series(np.var((d.values[1:]), axis=0),
                     index=["_".join([cl, "jitter"]) for cl in d.columns])


def get_trend(d):
    """
    Calcuate trend for a frame `d`.
    """

    dv = d.reset_index(drop=True)
    dv["minutes"] = np.arange(dv.shape[0], dtype=np.float64)
    covariance = dv.cov()
    return (((covariance["minutes"]) / covariance.loc["minutes", "minutes"])[d.columns]
            .rename(lambda cl: "_".join([cl, "trend"])))


def get_features(frame):
    """
    Calculate simple features for dataframe.
    """

    average_sensors = frame.mean(axis=1)
    average_temp = average_sensors.mean()
    std_temp = average_sensors.std()
    min_temp = average_sensors.min()
    max_temp = average_sensors.max()

    features = []
    features.append(frame.mean().rename(lambda cl: "_".join([cl, "mean"])))
    features.append(frame.std().rename(lambda cl: "_".join([cl, "std"])))
    features.append(frame.min().rename(lambda cl: "_".join([cl, "min"])))
    features.append(frame.max().rename(lambda cl: "_".join([cl, "max"])))

    features.append(frame.mean().rename(lambda cl: "_".join([cl, "mean_norm"])) / average_temp)
    features.append(frame.std().rename(lambda cl: "_".join([cl, "std_norm"])) / std_temp)
    features.append(frame.min().rename(lambda cl: "_".join([cl, "min_norm"])) / min_temp)
    features.append(frame.max().rename(lambda cl: "_".join([cl, "max_norm"])) / max_temp)

    features.append(jitter(frame))
    features.append(variance(frame))  # new
    features.append(mean_window(frame))  # new
    features.append(get_trend(frame))
    features.append(jitter(frame).rename(lambda cl: "_".join([cl, "norm"])) / (max_temp - min_temp))

    features.append(average_sensors.apply(["mean", "std", "min", "max"]))
    return pd.concat(features)