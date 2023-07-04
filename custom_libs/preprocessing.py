import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def preprocess_text1(raw_review):
    review_text = BeautifulSoup(
        raw_review, 'html.parser').get_text()  # delete html

    letters_only = re.sub('[^a-zA-Z]', ' ', review_text)  # make a space

    words = letters_only.lower().split()  # lower letters

    meaningful_words = [w for w in words if not w in stopwords.words(
        'english')]  # delete stopwords

    lemmitize_words = [WordNetLemmatizer().lemmatize(w)
                       for w in meaningful_words]  # lemmitization

    return (' '.join(lemmitize_words))  # space join words
