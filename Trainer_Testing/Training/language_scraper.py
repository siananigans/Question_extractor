"""
Scrape language data (programming and usual languages) from
websites to write to model.

"""
from bs4 import BeautifulSoup
import requests
import pickle


def main():
    endpoint = "https://en.wikipedia.org/wiki/List_of_programming_languages"

    response = requests.get(endpoint)
    soup = BeautifulSoup(response.content)

    # Get all list
    nw_sp = [li.text for li in soup.find_all('li')]
    nw_sp = nw_sp[35:-155]

    # Second url
    url = "https://www.mustgo.com/worldlanguages/languages-a-z/"
    response = requests.get(url)

    soup = BeautifulSoup(response.content)
    nw_sp2 = [li.text for li in soup.find_all('a')]

    nw_sp2 = nw_sp2[10:-70]

    nw_sp3 = nw_sp + nw_sp2

    i = 0

    while i < len(nw_sp3):
        nw_sp3[i] = nw_sp3[i].split()[0].lower()
        i += 1

    # Write to model
    language_model = open('models/language_model', 'wb')
    pickle.dump(nw_sp3, language_model)


if __name__ == '__main__':
    main()
