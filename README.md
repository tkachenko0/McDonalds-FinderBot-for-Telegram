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

2. Chose if you want to find a the best rated McDonald's restaurant or the one with the best sentiment (or both).

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
This section employs two alternative techniques for sentiment analysis.

#### Homemade classifier
A classifier is created to extract the sentiment labels from a distinct dataset. The message and the related sentiment are contained in the dataset. This analysis is carried out in the notebook [nb_NostroCLF](./nb_NostroCLF.ipynb) and the steps are: 
  1. Loading of the dataset of chats 
  2. Preprocessing of text
  3. Splitting in Training set and Test sets
  4. Training and testing of the following classifiers showing also the results:
     - Passive Agressive Classifier
     - Logistic Regression Classifier
     - Multinomial Naive Bayes Classifier
     - Support Vector Classifier

        **A separate vectorizer containing unigram, bigram, and trigram is utilised for each classifier.**

  5. Choosing the best classifier
   <div align="center" style="display: flex; justify-content: space-between;">
      <img src="analysis_images/results_classifiers.png" alt="center" width="300"/>
  </div>
  6. Saving the model

#### Library classifier
Utilising the "nltk.sentiment" library to do sentiment analysis on the McDonald's reviews dataset. The sentiment labels are acquired using the "SentimentIntensityAnalyzer()" method. 

The sentiment analysis is carried out in the [nb_Progetto](./nb_progetto.ipynb) using "SentimentIntensityAnalyser()" and our classifier. The best classifier is then determined by comparing the results of these two analyses. The filtering to choose the best restaurant based on sentiment is then done. 

The choice of the best restaurant is made on the basis of a **score**. The objective of this score is not to overlook information on how many neutral and negative reviews there are as well as positive ones. The logic is to go and assign weights to the different categories with the following formula:

\[
\frac{{(TotalPositive \times 1) + (TotalNeutral \times 0) + (TotalNegative \times (-2))}}{{TotalReviews}}
\]


## Contributing
Contributions are welcome! If you have any ideas, suggestions, or improvements, please submit a pull request. Make sure to follow the existing code style and include appropriate tests.

One significant contribution to the project would be extending the database to include McDonald's restaurants from countries other than the United States. Currently, the bot focuses on providing recommendations based on the available data within the USA from [McDonald's Store Reviews dataset](https://www.kaggle.com/datasets/nelgiriyewithana/mcdonalds-store-reviews).

## License

This project is licensed under the [MIT License](LICENSE).