import pandas as pd

datasets_folder = "datasets"


def get_dataset(filename):
    return pd.read_csv(f"{datasets_folder}/{filename}.csv", encoding="latin-1")


def save_dataset(df, filename):
    df.to_csv(f"{datasets_folder}/{filename}.csv", index=False)


def from_tsv_to_csv(filename):
    df = pd.read_csv(f'{datasets_folder}/{filename}.tsv', sep='\t')
    df.to_csv(f'{datasets_folder}/{filename}.csv', index=False)
    return df
