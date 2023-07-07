import pandas as pd
import os

datasets_folder = "datasets"


def get_dataset(filename):
    filepath = os.path.join(datasets_folder, f'{filename}.csv')
    return pd.read_csv(filepath, encoding="latin-1")


def save_dataset(df, filename):
    filepath = os.path.join(datasets_folder, f'{filename}.csv')
    df.to_csv(filepath, index=False)


def from_tsv_to_csv(filename):
    filepath = os.path.join(datasets_folder, f'{filename}.csv')
    df = pd.read_csv(filepath, sep='\t')
    df.to_csv(f'{datasets_folder}/{filename}.csv', index=False)
    return df
