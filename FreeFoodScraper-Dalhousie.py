from bs4 import BeautifulSoup
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

MAX_CHARS = 140

# common words that indicate free food
filters = ['Breakfast', 'Lunch', 'Meal', 'Coffee', 'Snacks', 'Refreshments', 'Food', 'Dinner', 'Pizza']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


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
                    if keyword.lower() in html.lower() and 'free' in html.lower():
                        write_tweet(keyword, link)
    print("Scan completed at %s" % strftime("%Y-%m-%d %H:%M:%S", localtime()))


def write_tweet(keyword, link):
    event_date = get_event_date(link['href'])
    tweet = "%s - %s: %s" % (keyword, event_date, link['href'])
    print(tweet)
    api.update_status(status=tweet)


def get_event_date(event_url):
    webpage = requests.get(event_url)
    event_soup = BeautifulSoup(webpage.text, 'html.parser')
    start_date = event_soup.find('time', itemprop="startDate")
    return start_date.get_text() if start_date else "No Date"


print("# Dalhousie Free Food Scraper Started #")
schedule.every().sunday.at('12:00').do(scan_events)

while True:
    schedule.run_pending()
    time.sleep(1)
