import re
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


def preprocess_dataframe(df, column_name, cleaned_text_column_name,  proprocessing_function):
    df[cleaned_text_column_name] = df[column_name].apply(
        proprocessing_function)


def add_id_column(df, columns):
    df.columns = df.columns.str.strip()
    df['id'] = df.groupby(columns).ngroup()
    num = df['id'].nunique()
    print("Number of unique ids: ", num)


def add_rating_number_column(df):
    """Add a column with the number of rating without the word "star" or "stars"."""
    df.insert(df.columns.get_loc("rating")+1, "rating_number", 0)
    df['rating_number'] = df['rating'].apply(
        lambda x: int(re.sub(r'\b(star|stars)\b', '', x, flags=re.IGNORECASE)))


def preprocess_text(raw_review):

    if (type(raw_review) != str):
        return ""

    # Delete html
    review_text = BeautifulSoup(
        raw_review, 'html.parser').get_text()

    # Make a space
    letters_only = re.sub('[^a-zA-Z]', ' ', review_text)

    # Lower letters
    words = letters_only.lower().split()

    # Delete stopwords
    meaningful_words = [w for w in words if not w in stopwords.words(
        'english')]

    # Lemmitization
    lemmitize_words = lemmatize_words(meaningful_words)

        # Remmove some words
    words_to_be_deleted = ["Mcdonalds", "Mcdonald",
                           "mc donald", "mcd", "order", "\u00BD", "\u00EF"]

    cleaned_words = [w for w in lemmitize_words if not w in
                     [s.lower() for s in words_to_be_deleted]]

    return (' '.join(cleaned_words))

def lemmatize_words(words):
    lemmitize_words = list()

    for word in words:
        # Determine the POS tag for each word
        pos_tag = nltk.pos_tag([word])[0][1][0].lower()

        # Map the POS tag to WordNet tags
        if pos_tag.startswith('j'):
            pos_tag = wordnet.ADJ
        elif pos_tag.startswith('v'):
            pos_tag = wordnet.VERB
        elif pos_tag.startswith('n'):
            pos_tag = wordnet.NOUN
        elif pos_tag.startswith('r'):
            pos_tag = wordnet.ADV
        else:
            pos_tag = wordnet.NOUN  # Default to noun if no specific tag is found

        lemma = WordNetLemmatizer().lemmatize(word, pos=pos_tag)

        lemmitize_words.append(lemma)

    return lemmitize_words