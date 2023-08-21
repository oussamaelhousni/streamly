import numpy as np
import pandas as pd


def add_noise(x, epsilon):
    noise = np.random.laplace(0, epsilon)
    return x + noise


def generalize_string(value):
    k = len(value) // 2
    return (
        str(value)[:k] + "".join(["*" for item in range(len(value) - k)])
        if len(value) > 5
        else value
    )


def privacy(dataframe, columns_to_delete):
    if type(dataframe) == dict:
        for column in columns_to_delete:
            dataframe.pop(column)
        for key, value in dataframe.items():
            if type(value) == str:
                dataframe[key] = generalize_string(value)
            else:
                dataframe[key] = add_noise(value, 0.1)
        return dataframe
    new_df = dataframe.drop(columns_to_delete)
    for column in new_df.columns:
        if pd.api.types.is_numeric_dtype(new_df[column]):
            new_df[column] = new_df[column].apply(lambda x: add_noise(x, 0.1))
        else:
            new_df[column] = new_df[column].apply(generalize_string)
    return new_df
