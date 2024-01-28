from bs4 import BeautifulSoup as bs

import requests

class Crawler:
    def __init__(self):
        self.headers = {
            'User-Agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }

    def soup(self, url: str) -> list:
        """Filter the HTML of page to get a dataset of the news"""
        request = requests.get(url, 
                                headers=self.headers)
        
        enconde = request.encoding

        if request.status_code != 200:
            print(f"Error - Status Code {requests.status_code}")
        else:
            self.page      = bs(request.text,"html.parser",from_encoding=enconde)
            self.news_list = []

        page_news_div = self.page.find_all('li', class_='css-1l4w6pd')

        for news in page_news_div:
            news_data            = {}
            news_data['Title']   = news.find('h4').text
            news_data['Date']    = news.find_all('span', class_='css-bc0f0m')[0].text.replace('PRINT EDITION','').split(',')[0:2]
            
            if '|' in news_data['Date'][0]:
                news_data['Date'][0] = news_data['Date'][0].split('|')[1]
                news_data['Date']    = news_data['Date'][0] + ',' + news_data['Date'][1]

            elif '|' in news_data['Date'][1]:
                news_data['Date'][1] = news_data['Date'][1].split('|')[1]
                news_data['Date']    = news_data['Date'][0] + ',' + news_data['Date'][1]

            elif news_data['Date'][1].split(" ")[-1] not in ['1','2','3','4','5','6','7','8','9']:
                news_data['Date']    = 'No date specified'

            else:
                news_data['Date']    = news_data['Date'][0] + ',' + news_data['Date'][1]

            try:
                news_data['Description'] = news.find_all('p', class_='css-16nhkrn')[0].text
            except:
                news_data['Description'] = 'No description available'

            if '&' in news_data['Description'] or 'dollars' in news_data['Description'] or 'USD' in news_data['Description']:
                news_data['Any Money'] = True
            else:
                news_data['Any Money'] = False
            
            try:
                news_data['Image Link'] = news.find('img')['src']
                news_data['Image Link'] = news.find('img')['srcset'].split(',')[-1].split(' ')[0]
            except:
                news_data['Image Link'] = 'No image available'

            self.news_list.append(news_data)
        
        return self.news_list
