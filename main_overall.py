#%%
import pandas as pd
import numpy as np
from collections import Counter

import matplotlib.pyplot as plt
import matplotlib as mpl
import plt_utils
import seaborn as sns
from highlight_text import fig_text

import scrape_transfermarkt as st
from metadata import *

# -------- PREPARE DATA FOR OVERALL SUMMARY -------- #
transfer_url = 'https://www.transfermarkt.com/superligaen/transfers/wettbewerb/DK1'
league_url = 'https://www.transfermarkt.com/superligaen/startseite/wettbewerb/DK1'

transfer_summaries = dict()
for season in seasons_str:
    transfer_summary = st.get_league_transfers_summary(transfer_url,
                                                       season=str(season),
                                                       summer_or_winter='summer')
    # Input number departues and arrivals per season
    transfer_summary['departues'] = int(transfer_summary['total_income']/transfer_summary['avg_income_per_player'])
    transfer_summary['arrivals'] = int(transfer_summary['total_spend']/transfer_summary['avg_spend_per_player'])
    transfer_summaries[season] = transfer_summary

# Get data from transfer summaries
departues = [values['departues'] for key, values in transfer_summaries.items()]
arrivals = [values['arrivals'] for key, values in transfer_summaries.items()]
total_spend = [round(values['total_spend']/1000000, 1) for key, values in transfer_summaries.items()]
total_income = [round(values['total_income']/1000000, 1) for key, values in transfer_summaries.items()]
avg_spend_per_club = [values['avg_spend_per_club'] for key, values in transfer_summaries.items()]
avg_spend_per_player = [values['avg_spend_per_player'] for key, values in transfer_summaries.items()]
avg_income_per_club = [values['avg_income_per_club'] for key, values in transfer_summaries.items()]
avg_income_per_player = [values['avg_income_per_player'] for key, values in transfer_summaries.items()]

# ----- READ AND PREPARE SCRAPED LEAGUE DATA ------ #
df_transfers = pd.read_csv('data/all_league_transfers_2010_2021.csv', index_col=0)

# Compute bought type and bought area
df_transfers = st.clean_transfer_df(df_transfers)

# Clean transfer fees
df_transfers = st.clean_transfer_fees(df_transfers)

# Separate in/out transfers
df_transfers_out = df_transfers[df_transfers['In or Out'] == 'out']
df_transfers_in = df_transfers[df_transfers['In or Out'] == 'in']

# Calculate average ages
average_age_in = pd.DataFrame(df_transfers_in.groupby('season')['Age'].mean()).reset_index()
average_age_out = pd.DataFrame(df_transfers_out.groupby('season')['Age'].mean()).reset_index()


# --------- PLOT TABLE OF HIGHEST TRANSFER --------- #
cols_out = ['Name', 'Team', 'Left / Joined Club', 'Transfer Fee', 'season']
cols_in = ['Name', 'Left / Joined Club', 'Team', 'Transfer Fee', 'season']
top_transfers_out = df_transfers_out.sort_values('Transfer Fee', ascending=False).head(10)[cols_out].reset_index(drop=True)
top_transfers_out['Transfer Fee'] = top_transfers_out['Transfer Fee'].apply(str) + '  mil. €'
top_transfers_in = df_transfers_in.sort_values('Transfer Fee', ascending=False).head(10)[cols_in].reset_index(drop=True)
top_transfers_in['Transfer Fee'] = top_transfers_in['Transfer Fee'].apply(str) + '  mil. €'

# PLOT TABLE
plt_utils.plot_table(top_transfers_out,
                     top_transfers_in,
                     save_name='top_transfers_2010_2021')


# --------- PLOT SCATTER PLOTS ----------- #
dataframes = [departues, arrivals,
              total_spend, total_income]
titles = ['Antal solgte spillere i Superligaen', 'Antal købte spillere i Superligaen',
          'Superliga klubberne har aldrig brugt flere penge', 'Modtaget transfersum er stegt markant de seneste 12 år']
subtitles = 'Transfers i sommervinduet | 3F Superligaen fra 2010 til 2021'
y_labels = ['Antal af udgående transfer', 'Antal af indgående transfer',
            'Transfersum (mil. €)', 'Transfersum (mil. €)',
            'Transfersum (mil. €)']
save_names = ['departues_1011_2122', 'arrivals_1011_2122',
              'total_spend_1011_2122', 'total_income_1011_2122']

# Plot scatters
for i in range(len(dataframes)):
    plt_utils.plot_scatter(seasons_str, dataframes[i],
                           title=titles[i],
                           subtitle=subtitles,
                           y_label=y_labels[i],
                           save_name=save_names[i])

# Plot avg age
plt_utils.plot_scatter(average_age_in['season'], round(average_age_in['Age'], 1),
                       title='Gennemsnitlig alder for indgående Superliga transfers',
                       subtitle='Transfers i sommervinduet | 3F Superligaen fra 2010 til 2021',
                       y_label='Alder',
                       save_name='avg_age_in_1011_2122')
plt_utils.plot_scatter(average_age_out['season'], round(average_age_out['Age'], 1),
                       title='Gennemsnitlig alder for udgående Superliga transfers',
                       subtitle='Transfers i sommervinduet | 3F Superligaen fra 2010 til 2021',
                       y_label='Alder',
                       save_name='avg_age_out_1011_2122')


# PLOT STACKED BAR CHART
# from raw value to percentage
values_type = df_transfers_in.groupby('season')['bought_type'].value_counts(normalize=True).mul(100)
values_type = values_type.unstack()

# plotting
plt_utils.plot_bar(values_type,
                   bar_colors_type, bar_title_type,
                   'Fordeling af indgående transfers i Superligaen',
                   'Transfers i sommervinduet | 3F Superligaen fra 2010 til 2021',
                   save_name='share_of_in_transfers_1011_2021')
# from raw value to percentage
values_area = df_transfers_out.groupby('season')['bought_area'].value_counts(normalize=True).mul(100)
values_area = values_area.unstack()

# plotting
plt_utils.plot_bar(values_area,
                   bar_colors_area, bar_title_area,
                   'I hvilke lande ender udgående Superliga transfers?',
                   'Transfers i sommervinduet | 3F Superligaen fra 2010 til 2021',
                   save_name='share_of_area_transfers_1011_2021')

# PLOT SWARM PLOT OF AVG AND MAX TRANSFERS
plt_utils.plot_dots(df_transfers_out,
                    'Hvordan har den <gennemsnitlige> og <maksimale> transfersum udviklet fra 2010 til 2021?',
                    'Alle udgående transfersummer i sommervinduet fra 2010 til 2021',
                    save_name='avg_max_transfersum_2010_2021')
