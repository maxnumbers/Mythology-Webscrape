from glob import glob
import json
import requests
import pandas as pd
from tools.webscrapetools import get_soup, split_noblanks
from bs4 import BeautifulSoup

url = "https://godchecker.com"
soup = get_soup(url)
myth = []

### Page 1: Homepage
region_soup = soup.find("div", id="pantheon-list")
regions = region_soup.find_all("div", class_="pullout-panel")

# iterate through [1:-1] due to unneeded boxes
for x, region in enumerate(regions[1:-1]):
    region_name = region.find("h2").text
    pantheons = region.find_all("li")

    for y, pantheon in enumerate(pantheons):
        pantheon_href = pantheon.find("a")["href"]
        pantheon_name = split_noblanks(pantheon_href, "/")[-1]
        pantheon_soup = get_soup(pantheon_href)
        print(f"Groups:{x+1}/{len(regions)-2}, Pantheons:{y+1}/{len(pantheons)}")

        ### [Page2]Pantheon's Page:
        try:
            """
                <div class="pullout-panel topgodsbox floatable">
                    <h1>The most popular Greek gods</h1>
                    <ul>
                        <li> <a href="https://www.godchecker.com/greek-mythology/PHOBETOR/">1st: <span class="god-name"> Phobetor</span></a></li>
                        <li> <a href="https://www.godchecker.com/greek-mythology/APOLLO/">2nd: <span class="god-name"> Apollo</span></a></li>
                        <li> <a href="https://www.godchecker.com/greek-mythology/HERMES/">3rd: <span class="god-name"> Hermes</span></a></li>
                        <li> <a href="https://www.godchecker.com/greek-mythology/ZEUS/">4th: <span class="god-name"> Zeus</span></a></li>
                        <li> <a href="https://www.godchecker.com/greek-mythology/TITHONUS/">5th: <span class="god-name"> Tithonus</span></a></li>
                        <li> <a href="https://www.godchecker.com/greek-mythology/APHRODITE/">6th: <span class="god-name"> Aphrodite</span></a></li>
                        <li> <a href="https://www.godchecker.com/greek-mythology/ARTEMIS/">7th: <span class="god-name"> Artemis</span></a></li>
                        <li> <a href="https://www.godchecker.com/greek-mythology/HADES/">8th: <span class="god-name"> Hades</span></a></li>
                        <li> <a href="https://www.godchecker.com/greek-mythology/ATLAS/">9th: <span class="god-name"> Atlas</span></a></li>
                        <li> <a href="https://www.godchecker.com/greek-mythology/CHAOS/">10th: <span class="god-name"> Chaos</span></a></li>
                    </ul>
                    <p class="txt-notes">
                    Godchecker's Holy Hit Parade of <a href="https://www.godchecker.com/top-gods/">popular Gods</a> is powered by GodRank™ Technology.
                    </p>
                    </div>
                """

            gods = pantheon_soup.find("div", class_="topgodsbox").find_all("li")
        except:
            """
                <div class="search-result clickable-panel">
                    <a href="https://www.godchecker.com/brittonic-mythology/ANDRASTE/">
                        <h1> Andraste</h1>
                    <p><span class="boxinho brittonic"></span>Brittonic Goddess</p>
                    <div class="more icon-go"></div>
                    </a></div>    
                """
            gods = pantheon_soup.find_all(
                "div", class_="search-result clickable-panel"
            )[:-1]
        finally:
            for god in gods:
                god_href = god.find("a")["href"]
                god_name = split_noblanks(god_href, "/")[-1]
                god_soup = get_soup(god_href)
                god = {}

                ### Page 3: God Page
                god_page = god_soup.find("div", "text-bubble", "p")
                related_gods = god_page.find_all(class_="god-name")
                related_gods_links = god_page.find_all("a", class_="god-name")
                god_table = god_page.find("div", class_="pullout-panel").find_all("p")
                god_summary = god_soup.find("div", class_="text-bubble").find_all("p")

                # parse god summary paragraphs
                god_summary_text = ""
                if len(god_summary) > 2:
                    god_summary = god_summary[:2]
                for paragraph in god_summary:
                    god_summary_text = god_summary_text + paragraph.text

                # parse god relationships
                related_god_list = []
                for related_god in related_gods:
                    if related_god.text not in related_god_list:
                        related_god_list.append(related_god.text)

                related_god_link_list = []
                for link in related_gods_links:
                    related_god_link_list.append(link["href"])

                # parse god information table
                for section in god_table:
                    info_fields = split_noblanks(section.text, "\n")
                    for info in info_fields:
                        field_name = info.split(":")[0].replace(" ", "")
                        field_str = info.split(":")[1].replace(" ", "")
                        god[f"{field_name}"] = field_str

                # assigned parsed info to dict
                god["Link"] = god_href
                god["Summary"] = god_summary_text
                god["Related_Gods"] = related_god_list
                god["Related_Gods_Links"] = related_god_link_list
                god["Region_Name"] = region_name.replace("The Gods of", "")
                god["Pantheon_Name"] = pantheon_name
                myth.append(god)
                # god[""] =
                # god[""] =
                # god[""] =
                # god[""] =
                # god[""] =
                # god[""] =


df = pd.DataFrame.from_dict(myth)
# df_json = pd.DataFrame.to_json(df)
df.to_excel("godchecker/mythology.xlsx", sheet_name="gods")
print("Process Complete! :D")

# with open("godchecker/mythology_json.txt", "w") as outfile:
#     json.dump(myth, outfile)
