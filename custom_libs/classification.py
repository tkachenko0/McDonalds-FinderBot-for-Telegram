import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from nltk.sentiment import SentimentIntensityAnalyzer

# import custom modules
import custom_libs.plotting as plotting


class Sentiment:
    NEGATIVE = 'Negative'
    NEUTRAL = 'Neutral'
    POSITIVE = 'Positive'

    @staticmethod
    def get_all():
        return [Sentiment.NEGATIVE, Sentiment.NEUTRAL, Sentiment.POSITIVE]


def train_and_predict(model, x_train, x_test, y_train):
    model.fit(x_train, y_train)
    return model.predict(x_test)


def show_results(y_test, y_pred, class_names):
    accuracy = metrics.accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    print("Classification Report:")
    print(metrics.classification_report(y_test, y_pred))
    cm = metrics.confusion_matrix(y_test, y_pred, labels=class_names)

    plotting.plot_confusion_matrix(cm, classes=class_names)


def test_classifier(model_class, x_train, x_test, y_train, y_test, class_names):
    model = model_class()
    y_pred = train_and_predict(model, x_train, x_test, y_train)
    show_results(y_test, y_pred, class_names)
    return model


def most_informative_feature_for_class(vectorizer, classifier, classlabel, n=10):
    labelid = list(classifier.classes_).index(classlabel)
    feature_names = vectorizer.get_feature_names_out()
    topn = sorted(zip(classifier.coef_[labelid], feature_names))[-n:]

    for coef, feat in topn:
        print(classlabel, feat, coef)


def test_classifiers(model_classes, vectorizers, x_train, x_test, y_train, y_test):
    for model_class in model_classes:
        for i, vectorizer in enumerate(vectorizers):
            model = model_class()
            x_train_trasformed = vectorizer.fit_transform(x_train)
            x_test_trasformed = vectorizer.transform(x_test)
            y_pred = train_and_predict(model, x_train_trasformed, x_test_trasformed, y_train)
            accuracy = metrics.accuracy_score(y_test, y_pred)
            print(f"Accuracy for {model_class.__name__} with vectorizer {i}:", accuracy)
        print("\n")


def predict_sentences(lst_sentences, vectorizer, model, preprocess_function):
    df_test = pd.DataFrame(lst_sentences, columns=['test_sent'])

    if preprocess_function is not None:
        df_test["test_sent"] = df_test["test_sent"].apply(preprocess_function)

    X = vectorizer.transform(lst_sentences)
    prediction = model.predict(X)
    df_test['prediction'] = prediction
    return df_test


def append_sentiment_for_each_row(df, column_name, new_column_name='sentiment'):
    sia = SentimentIntensityAnalyzer()
    sentiment_labels = []
    for text in df[column_name]:
        sentiment = sia.polarity_scores(text)
        compound_score = sentiment['compound']

        if compound_score >= 0.05:
            sentiment_labels.append(Sentiment.POSITIVE)
        elif compound_score <= -0.05:
            sentiment_labels.append(Sentiment.NEGATIVE)
        else:
            sentiment_labels.append(Sentiment.NEUTRAL)

    df[new_column_name] = sentiment_labels
