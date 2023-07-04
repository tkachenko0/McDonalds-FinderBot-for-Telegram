from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from sklearn.linear_model import PassiveAggressiveClassifier

# import custom modules
import custom_libs.plotting as plotting


def train_and_classify(model, x_train, x_test, y_train):
    model.fit(x_train, y_train)
    return model.predict(x_test)


def test_multinomial_naive_bayes(x_train, x_test, y_train, y_test, class_names):
    model = MultinomialNB()
    pred = train_and_classify(model, x_train, x_test, y_train)
    score = metrics.accuracy_score(y_test, pred)
    show_results(score, y_test, pred, class_names)


def test_passive_aggressive(x_train, x_test, y_train, y_test, class_names):
    model = PassiveAggressiveClassifier()
    pred = train_and_classify(model, x_train, x_test, y_train)
    score = metrics.accuracy_score(y_test, pred)
    show_results(score, y_test, pred, class_names)


def show_results(score, y_test, pred, class_names):
    print("accuracy:   %0.3f" % score)
    cm = metrics.confusion_matrix(y_test, pred, labels=class_names)
    plotting.plot_confusion_matrix(cm, classes=class_names)
