import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def preprocess_dataframe(df, column_name, proprocessing_function):
    df[column_name+"_clean"] = df[column_name].apply(proprocessing_function)


def add_id_column(df, columns):
    df.columns = df.columns.str.strip()
    df['id'] = df.groupby(columns).ngroup()
    num = df['id'].nunique()
    print("Number of unique ids: ", num)

#add a column with the number of rating without the word "star" or "stars"
def add_rating_number_column(df): 
    df.insert(df.columns.get_loc("rating")+1, "rating_number", 0)
    df['rating_number'] = df['rating'].apply(
        lambda x: int(re.sub(r'\b(star|stars)\b', '', x, flags=re.IGNORECASE)))

def preprocess_text1(raw_review):
    review_text = BeautifulSoup(
        raw_review, 'html.parser').get_text()  # delete html

    letters_only = re.sub('[^a-zA-Z]', ' ', review_text)  # make a space

    words = letters_only.lower().split()  # lower letters

    meaningful_words = [w for w in words if not w in stopwords.words(
        'english')]  # delete stopwords
    
    ####################### Rimozione della parola mcDonalds orders #######################
    words_to_be_deleted = ["Mcdonalds","Mcdonald", "mc donald", "mcd" ,"order","\u00BD","\u00EF"]
    
    cleaned_words = [w for w in meaningful_words if not w in 
                     [s.lower() for s in words_to_be_deleted] ]#delete some words
    #####################################################################################

    lemmitize_words = [WordNetLemmatizer().lemmatize(w)
                       for w in cleaned_words]  # lemmitization
    
    return (' '.join(lemmitize_words))  # space join words
