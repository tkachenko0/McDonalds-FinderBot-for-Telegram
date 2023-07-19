import pandas as pd
from sklearn import metrics
import custom_libs.plotting as plotting
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np


class Sentiment:
    NEGATIVE = 'Negative'
    NEUTRAL = 'Neutral'
    POSITIVE = 'Positive'

    @staticmethod
    def get_all():
        return [Sentiment.NEGATIVE, Sentiment.NEUTRAL, Sentiment.POSITIVE]


def show_results(y_test, y_pred, class_names):
    accuracy = metrics.accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    print("Classification Report:")
    print(metrics.classification_report(y_test, y_pred))
    cm = metrics.confusion_matrix(y_test, y_pred, labels=class_names)

    plotting.plot_confusion_matrix(cm, classes=class_names)


def test_classifier(model_class, vectorizer, x_train, x_test, y_train, y_test):
    model = model_class()
    x_train_trasformed = vectorizer.fit_transform(x_train)
    x_test_trasformed = vectorizer.transform(x_test)
    model.fit(x_train_trasformed, y_train)
    y_pred = model.predict(x_test_trasformed)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    return accuracy


def test_classifiers(model_classes, vectorizers, labels_vectorizers, x_train, x_test, y_train, y_test):
    results = {}
    for model_class in model_classes:
        for i, vectorizer in enumerate(vectorizers):
            accuracy = test_classifier(model_class, vectorizer, x_train, x_test, y_train, y_test)
            print(f"Accuracy for {model_class.__name__} with vectorizer {labels_vectorizers[i]}:", accuracy)

            # insert into results dict the name of the model and an array of accuracies for each vectorizer
            if model_class.__name__ not in results:
                results[model_class.__name__] = [accuracy]
            else:
                results[model_class.__name__].append(accuracy)
        print("\n")
    return results




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

def most_informative_feature_for_class(vectorizer, classifier, classlabel, n=10):
    labelid = list(classifier.classes_).index(classlabel)
    feature_names = vectorizer.get_feature_names_out()
    topn = sorted(zip(classifier.coef_[labelid], feature_names))[-n:]

    for coef, feat in topn:
        print(classlabel, feat, coef)

def vectorize(sentence,model):
    words = sentence.split()
    words_vecs = [model.wv[word] for word in words if word in model.wv]
    if len(words_vecs) == 0:
        return np.zeros(100)
    words_vecs = np.array(words_vecs)
    return words_vecs.mean(axis=0)


def select_best_classifier_from_accuracy(models,x_train, y_train, x_test, y_test):

    best_model = None 

    #test each model in models list
    for model in models:
        
        model_name = model.__name__
        clf = model()
        act_model=  clf.fit(x_train, y_train)
        y_pred = act_model.predict(x_test)
        accuracy = metrics.accuracy_score(y_test, y_pred)
        print(f"Accuracy of {model_name} is {accuracy}")
       
        if best_model is None or accuracy > best_accuracy:
            best_model = act_model
            best_accuracy = accuracy
    
    return best_model
    
