# McDonald's Finder Bot for Telegram 🔥
<table>
<tr>
</tr>
<tr>
<td>
This is a Python-based Telegram bot that allows users to find McDonald's restaurants based on their location and specified preferences. The bot utilizes various features, including distance calculation, ratings, and sentiment analysis, to provide users with accurate and relevant results.
</td>
<td>
<img src="bot_images/logo.png" alt="McDonaBot logo" width="100"/> 

*[freepik.com](https://www.freepik.com)*
</td>
</tr>
</table>

> ### Disclaimer: 
> Please note that this project is developed as a university project and is intended for educational purposes only. It does not have any commercial intentions or affiliations with McDonald's or any other organizations mentioned.

- [McDonald's Finder Bot for Telegram 🔥](#mcdonalds-finder-bot-for-telegram-)
  - [Features](#features)
  - [Getting Started](#getting-started)
  - [Usage](#usage)
  - [Implementation](#implementation)
    - [Preprocessing](#preprocessing)
    - [Analysis based on the number of stars](#analysis-based-on-the-number-of-stars)
    - [Analysis based on the sentiment](#analysis-based-on-the-sentiment)
      - [Homemade classifier](#homemade-classifier)
      - [Library classifier](#library-classifier)
  - [Contributing](#contributing)
  - [License](#license)
  - [Presentazione](#presentazione)

## Features

- **Location-based search**: users can specify their current location or any location of interest to find nearby McDonald's restaurants.
- **Distance filtering**: users can set a maximum distance within which the bot will search for McDonald's restaurants.
- **Rating-based recommendation**: the bot provides the first McDonald's restaurant based on ratings, considering it as the primary recommendation.
- **Sentiment-based recommendation**: the bot provides the the best restaurant based on the analysis of the sentiment of users who have already visited it and left a review.
- **Interactive user interface**: the bot offers a user-friendly interface with step-by-step instructions for smooth interaction.

## Getting Started

1. Clone the repository:

```
git clone 
```

2. Install the required dependencies:

```
pip install python-telegram-bot --upgrade
pip install scikit-learn
pip install nltk
pip install matplotlib
```

3. Run the bot:

```
python bot.py
```

## Usage

1. Start the bot by searching for it on Telegram ([@DonMCbot](https://t.me/DonMCbot)) and clicking the "Start" button.

2. Chose if you want to find a the bestrated McDonald's restaurant or the one with the best sentiment (or both).

3. Enter your location or share your current location with the bot.

4. Specify the maximum distance to search for McDonald's restaurants.

Then the bot will provide the requested recommendation based on ratings or on sentiment analysis.

<div style="display: flex; justify-content: space-between;">
  <img src="bot_images/1start.PNG" alt="Start" width="150"/>
  <img src="bot_images/2chose.PNG" alt="Start" width="150"/>
  <img src="bot_images/2feeling.PNG" alt="Start" width="150"/>
  <img src="bot_images/3location.PNG" alt="Start" width="150"/>
  <img src="bot_images/4result.PNG" alt="Start" width="150"/>
</div>


## Implementation

### Preprocessing

### Analysis based on the number of stars

### Analysis based on the sentiment
In this part is performed sentiment analysis on two different methods.

#### Homemade classifier
Creation of a classifier to obtain the sentiment labels on a different dataset. The dataset contains the message and the sentiment associated. This analysis is contained in [nb_NostroCLF](./nb_NostroCLF.ipynb). 
The steps are: 
  1. Loading of the dataset of chats 
  2. Preprocessing of text
  3. Splitting of the training set 
  4. Training and testing (with a showing of results): This part includes:
     - Passive Agressive Classifier
     - Logistic Regression Classifier
     - Multinomial Naive Bayes Classifier
     - Support Vector Classifier
     - **For each classifier is used a different vectorizer with unigram, bigram, and trigram**
  6. Choosing the best classifier
  7. Saving the model

#### Library classifier
Performing the sentiment analysis of McDonald's reviews dataset with the library "nltk.sentiment". With the function "SentimentIntensityAnalyzer()" the sentiment labels are obtained. 

In the [nb_Progetto](./nb_progetto.ipynb) is perfomed the sentiment analyis with "SentimentIntensityAnalyser()" and our classifier. After that is performed a comparison with these two anlyisis to obtain the best classifier. Following is performed the filtering to search the best restaurant on sentiment. The choose is perfomed by a formula that assign at each restaurant a **score** that is used to find the best. The formula is [(TotalPositive \* 1) + (TotalNeutral \* 0) + (TotalNegative \* (-2))] / TotalReviews* .

## Contributing
Contributions are welcome! If you have any ideas, suggestions, or improvements, please submit a pull request. Make sure to follow the existing code style and include appropriate tests.

One significant contribution to the project would be extending the database to include McDonald's restaurants from countries other than the United States. Currently, the bot focuses on providing recommendations based on the available data within the USA from [McDonald's Store Reviews dataset](https://www.kaggle.com/datasets/nelgiriyewithana/mcdonalds-store-reviews).

## License

This project is licensed under the [MIT License](LICENSE).

## Presentazione

- Definire il problema
- MetStelline
  - risultato bot
- Preprocessing
- MetSia
- MetNostroCLF (capire cosa fa la funzione most_informative_feature_for_class())
    - Tutti i classificatori che abbiamo usato e quello migliore sulla base del acc, ...
- Risultato bot per la classificazione
- Applichiamo i due al dataset del mcdonalds e vediamo (nelle differenze) quale (secondo noi) sia il migliore
- Risultati Finali

## Mail per il prof che mandieamo alla fine

Salve prof, abbiamo fatto. Questa è la nostra repository dove abbiamo i nostri notebook e file python, compreso il chatbot di telegra. Abbiamo scritto anche un readme che comprende sia la descrizione delle funzionalità del bot, sia l’implementazione. Abbiamo anche incluso degli screenshot per essere più chiari.

Sarebbe possibile fare l’esame durante la settimana prossima?
