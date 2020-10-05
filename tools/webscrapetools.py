import json
import requests
from bs4 import BeautifulSoup


def get_soup(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "html.parser")
    return soup


def split_noblanks(text=str, split_by=str):
    split_arr = text.split(split_by)
    while "" in split_arr:
        split_arr.remove("")
    return split_arr


class soupstrainer:
    def __init__(self, find_soup, findall_soup, *kwargs):
        """[summary]

        Args:
            soup ([type]): [description]
            find_params ([type]): [description]
            findall_params (list, optional): [description]. Defaults to [].
        """

        self.found = self.find_filter(find_soup)

        if self.found and findall_params:

            self.found_all = self.find_all_filter(soup, findall_params)
            self.len = len(self.found_all)

    def find_filter(self, soup, find_params):
        return soup.find(eval(find_params))

    def find_all_filter(self, soup, findall_params):
        return soup.find_all(findall_params)

