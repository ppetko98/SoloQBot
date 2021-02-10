import requests
import pandas as pd
import json
import time
import imgkit

# api requests limits:
# 20 requests every 1 seconds(s)
# 100 requests every 2 minutes(s)

API_KEY = 'RGAPI-3136be7b-99aa-44e8-95fa-5bfa50783cc2'


SUMMONERS_LIST = [('Amemo', 'Rodrigo'), ('TristanaBacana', 'Adrian'), ('Sazonadör', 'Santiago'),
                 ('kSalsaKiereChico', 'Petko'), ('Escapatraj0', 'Manuel'), ('Jäx Teller', 'Shalo'),
                 ('Chiquistruquis', 'Mario'), ('I äm not Fäker', 'Xichen'), ('CalvusDumbledore', 'Juancar')]


def get_account(summoner):
    account_url = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'.format(
        summoner.replace(' ', '%20'), API_KEY)
    response = requests.get(account_url)  # devuelve summ id, acc id, puuid
    return response


def get_stats(summoner):
    response = get_account(summoner)
    id = response.json()['id']  # summoner id
    # print(response.json()['accountId'])
    # print(id)
    summoner_name = summoner
    stats_url = 'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{}?api_key={}'.format(id, API_KEY)
    acc_stats = requests.get(stats_url).json()
    try:
        summoner_name = acc_stats[0]['summonerName']
        acc_stats_cleaned = [
            {'Name': i['summonerName'], 'Division': i['tier'], 'Rango': i['rank'], 'PLs': i['leaguePoints'],
             'totalMatches': int(i['wins']) + int(i['losses']), 'wins': i['wins'], 'losses': i['losses']} for i in
            acc_stats if i['queueType'] == 'RANKED_SOLO_5x5'][0]
    except IndexError:
        return {'Summoner': summoner_name, 'Division': 'UNRANKED', 'Rango': '-', 'PLs': 0, 'totalMatches': -1, 'wins': 0,
                'losses': 0}
    return acc_stats_cleaned


def get_last_matches(acc_id):
    response = requests.get(
        'https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?queue=420&season=13&api_key={}'.format(
            acc_id, API_KEY))
    if response.status_code == 200:
        match_list = response.json()['matches'][:3]
        return match_list
    else:
        return None


def get_table():
    data_list = []
    for i in SUMMONERS_LIST:
        data = get_stats(i[0])
        if data:
            data['Alias'] = i[1]
            data_list.append(data)

    df = pd.DataFrame(data=data_list)
    df["Division"] = pd.Categorical(df["Division"],
                                    categories=["CHALLENGER", "GRANDMASTER", "MASTER", "DIAMOND", "PLATINUM", "GOLD",
                                                "SILVER", "BRONZE", "IRON", "UNRANKED"])
    df["Win rate %"] = round(df['wins'] / df['totalMatches'] * 100, 2)
    df = df.reindex(columns=["Alias", "Summoner", "Division", "Rango", "PLs", "totalMatches", "wins", "losses", "Win rate %"])
    table = df.sort_values(by=['Division', 'Rango', 'PLs'], ascending=[True, True, False]).reset_index(drop=True)
    table.index += 1
    pd.set_option('display.max_rows', None, 'display.max_columns', None)
    return table


def generate_img_from_table(table):
    css = """
        <style type=\"text/css\">
        table {
        color: #333;
        font-family: Helvetica, Arial, sans-serif;
        width: 640px;
        border-collapse:
        collapse; 
        border-spacing: 0;
        }td, th {
        border: 1px solid transparent; /* No more visible border */
        height: 30px;
        }th {
        background: #DFDFDF; /* Darken header a bit */
        font-weight: bold;
        }td {
        background: #FAFAFA;
        text-align: center;
        }table tr:nth-child(odd) td{
        background-color: white;
        }
        </style>
        """
    filename = "leaderboard.html"
    with open(filename, 'a') as fp:
        fp.write(css)
        fp.write(table.to_html())
    imgkitoptions = {"format": "png"}
    imgkit.from_file(filename, 'leaderboard', options=imgkitoptions)


def generate_png():
    imgkitoptions = {"format": "png"}
    imgkit.from_file('leaderboard.html', 'leaderboard', options=imgkitoptions)


def main():
    generate_png()
    # generate_img_from_table(get_table())


if __name__ == "__main__":
    main()
