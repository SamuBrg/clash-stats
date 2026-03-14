import requests
import dbcr
import json
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
dbcr.setup_db()


player_tag = "%23YGQG0J"

api_key = os.getenv("SUPERCELL_API_KEY")

url = f"https://api.clashroyale.com/v1/players/{player_tag}/battlelog"
url1 = f"https://api.clashroyale.com/v1/cards"

headers = {
    'Authorization': f'Bearer {api_key}'
}

response = requests.get(url, headers=headers)
data = response.json()

def print_json_battlelog():
    with open("battlelog.json", "w") as datei0:
        json.dump(data, datei0, indent=4) 


def update_card_information():
    with open("all_cards.json", "r") as datei1:
        json_data = json.load(datei1)
        card_information = {}
        for karte in json_data["items"]:
            abc = karte["name"], karte["id"], karte["iconUrls"]["medium"]
            card_information[karte["id"]] = [karte["name"], karte["iconUrls"]["medium"]]
    return card_information


def update_games():
    for match in data:
        if match["type"] == "pathOfLegend":
            a = match["battleTime"]
            b = match["opponent"][0]["name"]
            c = []
            d = []
            for n in range(8):
                c.append(match["opponent"][0]["cards"][n]["id"])
            for r in range(8):
                d.append(match["team"][0]["cards"][r]["id"])
            team_crowns, enemy_crowns = match["team"][0]["crowns"], match["opponent"][0]["crowns"]
            if team_crowns > enemy_crowns:
                e = 1
            elif team_crowns < enemy_crowns:
                e = -1
            else:
                e = 0
            dbcr.update_game(a, b, c, d, e)
    return "games updated successfully"
    

@st.cache_data
def show_stats():
    card_table_1 = dbcr.enemy_card_stats()
    card_table_2 = dbcr.my_card_stats()
    enemy_card_list = []
    my_card_list = []
    for liste in card_table_1:
        card_list = cards[liste[0]]
        enemy_card_list.append([card_list[0], liste[2], liste[3], liste[1], card_list[1]])

    for liste in card_table_2:
        card_list = cards[liste[0]]
        my_card_list.append([card_list[0], liste[2], liste[3], liste[1], card_list[1]])

    return enemy_card_list, my_card_list


def winrate_percent(input_wins, input_draws, input_amount_games):
    result = (input_wins + 0.5 * input_draws)/input_amount_games
    return (f"{result*100:.2f} %")

print_json_battlelog()
cards = update_card_information()


update_games()
show_stats()


