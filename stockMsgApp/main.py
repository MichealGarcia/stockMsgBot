"""This code will use the Twitter API to grab tweets based on keyword searches, limited to the top 50 in each dataframe.

    It will then search through each tweet to find stock tickers associated with the search term "takeover chatter"

    Then it will create a list that will then be turned into a single string.

    This list will be texted through the Twilio API to my phone.
    """


# Import Various Libraries, including Tweepy, a Python library for the Twitter API.

import os
from pyclbr import Function
import re
import tweepy as tw
import pandas as pd
from datetime import date
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

bearer = os.getenv("BEAR")
# consumer_key = os.getenv("TWITTER_API")
# consumer_secret = os.getenv("TWITTER_SECRET")
# access_token = os.getenv("ACCESS")
# access_token_secret = os.getenv("ACCESS_SECRET")

auth = tw.OAuth2BearerHandler(bearer)
api = tw.API(auth)

search_words = "takeover chatter"
today = date.today()
date_since = today - timedelta(days=6)


# Collect tweets
tweets = tw.Cursor(api.search_tweets,
                   q=search_words,
                   tweet_mode='extended').items(500)


# Collect a list of tweets
text = [tweet.full_text for tweet in tweets]


tweet_text = pd.DataFrame(data=text, columns=['text'])
pd.options.display.max_colwidth = 1000
# print(tweet_text)

stocks = []


def tweet_list(tweet_text):

    for column in tweet_text.iteritems():
        # change from tuple to list
        column = list(column)
    return column


def word_list(tweet_list):
    word_list = []
    output_list = []
    for series in tweet_list:
        for row in series:
            word_list.append(row.split(" "))
    output_list = [item for sublist in word_list for item in sublist]
    return output_list


def new_word_list(word_list):
    new_list = []
    for words in word_list:
        # print(words)
        if "$" in words:
            # print(words)
            new_list.append(words)
    return new_list


t_list = tweet_list(tweet_text)
# print(t_list)
t_word_list = word_list(t_list)
# print(t_word_list)
t_stock_list = new_word_list(t_word_list)


# CURRENT PLACE FOR PROJECT, 
print(t_stock_list)

# NEXT FOCUS
# 1. Take list of stocks and remove duplicates
# 2. save data as JSON (i think)
# 3. on to html page
# 4. CSS, etc

t_stock_list = [words.split("\n\n") for words in t_stock_list]
# stocks
numbers_as_str = list(map(str, range(0, 10)))


# create flat list

stocks_list = [item for sublist in stocks for item in sublist]

stocks_list = [word.replace("\n", " ") for word in stocks_list]

stocks_list = list(set(stocks_list))

text_message = [' '.join(word for word in stocks_list)]
text_message = ''.join([i for i in text_message if not i.isdigit()])
text_message = ''.join([i for i in text_message if not i.isdigit()])
def remove_lower(text): return re.sub('[a-z]', '', text)


text_message = remove_lower(text_message)
text_message = re.sub('[\W_]+', ' ', text_message)
text_message = text_message.split()
text_message1 = list(set(text_message))
text_message = " "
text_message = text_message.join(text_message1)
text_message = text_message.replace(" ", ", ")


print(text_message)
