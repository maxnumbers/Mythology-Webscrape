myth = open("godchecker/mythology_dict.text", "r")

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
