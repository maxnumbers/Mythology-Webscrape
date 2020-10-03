import glob
import json
import requests
from webscrapetools import soupstrainer, get_soup, split_noblanks
from bs4 import BeautifulSoup

url = "https://godchecker.com"
soup = get_soup(url)
myth = {}

### Page 1: Homepage
regions = soupstrainer(
    soup, str("div", id="pantheon-list"), str("div", class_="pullout-panel")
)
regions_len = len(regions)

for x, region in enumerate(regions.found_all[1:-1]):
    pantheons = soupstrainer(region, "h2", "li")
    region_name = pantheons.found.text
    myth[f"{region_name}"] = {}

    for y, pantheon in enumerate(pantheons.found_all):
        pantheon_href = pantheon.find("a")["href"]
        pantheon_name = split_noblanks(pantheon_href.text, "/")[-1]
        pantheon_soup = get_soup(pantheon_href)
        print(f"Groups:{x+1}/{regions.len-2}, Pantheons:{y+1}/{pantheons.len}")
        myth[f"{region_name}"][f"{pantheon_name}"] = {}

        ### [Page2]Pantheon's Page:
        try:
            gods = soupstrainer(
                pantheon_soup,
                str("div", class_="pullout-panel topgodsbox floatable"),
                "a",
            )
        except:
            gods = soupstrainer(pantheon_soup, str("div", class_="text-bubble"), "a")
        finally:
            for god in gods.found_all:
                god_href = god.find("a")["href"]
                god_name = split_noblanks(god_href.text, "/")[-1]
                god_soup = get_soup(god_href)
                myth[f"{region_name}"][f"{pantheon_name}"][f"{god_name}"] = {}

                ### Page 3: God Page
                god_page = soupstrainer(
                    god_soup, str("div", class_="text-bubble" > "p"), "a"
                )
                related_gods = god_page.found.text
                related_gods_links = god_page.found_all
                god_table = soupstrainer(
                    god_soup, str("div", class_="pullout-panel vitalsbox finnish" > "p")
                )

                for section in god_table.find_all:

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

            # necessary because there's no way to get text from "find_all" w/o iterating
            rltn_list = []
            rltn_link_list = []
            for rltn in god_relations:
                rltn_list.append(rltn.text)
                if rltn.find("span")["href"]:
                    rltn_link_list.append(rltn.find("span")["href"])

            myth[f"{regs}"][f"{pans}"][f"{gs}"]["Related_Gods"] = rltn_list
            myth[f"{regs}"][f"{pans}"][f"{gs}"]["Related_Gods_Links"] = rltn_link_list

            flat_json.append(myth[f"{regs}"][f"{pans}"][f"{gs}"])

with open("mythology_flattened.json", "w") as f:
    json.dump(flat_json, f)

