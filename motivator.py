import random
import time
import tweepy
import pandas
from config import consumer_key, consumer_secret, access_token, access_token_secret

#Declare variables
timer = 10800 # three hours
df = pandas.read_csv('quotes.csv', delimiter='*')
index = df.index
number_of_rows = len(index)

# authenticate the consumer key and secret
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)

# authentication of access token and secret
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)


# Get a follower and add return their tag to add to the string to be sent
def getUser():
    follows = []
    for follower in tweepy.Cursor(api.followers).items():
        follows.append(follower.screen_name)
    # Random number to choose user
    follow_rand = random.randint(0,(len(follows)-1))
    followName = follows[follow_rand]
    preString = "Hey @{f} ".format(f=followName)

    return preString

# Get a quote from th CSV
def getQuote():
    quote_picker = random.randint(0,(number_of_rows - 1))
    quote = df['quote'][quote_picker]
    author = df['author'][quote_picker]
    quoteFormat = "{quote} -{author} ".format(quote=quote, author=author)

    return quoteFormat

# This is the main loop. 
while True:
    print('starting Loop')
    quoteString = ''
    userChoose = random.randint(0,3)
    if userChoose <1:
        quoteString += getUser()

    quoteString +=  getQuote()
    sleepSecs = random.randint(0,timer)
    print(quoteString)
    print(sleepSecs)
    #Try the API Call. One possible error is 187, which is an error coming from Twitter that limits tweeting the same tweet out multiple times. 
    # I can't find any documentation from Twitter on the timeframe tht they're looking for, so what I'm doing is going back to the start of 
    # the loop if I see an error, because the liklihood that it will come back with another quote that will violate Twitter's policies is slim 
    # to none, and even if it does it will just keep trying quotes until it gets something that works.
    try:
        api.update_status(status = quoteString)
    except tweepy.TweepError as e:
        print('Error Code', e.api_code)
        print('Reason', e.reason)
        continue

    
    time.sleep(sleepSecs)

