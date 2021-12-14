from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://rss.nytimes.com/services/xml/rss/nyt/US.xml'
response = requests.get(url).content

with open('nytnewsfeed.xml', 'wb') as f: 
    f.write(response)


def parse_xml(xml_file):
    with open(xml_file, 'r') as f:
        file = f.read()

    soup = BeautifulSoup(file, 'xml')

    df  = pd.DataFrame(columns = ['guid', 'title', 'pubDate', 'description'])

    for item in soup.find_all('item'):
        guid = item.find('guid').text
        title = item.find('title').text
        pubDate = item.find('pubDate').text
        description = item.find('description').text

        row = {'guid': guid,
               'title': title,
               'pubDate': pubDate,
               'description': description}

        df = df.append(row, ignore_index=True)

    return df 
   
df = parse_xml('nytnewsfeed.xml')
df.to_csv('news.csv')