    """This code will use the Twitter API to grab tweets based on keyword searches, limited to the top 50 in each dataframe.
    
    It will then search through each tweet to find stock tickers associated with the search term "takeover chatter"

    Then it will create a list that will then be turned into a single string.

    This list will be texted through the Twilio API to my phone.
    """


#Import Various Libraries, including Tweepy, a Python library for the Twitter API.
import os
import re
from re import search
import tweepy as tw
import pandas as pd
from twilio.rest import Client
from datetime import date
from datetime import timedelta  
from dotenv import load_dotenv
load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)



twilio_phone = os.getenv("TWILIO_PHONE")
personal_phone = os.getenv("PERSONAL_PHONE")
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_words = "takeover chatter"
today = date.today()
date_since = today - timedelta(days=7)


# Collect tweets
tweets = tw.Cursor(api.search,
                       q=search_words,
                       lang="en",
                       since=date_since).items(200)

# Collect a list of tweets
text = [tweet.text for tweet in tweets]

tweet_text = pd.DataFrame(data = text, columns=['text'])
stocks = []


for column in tweet_text.iteritems():
    #change from tuple to list
    column = list(column)
    for series in column:
        for row in series:
            word_list = row.split(" ")
            for words in word_list:
                if "$" in words:
                    stocks.append(words)
                   

stocks = [words.split("\n\n") for words in stocks]

numbers_as_str = list(map(str, range(0,10)))




#create flat list

stocks_list = [item for sublist in stocks for item in sublist]

stocks_list = [word.replace("\n", " ") for word in stocks_list]

stocks_list = list(set(stocks_list))

text_message = [' '.join(word for word in stocks_list)]
text_message
text_message = ''.join([i for i in text_message if not i.isdigit()])
text_message = ''.join([i for i in text_message if not i.isdigit()])
remove_lower = lambda text: re.sub('[a-z]', '', text)
text_message = remove_lower(text_message)
text_message = re.sub('[\W_]+', ' ', text_message)
text_message = text_message.split()
text_message1 = list(set(text_message))
text_message = " "
text_message = text_message.join(text_message1)
text_message
text_message = text_message.replace(" ", ", ")
text_message




print(client)
message = client.messages \
                .create(
                     body=f"-\nHere are the most discussed stocks in takeover chatter:\n {text_message}",
                     from_=twilio_phone,
                     to=personal_phone
                 )
print(message.sid)
