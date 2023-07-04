import joblib

extention = 'pkl'


def save_vectorizer(vectorizer, filename):
    joblib.dump(vectorizer, f'{filename}.{extention}')


def load_vectorizer(filename):
    return joblib.load(f'{filename}.{extention}')


def save_model(model, filename):
    joblib.dump(model, f'{filename}.{extention}')


def load_model(filename):
    return joblib.load(f'{filename}.{extention}')
