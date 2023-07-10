import numpy as np
import itertools
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def plot_word_cloud(X, class_name, column_name, plt_name):
    plt.figure(figsize=(20, 20))
    wc = WordCloud(max_words=500, width=1600,height=800).generate(" ".join(X[column_name]))
    plt.imshow(wc, interpolation='bilinear')
    plt.title(f'Word cloud for {class_name}, in sentiment version: {plt_name}', fontsize=14)

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    See full source and example: 
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def plot_accuracies(results,labels):  
    """
    this function plots the accuracies of the models in the results dict
    the dict is in the form of {model_name: [accuracies]}
    the labels are the names of the vectorizers with they configuration and are used as xticks. 
    """
    plt.figure(figsize=(10, 10))
    for model_name, accuracies in results.items():
        plt.plot(accuracies, label=model_name)
    
    plt.xticks(np.arange(len(labels)), labels, rotation=45)
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

