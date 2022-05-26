from bs4 import BeautifulSoup
import requests


def get_horo(sign):
    sign = sign.lower()
    url = "https://horo.mail.ru/prediction/" + sign +"/today/"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find("div", class_="article__item article__item_alignment_left article__item_html")
    result = quotes.text

    return str(result)
