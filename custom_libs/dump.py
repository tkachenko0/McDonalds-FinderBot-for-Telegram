import joblib
import os

extension = 'pkl'
folder = '../dump_models'


def save_vectorizer(vectorizer, filename):
    filepath = os.path.join(folder, f'{filename}.{extension}')
    print("Saving vectorizer at:", filepath)
    joblib.dump(vectorizer, filepath)


def load_vectorizer(filename):
    filepath = os.path.join(folder, f'{filename}.{extension}')
    print("Loading vectorizer from:", filepath)
    return joblib.load(filepath)


def save_model(model, filename):
    filepath = os.path.join(folder, f'{filename}.{extension}')
    print("Saving model at:", filepath)
    joblib.dump(model, filepath)


def load_model(filename):
    filepath = os.path.join(folder, f'{filename}.{extension}')
    print("Loading model from:", filepath)
    return joblib.load(filepath)
