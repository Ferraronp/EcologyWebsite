from bs4 import BeautifulSoup as bs
import requests
import datetime


def eco_portalsu_parser():
    date = []
    for part in range(1, 5 + 1):
        url = f"https://ecoportal.su//news.html?p={part}"
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        src = requests.get(url, headers= header)
        info = src.content.decode()
        soup = bs(info, 'html.parser')
        news = soup.find_all('div', attrs={"class": "index_anons"})

        for i in news:
            inf = dict()

            inf['url'] = 'https://ecoportal.su' + str(i.a['href'])

            inf['title'] = str(i.a['title']).replace('\xa0', '')

            _url = i.a['style'].split('(')[1][:-3]
            inf['img'] = requests.get('https://ecoportal.su' + _url, headers=header).content

            data = i.div.text.split(' ')
            day, month, year = map(int, data[0].split('/'))
            hour, minute = map(int, data[1].split(':'))
            inf['date'] = datetime.datetime(year, month, day, hour, minute)

            article = bs(requests.get(inf['href'], headers=header).content.decode(), 'html.parser')
            main_text = []
            for i in article.find_all('description'):
                main_text.append(i.text)

            for i in article.find_all('p'):
                main_text.append(i.text)

            inf['content'] = "".join(main_text).replace('\xa0', '')

            inf['article_img'] = requests.get(('https://ecoportal.su' + article.find('newsimage').img['src']), headers=header).content

            date.append(inf)
        return date



