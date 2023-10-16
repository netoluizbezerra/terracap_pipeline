import pandas as pd
import ast


def add_missing_columns(df1, df2):
    for col in df1.columns:
        if col not in df2.columns:
            df2[col] = None
    return df2

def revert_geometries(df):
    temp =[]
    for i in range(len(df)):
        coord = ast.literal_eval(df.geometry.iloc[i])
        new_temp = []
        for item in coord:
            item.reverse()
            new_temp.append(item)
        temp.append(new_temp)
    return temp
