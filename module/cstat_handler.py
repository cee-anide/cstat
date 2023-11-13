from typing import List
from pathlib import Path

import pandas as pd

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

import module.playercstat as playercstat

URL_SORT_POINTS = "https://cstat.snowy.gg"
URL_SORT_TIME = "https://cstat.snowy.gg/?sort=totaltime"
URL_SORT_TD = "https://cstat.snowy.gg/?sort=td_count"


def scrape_and_export(pages: int, outfile_name: Path, sort: str):
    raw_cstat_entries = scrape_text(pages, sort)
    print("Exporting", pages, "page(s) of cstat data...")
    df = raw_extract_to_dataframe(raw_cstat_entries)
    df.to_excel(outfile_name, index=False)


def scrape_text(pages: int, sort: int) -> List[List[str]]:
    options = Options()
    options.binary = FirefoxBinary("/snap/bin/firefox")
    driver = webdriver.Firefox(options=options)

    wait = WebDriverWait(driver, 10.0, 0.5)

    if sort == "time":
        url = URL_SORT_TIME
    elif sort == "topdefender":
        url = URL_SORT_POINTS
    else:
        url = URL_SORT_POINTS

    driver.get(url)

    cstat: List[List[str]] = []
    #INFO: PAGE ACTION BEGIN
    for i in range(0, pages):
        # Collect all cstat entries on page, should be 15, also remove the first header row
        clickable_table_rows: List[WebElement] = wait.until(lambda d: driver.find_elements(By.CSS_SELECTOR, "tr"))
        clickable_table_rows.pop(0)

        for row in clickable_table_rows:
            row.find_element(By.CSS_SELECTOR, "td").click()

        tables = driver.find_elements(By.CLASS_NAME, "table-opener")
        
        table_idx = 0
        for table in tables:
            entry: List[str] = ["Points:" + clickable_table_rows[table_idx].text.splitlines()[2]]
            for e in table.find_elements(By.CSS_SELECTOR, "tr"):
                entry.append(e.text)

            table_idx += 1
            cstat.append(entry)

        
        if i < pages - 1:
            next_page_button: WebElement = wait.until(lambda d: driver.find_element(By.LINK_TEXT, ">"))
            next_page_button.click()

    #INFO: PAGE ACTION ENDS
    driver.quit()
    return cstat


def raw_extract_to_dataframe(entries: List[List[str]]) -> pd.DataFrame:
    column_names = {
        "name": "Player",
        "points": "Points", 
        "total_time": "Total Time (days)", 
        "human_time": "Human Time (days)", 
        "zombie_time": "Zombie Time (days)", 
        "zombie_kills": "Zombies Killed",
        "zombie_hs": "Zombies Killed (HS)",
        "infected": "Infected",
        "items_picked": "Items picked up",
        "boss_killed": "Boss Killed",
        "leader_count": "Leader Count",
        "td_count": "TopDefender Count"
    }
    cstat_objs = []
    for ent in entries:
        obj = playercstat.PlayerCstat(ent)
        cstat_objs.append(obj)

    df = pd.DataFrame(cstat_objs)
    df.rename(columns=column_names, inplace=True)
    return df


def find_cstat_diff(old_data_path: Path, new_data_path: Path, path_output: Path):

    # File paths verified in main
    old_data = pd.read_excel(old_data_path)
    new_data = pd.read_excel(new_data_path)

    compared_stats = pd.DataFrame(
        columns=["Player", "Total Time Diff", "Human Time Diff", "cStat/d Total", "cStat/d Human"])
    
    old_len = len(old_data)
    new_len = len(new_data)
    data_length = min(old_len, new_len)
    
    compared_stats["Player"] = new_data["Player"]
    if len(compared_stats) > data_length:
        compared_stats = compared_stats.iloc[0:data_length]

    to_drop = []
    for i in range(0, data_length):
        player = compared_stats.loc[i, "Player"]
        old_entry = old_data.loc[old_data["Player"] == player].reset_index(drop=True)
        new_entry = new_data.loc[new_data["Player"] == player].reset_index(drop=True)

        if old_entry.empty or new_entry.empty:
            to_drop.append(player)
            continue

        comp_total_diff = new_entry.loc[0, "Total Time (days)"] - old_entry.loc[0, "Total Time (days)"]
        comp_human_diff = new_entry.loc[0, "Human Time (days)"] - old_entry.loc[0, "Human Time (days)"]
        comp_points = new_entry.loc[0, "Points"] - old_entry.loc[0, "Points"]

        compared_stats.loc[i, "Total Time Diff"] = comp_total_diff
        compared_stats.loc[i, "Human Time Diff"] = comp_human_diff

        if comp_total_diff == 0 or comp_human_diff == 0 or comp_points == 0:
            compared_stats.loc[i, "cStat/d Total"] = 0
            compared_stats.loc[i, "cStat/d Human"] = 0
        else:
            compared_stats.loc[i, "cStat/d Total"] = comp_points / comp_total_diff
            compared_stats.loc[i, "cStat/d Human"] = comp_points / comp_human_diff

    for name in to_drop:
        compared_stats.drop(compared_stats[compared_stats["Player"] == name].index, inplace=True)

    compared_stats.to_excel(path_output, index=False)
