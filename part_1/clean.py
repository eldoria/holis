import pandas as pd
import re
import numpy as np


def alter_columns_name(cols):
    hashmap = set()
    new_cols = []

    for col in cols:
        if col not in hashmap:
            hashmap.add(col)
            new_cols.append(col)
        else:
            i = 1
            while True:
                new_col = col + f'.{i}'
                if new_col not in hashmap:
                    break
                i += 1
            hashmap.add(new_col)
            new_cols.append(new_col)

    return new_cols


def convert_to_float(x):
    try:
        return float(x)
    except:
        return np.nan


def apply_float_to_series(s):
    return s.apply(convert_to_float)


def clean_file(file):
    """ function created to clean file 2 and 6 """
    df = pd.read_excel(file, engine='calamine')
    df.drop(df.columns[1], inplace=True, axis=1)  # remove english cols

    # remove all the \n in the string cells
    for col in df.select_dtypes(include=[object]).columns:
        df[col].fillna('', inplace=True)
        df[col] = df[col].apply(lambda x: x.replace('\n', ' ').replace('\r', ' '))


    # Ensure all cells are treated as strings (this is important for regex replacement)
    df = df.astype(str)
    # Replace cells that start with a period followed by digits with an empty string
    df.replace('\n', ' ').replace('\r', ' ', inplace=True)
    df.replace(r'^\s+|\s+$', '', regex=True, inplace=True)
    df.columns = [re.sub(r'^\s+|\s+$', '', col).strip() for col in df.columns]

    # Transpose the DataFrame
    df = df.transpose()

    # Use the first row of the transposed DataFrame as the new headers
    df.columns = df.iloc[0]

    # Drop the first row as it's now the header
    df = df[1:].reset_index(drop=True)
    if '' in df.columns:
        df = df.drop(columns=[''], axis=1)
    df = df.loc[:, ~(df == '').all()]

    columns_name = alter_columns_name(df.columns)

    output_file = 'data_pre_processing/' + file.split('/')[1].split('.xlsx')[0] + '.csv'

    df.to_csv(output_file, index=False, header=columns_name)


def clean_file_2(file, usecols):
    df = pd.read_excel(file, usecols=usecols)

    df = df.T
    df.reset_index(inplace=True)
    df.columns = df.iloc[0]
    df.columns.values[0], df.columns.values[1] = 'UUID', 'Unité'
    df = df[1:]

    columns_name = alter_columns_name(df.columns)

    for i in range(len(df.columns)):
        df.columns.values[i] = columns_name[i]
    numerical_columns = [col for col in df.columns if col not in ['UUID', 'Unité']]
    df[numerical_columns] = df[numerical_columns].apply(apply_float_to_series)

    df.to_csv('data_pre_processing/' + file.split('/')[1].split('.xlsx')[0] + '.csv', index=False, header=columns_name)


clean_file('data_post_processing/BI_2.02__02_Procedes_Details.xlsx')
clean_file('data_post_processing/BI_2.02__06_CatImpacts_Details.xlsx')

clean_file_2('data_post_processing/BI_2.02__03_Procedes_Impacts.xlsx', 'D:BIZ')
