import pandas as pd
import numpy as np


def filter_siege_weapons(df):
    condition = df["Skill"] == "Spirit Siegebreaker"
    df.loc[condition, "Name"] = "Siege_" + df.loc[condition, "Name"]
    df.loc[condition, "Class"] = "Siege"
    return df