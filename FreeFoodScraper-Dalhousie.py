from bs4 import BeautifulSoup, SoupStrainer
import requests
import urllib2
import tweepy
from time import strftime, localtime

# all public events at Dalhousie are posted here
url = 'https://www.dal.ca/news/events.html'
# Twitter API setup
consumer_key = 'XXX'
consumer_secret = 'XXX'
access_token = 'XXX'
access_token_secret = 'XXX'


def scan_events():
    webpage = requests.get(url)
    root_soup = BeautifulSoup(webpage.text, 'html.parser')
    print("Starting Dalhousie Free Food Scan:")
    # for all event links check for keywords
    for link in root_soup.find_all('a', href=True):
        # only want links for the next week
        current_day = strftime("%d", localtime())
        current_month = strftime("%Y/%m/", localtime())
        # while date in url < current datetime
        for day in range(int(current_day), int(current_day) + 7):
            if '/events/'+current_month+current_day in link['href']:
                html = urllib2.urlopen(link['href']).read()
                for keyword in filters:
                    if keyword in html.lower() and 'free' in html.lower():
                        write_tweet(keyword, link)


def write_tweet(keyword, link):
    tweet = "%s: %s" % (keyword, link['href'])
    print(tweet)
    # api.update_status(status=tweet)


# common words that indicate free food
filters = ['breakfast', 'lunch', 'meal', 'coffee', 'snacks', 'refreshments', 'food', 'dinner', 'pizza']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

scan_events()
