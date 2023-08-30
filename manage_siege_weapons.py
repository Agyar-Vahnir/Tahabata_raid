import pandas as pd
import numpy as np


def filter_siege_weapons(log_in, log_out):
    df = pd.read_csv(log_in, sep=';')
    condition = df["Skill"] == "Spirit Siegebreaker"
    df.loc[condition, "Source"] = "Siege_" + df.loc[condition, "Source"]
    df.to_csv(log_out, index=False, sep=';')
    