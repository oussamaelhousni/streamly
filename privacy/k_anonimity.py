from sklearn.compose import make_column_selector as selector

numerical_columns_selector = selector(dtype_exclude=object)
categorical_columns_selector = selector(dtype_include=object)


def generalize_number(value):
    interval = 10
    return f"{(value // interval) * interval}-{((value // interval) + 1) * interval}"


def generalize_string(value, k):
    return str(value)[:k]


def k_anonimity(dataframe, columns_to_delete):
    df = dataframe.drop(columns=columns_to_delete)
    numerical_columns = numerical_columns_selector(df)
    categorical_columns = categorical_columns_selector(df)
    df = df[numerical_columns + categorical_columns]
    """
    for column in categorical_columns:
        df[column] = generalize_string(df[column])
    for column in numerical_columns:
        df[column] = generalize_string(df[column])
    """
    return df
