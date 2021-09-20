import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv
import re
import numpy as np

from metadata import *

def change_transfer_url(transfers_url, season, summer_winter='both'):
    if isinstance(season, int):
        season = str(season)
    if "?saison_id" in transfers_url:
        pass
    if summer_winter=='summer':
        transfers_url = transfers_url + "/plus/?saison_id=" + season + "&s_w=s&leihe=1&intern=0&intern=1"
    if summer_winter=='winter':
        transfers_url = transfers_url + "/plus/?saison_id=" + season + "&s_w=w&leihe=1&intern=0&intern=1"
    if summer_winter=='both':
        transfers_url = transfers_url + "/plus/?saison_id=" + season + "&s_w=&leihe=1&intern=0&intern=1"

    return transfers_url

def clean_values(series):
    series = (series.str.replace('€', '')
              .replace('Th.', '000', regex=True)
              .replace('m', '0000', regex=True)
              .replace('\.', '', regex=True)
              .replace('-', '0')
              .replace('?', '0'))
    return series

def get_league_transfers_summary(transfer_url, season, summer_or_winter='both'):

    transfer_url = change_transfer_url(transfer_url, season, summer_or_winter)
    
    # Get transfer website
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.58 Safari/537.36'}
    r = requests.get(transfer_url, headers=header)
    soup = bs(r.content, 'html.parser')
    competition_id = transfer_url.split("wettbewerb/")[1].split("/plus")[0]

    counter = 0
    box_select = 0

    for box_index in range(len(soup.select('div.box'))):
        box = soup.select('div.box')[box_index]
        try:
            if "Transfer record" in box.select('h2')[0].get_text():
                counter += 1
                if counter == 1:
                    box_select = box_index
        except:
            pass

    transfer_box = soup.select('div.box')[box_select]

    values_raw = []

    for item in transfer_box.select('div.text')[0].select('span'):
        values_raw.append(item.get_text())

    for item in transfer_box.select('div.text')[1].select('span'):
        values_raw.append(item.get_text())

    for item in transfer_box.select('div.text')[2].select('span'):
        values_raw.append(item.get_text())

    values_raw = [int(f.replace('€','').replace(',','')) for f in values_raw]

    transfer_overview = {}
    transfer_overview['total_income'] = values_raw[0]
    transfer_overview['avg_income_per_club'] = values_raw[1]
    transfer_overview['avg_income_per_player'] = values_raw[2]
    transfer_overview['total_spend'] = values_raw[3]
    transfer_overview['avg_spend_per_club'] = values_raw[4]
    transfer_overview['avg_spend_per_player'] = values_raw[5]
    transfer_overview['total_balance'] = values_raw[6]
    transfer_overview['avg_balance_per_club'] = values_raw[7]
    transfer_overview['avg_balance_per_player'] = values_raw[8]
    transfer_overview['competition'] = soup.select('h1')[0].get_text().strip().lower()
    transfer_overview['competition_id'] = competition_id
    transfer_overview['season'] = soup.select('div.table-header')[0].get_text().replace("Transfers ","").strip()
    transfer_overview['country'] = soup.select('div.flagge')[0].select('img')[0]['alt'].lower()
    
    return transfer_overview

def get_league_transfers(url, season, summer_or_winter):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.58 Safari/537.36'}
    transfer_url = change_transfer_url(url, season, summer_or_winter)
    
    # Get transfer website
    r = requests.get(transfer_url, headers=header)

    soup = bs(r.content, 'html.parser')
    # Get teams
    team_headers = soup.find_all('div', {'class': 'table-header'})
    teams = [box.getText() for box in team_headers[1:]]
    # ------- GET DIFFERENT ELEMENTS ------- #
    # AGE
    age_elements = soup.find_all(class_='zentriert alter-transfer-cell')
    ages = []
    for age in age_elements:
        ages.append(age.text)
    # NAME
    name_elements = soup.find_all('span', {'class': 'hide-for-small'})
    names = []
    for name in name_elements:
        names.append(name.text)
    # POSITION
    position_elements = soup.find_all(class_='pos-transfer-cell')
    positions = []
    for position in position_elements:
        positions.append(position.text)
    # NATIONALITY
    elements = soup.find_all(class_='zentriert nat-transfer-cell')
    nation_elements = []
    for element in elements:
        img_element = element.find('img', {'class': 'flaggenrahmen'}, {'title':True})
        if img_element != None:
            nation_elements.append(img_element['title'])
        if img_element == None:
            nation_elements.append('Nation')
    # MARKET VALUE (mv)
    mv_elements = soup.find_all(class_='rechts mw-transfer-cell')
    market_values = []
    for mv in mv_elements:
        market_values.append(mv.text)
    # LEFT / JOINED CLUB AND COUNTRY
    #club
    joined_elements = soup.find_all(class_='no-border-links verein-flagge-transfer-cell')
    joined_clubs = []
    for element in joined_elements:
        club_element = element.find(class_='vereinprofil_tooltip')
        if club_element != None:
            joined_clubs.append(club_element.text)
        if club_element == None:
            joined_clubs.append('No club')
    #country
    joined_country = []
    for element in joined_elements:
        country = element.find(class_='flaggenrahmen')
        if country != None:
            joined_country.append(country['title'])
        if country == None:
            joined_country.append('No country')
    # TRANSFER FEE
    fee_elements = soup.find_all(class_='rechts')
    transfer_fees = []
    for fee in fee_elements:
        transfer_fees.append(fee.text)
    # both market and transfer fee is extracted, we only need transfer fee
    transfer_fees = transfer_fees[1::2]

    # Create list of in-out transfer
    s = ['in', 'out']
    in_out_list = []
    j = 1
    for age in ages:
        if age=='Age':
            in_out_list.append('Age')
            j = ~j
        else:
            in_out_list.append(s[j])
    # Make names and joined from lists same length
    for idx, position in enumerate(positions):
        if position=='Position':
            names.insert(idx, 'Name')
            joined_clubs.insert(idx, 'Joined')
            joined_country.insert(idx, 'Joined')
    # length 320 (ages, position, nations, market value, transfer fee)
    # length 296 (names, joined club, joined country)
    teams_long_list = ages
    # Get indices for where to insert team names
    age_idx = []
    for idx, age in enumerate(ages):
        if age=='Age':
            age_idx.append(idx)
    # Replace "Age" with team at every other index
    for idx, (team, team_idx) in enumerate(zip(teams, age_idx[::2])):
        teams_long_list[team_idx] = team
    # Replace non team names with NaN
    teams_long_list = [None if team not in teams else team for team in teams_long_list]
    
    # ----- CREATE DATAFRAME ----- #
    df = pd.DataFrame({'Team': teams_long_list,
                       'Name': names,
                       'Age': ages,
                       'Position': positions,
                       'Nation': nation_elements,
                       'Market Value': market_values,
                       'Left / Joined Club': joined_clubs,
                       'Left / Joined Country': joined_country,
                       'Transfer Fee': transfer_fees,
                       'In or Out': in_out_list})
    # forward fill clubs
    df['Team'].ffill(inplace=True)
    # remove rows that are headers
    df = df[df['Name']!='Name']
    # clean market value and transfer fee
    df['Market Value'] = clean_values(df['Market Value'])
    df['Transfer Fee'] = clean_values(df['Transfer Fee'])
    df = df.reset_index(drop=True)
    
    return df

def clean_transfer_df(df):
    # Compute bought type
    df['bought_type'] = df['Transfer Fee']
    for idx, row in df.iterrows():
        if row['bought_type'].startswith('End'):
            df.loc[idx, 'bought_type'] = None
        if row['bought_type'].startswith('Loan'):
            df.loc[idx, 'bought_type'] = 'loan transfer'
        if row['bought_type'].isdigit():
            df.loc[idx, 'bought_type'] = 'bought'
        if row['Left / Joined Club'] in academy_teams:
            df.loc[idx, 'bought_type'] = 'academy'

    # Compute bought area
    df['bought_area'] = df['Transfer Fee']
    for idx, row in df.iterrows():
        if row['Left / Joined Country'] == 'Denmark':
            df.loc[idx, 'bought_area'] = 'denmark'
        if row['Left / Joined Country'] in scandinavian:
            df.loc[idx, 'bought_area'] = 'scandinavia'
        if row['Left / Joined Country'] in east_europe:
            df.loc[idx, 'bought_area'] = 'east_europe'
        if row['Left / Joined Country'] in europe:
            df.loc[idx, 'bought_area'] = 'europe'
        if row['Left / Joined Country'] in others:
            df.loc[idx, 'bought_area'] = 'other'
    
    return df

def clean_transfer_fees(df):
    # clean transfer fees
    df['Transfer Fee'].replace('free transfer', '0', inplace=True)
    # clean loan transfers
    df['loan_transfer'] = np.where((df['Transfer Fee'] == 'loan transfer')
                                            | (df['Transfer Fee'].str.startswith('End'))
                                            | (df['Transfer Fee'].str.startswith('Loan')), True, False)
    df['Transfer Fee'].replace('loan transfer', '0', inplace=True)
    df['Transfer Fee'].replace('(^.*End.*$)', '0', inplace=True, regex=True)
    df['Transfer Fee'].replace('Loan fee:', '', inplace=True, regex=True)
    df['Age'].replace('-', None, inplace=True)
    #convert transfer fees to numeric
    df['Transfer Fee'] = df['Transfer Fee'].astype(int) / 1000000
    df['Age'] = df['Age'].astype(int)

    return df

if __name__ == '__main__':
    url = 'https://www.transfermarkt.com/superligaen/transfers/wettbewerb/DK1/plus/'

    # Get all leagues
    seasons = ['2010', '2011', '2012', '2013', '2014', '2015',
               '2016', '2017', '2018', '2019', '2020', '2021']
    all_league_transfers = []
    for season in seasons:
        legaue_transfers = get_league_transfers(url, season, summer_or_winter='summer')
        # add season
        legaue_transfers['season'] = season
        all_league_transfers.append(legaue_transfers)
    
    all_league_transfers = pd.concat(all_league_transfers).reset_index(drop=True)
    all_league_transfers.to_csv(f'data/all_league_transfers_{seasons[0]}_{seasons[-1]}.csv')
