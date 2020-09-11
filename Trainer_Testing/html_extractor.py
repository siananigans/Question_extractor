"""
Extract text from website.

"""
import requests
from bs4 import BeautifulSoup


def extract(url):
    session = requests.Session()
    session.max_redirects = 60

    try:
        response = session.get(url).text
        soup = BeautifulSoup(response, 'html.parser')

        for script in soup(["script", "style"]):
            script.extract()


        paragraphs = soup.find_all('p')
        text = ''

        for p in paragraphs:
            text += p.get_text().strip() + ' '

        text.strip()
        return text

    except(requests.TooManyRedirects, requests.ConnectionError):
        print('Website cannot be processed, please copy and paste text instead.')
        return ''