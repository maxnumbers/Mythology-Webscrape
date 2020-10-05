from glob import glob
import json
import requests
from tools.webscrapetools import get_soup, split_noblanks
from bs4 import BeautifulSoup

url = "https://godchecker.com"
soup = get_soup(url)
myth = {}

### Page 1: Homepage
region_soup = soup.find("div", id="pantheon-list")
regions = region_soup.find_all("div", class_="pullout-panel")

for x, region in enumerate(regions[1:-1]):
    region_name = region.find("h2").text
    pantheons = region.find_all("h2", "li")
    myth[f"{region_name}"] = {}

    for y, pantheon in enumerate(pantheons):
        pantheon_href = pantheon.find("a")["href"]
        pantheon_name = split_noblanks(pantheon_href.text, "/")[-1]
        pantheon_soup = get_soup(pantheon_href)
        print(f"Groups:{x+1}/{len(regions)-2}, Pantheons:{y+1}/{pantheons.len}")
        myth[f"{region_name}"][f"{pantheon_name}"] = {}

        ### [Page2]Pantheon's Page:
        try:
            gods = pantheon_soup.find(
                "div", class_="pullout-panel topgodsbox floatable"
            ).find_all("a")
        except:
            gods = pantheon_soup.find("div", class_="text-bubble").find_all("a")
        finally:
            for god in gods:
                god_href = god.find("a")["href"]
                god_name = split_noblanks(god_href.text, "/")[-1]
                god_soup = get_soup(god_href)
                myth[f"{region_name}"][f"{pantheon_name}"][f"{god_name}"] = {}

                ### Page 3: God Page
                god_page = god_soup.find("div", "text-bubble", "p")
                related_gods = god_page.text
                related_gods_links = god_page.find_all("a")
                god_table = god_soup.find(
                    "div", class_="pullout-panel vitalsbox finnish"
                ).find_all("p")

                for section in god_table:

                    info_fields = split_noblanks(section)
                    for info in info_fields:
                        field_name = info.split(":")[0]
                        field_str = info.split(":")[1]

                    myth[f"{region_name}"][f"{pantheon_name}"][f"{god_name}"][
                        f"{field_name}"
                    ] = field_str
                    myth[f"{region_name}"][f"{pantheon_name}"][f"{god_name}"][
                        "Link"
                    ] = god_href


flat_json = []
for regs in myth.keys():
    for pans in myth[f"{regs}"].keys():
        for gs in myth[f"{regs}"][f"{pans}"].keys():
            myth[f"{regs}"][f"{pans}"][f"{gs}"]["Region_Name"] = regs
            myth[f"{regs}"][f"{pans}"][f"{gs}"]["Pantheon_Name"] = pans

            rltn_list = []
            rltn_link_list = []
            for rltn in related_gods:
                rltn_list.append(rltn.text)
                if rltn.find("span")["href"]:
                    rltn_link_list.append(rltn.find("span")["href"])

            myth[f"{regs}"][f"{pans}"][f"{gs}"]["Related_Gods"] = rltn_list
            myth[f"{regs}"][f"{pans}"][f"{gs}"]["Related_Gods_Links"] = rltn_link_list

            flat_json.append(myth[f"{regs}"][f"{pans}"][f"{gs}"])

with open("godchecker/mythology_flattened.json", "w") as f:
    json.dump(flat_json, f)

