import grequests
from bs4 import BeautifulSoup as bs
import datetime


def get_news_ecosphere_press():
    """
    :return: [
                {
                    'title': str,
                    'img': bytes,
                    'content': str,
                    'date': datetime,
                    'url': str
                },
            ...]
    """
    response = grequests.get('https://ecosphere.press/news/').send().response
    parser = bs(response.text, 'html.parser')
    info = parser.find_all('h3', attrs={'class': 'elementor-heading-title elementor-size-default'})
    urls = list()
    for tag in info:
        urls.append(tag.a['href'])

    news = list()
    img_urls = list()
    requests = (grequests.get(url) for url in urls)
    for response in grequests.map(requests):
        parser = bs(response.text, 'html.parser')
        title = parser.find('h1', attrs={'class': 'elementor-heading-title elementor-size-default'}).text
        first_text = parser.find('p').text.strip()
        info_block = parser.find('div',
                                 attrs={'class': 'elementor-element '
                                                 'elementor-element-cdd3502 '
                                                 'elementor-widget '
                                                 'elementor-widget-theme-post-content'})
        text = info_block.div.find_all('p')
        text = ' '.join(list(map(lambda x: x.text, text))).strip()
        content = first_text + ' ' + text

        img_url = info_block.img['data-src']
        img_urls.append(img_url)
        # img = grequests.get(img_url).send().response.content

        date = parser.find('span', attrs={'class': 'elementor-icon-list-text elementor-post-info__item '
                                                   'elementor-post-info__item--type-date'})
        date = date.text.strip()

        months = {
            'январ': 1,
            'феврал': 2,
            'март': 3,
            'апрел': 4,
            'ма': 5,
            'июн': 6,
            'июл': 7,
            'август': 8,
            'сентябр': 9,
            'октябр': 10,
            'ноябр': 11,
            'декабр': 12
        }
        time_of_post = date.split(',')[0]
        day, month, year = date.split(',')[1].split()
        for key in months:
            if key in month:
                month = months[key]
                break
        day = int(day)
        year = int(year)
        hour, minute = list(map(int, time_of_post.split(':')))
        date = datetime.datetime(year, month, day, hour, minute)
        dictionary = {
            'title': title,
            # 'img': img,
            'content': content,
            'date': date,
            'url': response.url
        }
        news.append(dictionary)
    requests_images = (grequests.get(img_url) for img_url in img_urls)

    for i, response in enumerate(grequests.map(requests_images)):
        news[i]['img'] = response.content
    return news
