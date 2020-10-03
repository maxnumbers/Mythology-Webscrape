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


class soup_strainer:
    def __init__(
        self, soup, find_params, findall_params,
    ):
        """[summary]

        Args:
            soup ([type]): [description]
            find_params ([type]): [description]
            findall_params (list, optional): [description]. Defaults to [].
        """
        self.found = find_filter(soup, find_params)

        if self.found and findall_params:

            self.found_all = find_all_filter(soup, findall_params)
            self.len = len(self.found_all)

    def find_filter(self, soup, find_params):
        return soup.find(self.find(find_params))

    def find_all_filter(self, soup, findall_params):
        return soup.find_all(self.find_all(findall_params))

