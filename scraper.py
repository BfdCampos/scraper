import requests
from bs4 import BeautifulSoup
import csv
import time

# Latest player ID 2509
print("This script will scrape data from jalgpall.ee for all players with ID between the starting player ID + 500.")

start_id = input("Enter the starting player ID: ")

with open('player_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Player ID", "Name", "Total minutes played", "Birthday", "Team", "Nationality", "Total games", "Season"])

    for player_id in range(int(start_id), int(start_id) + 500):
        print(f"Looking for player with ID: {player_id}")
        url = f"https://jalgpall.ee/voistlused/player/{player_id}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            season = soup.find('select', {'name': 'season'}).find('option', selected=True).text
            if season not in ['2021', '2022', '2023']:
                print(f"Skipping player with ID: {player_id} due to season {season}")
                continue

            name = soup.find('p', {'class': 'player'}).text
            total_minutes_played = soup.find('span', {'id': 'totalminutes'}).text
            birthday = soup.find('p', text='Sünniaeg').find_next_sibling('p').text
            team = soup.find('p', text='Klubi').find_next_sibling('p').text
            nationality = soup.find('p', text='Kodakondsus').find_next_sibling('p').text
            total_games = soup.find('span', {'id': 'totalgames'}).text

            writer.writerow([player_id, name, total_minutes_played, birthday, team, nationality, total_games, season])
            print(f"Data successfully written for player with ID: {player_id} in season {season}")
        except AttributeError:
            # This player_id does not exist or some information is missing, skip to next player_id
            print(f"No data found for player with ID: {player_id}")
            continue
        time.sleep(0.01)

