import json
import requests
from bs4 import BeautifulSoup


def get_soup(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "html.parser")
    return soup


def split_noblanks(text, split_by):
    split_arr = text.split(split_by)
    while "" in split_arr:
        split_arr.remove("")
    return split_arr

