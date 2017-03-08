from bs4 import BeautifulSoup, SoupStrainer
import requests

url = 'https://www.dal.ca/news/events.html'
webpage = requests.get(url)
root_soup = BeautifulSoup(webpage.text, 'html.parser')

# for all event links check for keywords
for link in root_soup.find_all('a', href=True):
    if '/events/' in link['href']:
        event = requests.get(link['href'])
        event_soup = BeautifulSoup(event.text, 'html.parser')
        result = event_soup.find_all('p')
        for x in result:
            if 'lunch' in x.text:
                print(link['href'])
        #for body in event_soup.find_all('p'):
        #    if 'lunch' in body:
        #        print event_soup