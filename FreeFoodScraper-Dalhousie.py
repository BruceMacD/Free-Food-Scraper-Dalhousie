from bs4 import BeautifulSoup, SoupStrainer
import requests
import urllib2
import tweepy
from time import strftime, localtime
import schedule
import time

# Twitter API setup
consumer_key = 'XXX'
consumer_secret = 'XXX'
access_token = 'XXX'
access_token_secret = 'XXX'


def scan_events():
    # only want links for the next week
    current_date = strftime("%Y-%m-%d", localtime())
    # all public events at Dalhousie are posted here for the next week
    url = 'https://www.dal.ca/news/events.weekOf.html/' + current_date + '.html'
    webpage = requests.get(url)
    root_soup = BeautifulSoup(webpage.text, 'html.parser')
    print("Starting Dalhousie Free Food Scan:")
    # for all event links check for keywords
    for link in root_soup.find_all('a', href=True):
            if '/events/2' in link['href']:
                html = urllib2.urlopen(link['href']).read()
                for keyword in filters:
                    if keyword in html.lower() and 'free' in html.lower():
                        write_tweet(keyword, link)
    print("Scan completed at %s" % strftime("%Y-%m-%d %H:%M:%S", localtime()))


def write_tweet(keyword, link):
    # TODO: find the date of the event for formatting
    tweet = "%s: %s" % (keyword, link['href'])
    print(tweet)
    api.update_status(status=tweet)


# common words that indicate free food
filters = ['breakfast', 'lunch', 'meal', 'coffee', 'snacks', 'refreshments', 'food', 'dinner', 'pizza']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

schedule.every().sunday.at('12:00').do(scan_events)

while True:
    schedule.run_pending()
    time.sleep(1)
