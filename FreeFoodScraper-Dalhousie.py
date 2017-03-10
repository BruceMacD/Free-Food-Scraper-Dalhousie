from bs4 import BeautifulSoup, SoupStrainer
import requests
import urllib2

#common words that indicate free food
filters = ['breakfast', 'lunch', 'meal', 'coffee', 'snacks', 'refreshments', 'food', 'dinner', 'pizza']
# all public events at Dalhousie are posted here
url = 'https://www.dal.ca/news/events.html'
webpage = requests.get(url)
root_soup = BeautifulSoup(webpage.text, 'html.parser')

print("Upcoming events at Dalhousie with free food:")
# for all event links check for keywords
for link in root_soup.find_all('a', href=True):
    # any events have format events/20**, including the year removes rss feed link
    if '/events/2' in link['href']:
        html = urllib2.urlopen(link['href']).read()
        for keyword in filters:
            if keyword in html.lower() and 'free' in html.lower():
                print(link['href'])
                break
