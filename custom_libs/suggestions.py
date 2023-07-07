#this is a suggestion for sentiment analysis funcition

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# Example dataset for sentiment analysis
data = {
    'text': [
        "I love this product, it's amazing!",
        "I'm feeling neutral about this.",
        "I hate Mondays. They make me sad.",
        "The movie was so boring and uninteresting.",
        "The concert was absolutely fantastic! Absolutely outstanding!"
    ],
    'label': ['positive', 'neutral', 'negative', 'negative', 'positive']
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.8, min_df=0.1, ngram_range=(1,2))

# Transform the training and testing data into TF-IDF features
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a linear support vector machine (SVM) classifier
classifier = SVC()
classifier.fit(X_train_tfidf, y_train)

# Perform sentiment analysis on new sentences
new_sentences = [
    "I really enjoy using this product.",
    "I'm not sure how I feel about it.",
    "This book disappointed me.",
    "The performance was outstanding!"
]

# Transform the new sentences into TF-IDF features
new_sentences_tfidf = vectorizer.transform(new_sentences)

# Predict the sentiment labels for the new sentences
predicted_labels = classifier.predict(new_sentences_tfidf)

# Print the predicted sentiment labels
for sentence, label in zip(new_sentences, predicted_labels):
    print(f"Sentence: {sentence}")
    print(f"Sentiment: {label}")
    print("-------------------------------")