import matplotlib as mpl
import matplotlib.pyplot as plt
from highlight_text import fig_text

from metadata import *
from collections import Counter
import numpy as np

mpl.rcParams['font.family'] = 'Alegreya Sans'

# ------- PLOT SCATTER ------- #
def plot_scatter(x, y, title, subtitle, y_label, save_name=None):
    fig, ax = plt.subplots(figsize=(12,10))

    # plot scatter points
    ax.scatter(x, y,
            s=1500, facecolor=blue,
            edgecolor=background_color, lw=8, zorder=8)
    ax.plot(x, y,
            zorder=0, color='w', lw=3)

    # annotate scatter points
    for i, txt in enumerate(y):
        ax.annotate(txt, (x[i], y[i]),
                    color='w', fontsize=18, fontweight='bold',
                    ha='center', va='center', zorder=10)

    # set background color etc.
    fig.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    # spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_color('w')
    ax.spines['left'].set_color('w')
    # ticks
    ax.tick_params(axis='both', which='major',
                labelsize=16, labelcolor='w', color='w')
    ax.tick_params(axis='both', which='major',
                labelsize=16, labelcolor='w', color='w')
    ax.set_xticks(x)
    # grid
    ax.grid(which='both', alpha=0.4, ls='--')

    # titles
    ax.set_ylabel(y_label,
                  color='w', fontsize=16, fontweight='bold')
    fig.text(s=title, x=0.12, y=0.94,
            ha='left', color='w', fontsize=28, fontweight='bold')
    fig.text(s=subtitle, x=0.12, y=0.9,
            ha='left', color='w', fontsize=18, fontweight='regular')
    
    # add signature
    fig.text(s='twitter.com/C_Roensholt',
             y=0.06, x=0.9, ha='right',
             color='w', fontsize=12, fontweight='regular')
    
    if save_name:
        plt.savefig(f'output/{save_name}.png', dpi=300)
        
def plot_bar(values, bar_colors, bar_titles, title, subtitle, save_name=None):
    fig, axes = plt.subplots(figsize=(14, 10),
                             ncols=len(values.columns), nrows=1,
                             sharey=True)
    fig.set_facecolor(background_color)
    for idx, (ax, col) in enumerate(zip(axes.flat, values.columns)):
        ax.set_facecolor(background_color)
        
        # plot bar
        ax.barh(values.index, values[col],
                color=bar_colors[idx])

        # modify spines
        for spine in ['top', 'bottom', 'right', 'left']:
            ax.spines[spine].set_visible(False)
        
        # modify ticks
        ax.tick_params(axis='both', which='major',
                    labelsize=16, labelcolor='w', color=background_color)
        ax.set_yticks(values.index)
        ax.set_xticks([])
        
        ax.set_xlim(0, values.max().max()+0.5)
        
        # annotate bars
        for i in ax.patches:
            if i.get_width() > 3:
                ax.text(1, i.get_y()+0.4, str(round(i.get_width(), 1))+'%',
                        fontsize=14, fontweight='bold',
                        color=background_color, va='center')
        # set titles
        ax.set_title(label=bar_titles[idx], x=0, y=0.97,
                    ha='left', fontsize=16, fontweight='bold', color='w')
        
    fig.text(s=title, x=0.5, y=0.96,
            ha='center', color='w', fontsize=32, fontweight='bold')
    fig.text(s=subtitle, x=0.5, y=0.92,
            ha='center', color='w', fontsize=18, fontweight='regular')
    # add signature
    fig.text(s='twitter.com/C_Roensholt',
            y=0.12, x=0.9, ha='right',
            color='w', fontsize=12, fontweight='regular')
    if save_name:
        plt.savefig(f'output/{save_name}.png', dpi=300)


def plot_dots(df, title, subtitle, save_name=None):        
    fig, axes = plt.subplots(figsize=(14,10),
                            nrows=int(len(seasons_int)/2), ncols=2)

    # set background color etc.
    fig.set_facecolor(background_color)
    for ax, season in zip(axes.flat, seasons_int):
        ax.set_facecolor(background_color)

        # modify spines and ticks
        for spine in ['top', 'left', 'right']:
            ax.spines[spine].set_visible(False)
        ax.spines['bottom'].set_color('w')
        ax.tick_params(axis='both', which='major',
                    labelsize=16, labelcolor='w', color='w')
        ax.tick_params(axis='both', which='major',
                    labelsize=16, labelcolor='w', color='w')

        # prepare data
        data = df[(df['Transfer Fee'] != 0)
                  &(df['season'] == season)]['Transfer Fee']
        z = Counter(data)
        values, counts = np.unique(data, return_counts=True)
        for key, value in z.items():
            X = [key] * value
            Y = [item + 1 for item in range(value)]
            ax.scatter(X, Y, facecolor=blue, edgecolor='w', s=50, lw=0.5)
        # plot histogram
        #x.hist(values, bins=len(data.unique()), color='#015a9a')
        ax.set_xlim(0, df['Transfer Fee'].max()+0.5)
        ax.set_ylim(0.5, 4)
        #ax.set_xticks(range(16))
        
        # plot mean and max lines
        ax.annotate(text=f'{round(values.mean(), 1)} mil. €',
                    ha='center', size=10,
                    xy=(values.mean(), 2),
                    xytext=(values.mean(), 4),
                    color=yellow,
                    arrowprops=dict(arrowstyle='->', color=yellow))
        ax.annotate(text=f'{round(values.max(), 1)} mil. €',
                    ha='center', size=10,
                    xy=(values.max(), 2),
                    xytext=(values.max(), 4),
                    color=red,
                    arrowprops=dict(arrowstyle='->', color=red))
        
        # set titles and text
        ax.set_title(season, fontsize=20, color='w', fontweight='bold')

    fig_text(s=title,
            highlight_colors=[red, yellow],
            highlight_weights=['bold', 'bold'],
            x=0.5, y=1, ha='center',
            fontsize=28, color='w', fontweight='bold')
    plt.suptitle(subtitle,
                fontsize=20, color='w', fontweight='regular')
    # ylabel
    fig.text(s='Transfersum (mil. €)', x=0.5, y=-0.03, ha='center',
            fontsize=16, color='w', fontweight='bold')
    # signature
    fig.text(s='twitter.com/C_Roensholt',
            y=-0.02, x=1, ha='right',
            color='w', fontsize=12, fontweight='regular')
    plt.tight_layout()
    
    if save_name:
        plt.savefig(f'output/{save_name}.png', dpi=300, bbox_inches='tight')


def plot_table(top_transfers_out, top_transfers_in, save_name=None):        
    # PLOTTING
    fig, (ax1, ax2) = plt.subplots(figsize=(12,10),
                                nrows=1, ncols=2)

    # Set variables for both tables
    headers = ['Spiller', 'Skiftet fra', 'Skiftet til', 'Transfersum', 'Årstal']
    col_colors = [blue for _ in range(len(headers))]
    cellcolours = np.empty_like(top_transfers_out, dtype='object')
    for i, cl in enumerate(headers):
        cellcolours[:, i] = background_color

    # PLOT TOP 10 TRANSFERS OUT 
    table_1 = ax1.table(cellText=top_transfers_out.values, colLabels=headers,
                        loc='center', cellLoc='center', colColours=col_colors,
                        cellColours=cellcolours)
    table_1.scale(1, 1.75)
    table_1.auto_set_font_size(False)
    table_1.set_fontsize(8)

    # adjust column widths
    table_1.auto_set_column_width(col=list(range(len(top_transfers_out.columns))))

    # Format table
    for cell in table_1.get_children():
        cell_text = cell.get_text().get_text()
        cell.get_text().set_color('w')
        cell.set_edgecolor('w')
        if cell_text in headers:
            cell.get_text().set_weight('bold')
            cell.set_fontsize(11)
    ax1.axis('off')
    ax1.axis('tight')
    ax1.set_facecolor(background_color)
    ax1.set_title('Top 10 salg i 3F Superligaen',
                y=0.75,
                color='w', fontsize=22, fontweight='bold')

    # PLOT TOP 10 TRANSFERS IN
    table_2 = ax2.table(cellText=top_transfers_in.values, colLabels=headers,
                        loc='center', cellLoc='center', colColours=col_colors,
                        cellColours=cellcolours)
    table_2.scale(1, 1.75)
    table_2.auto_set_font_size(False)
    table_2.set_fontsize(8)

    # adjust column widths
    table_2.auto_set_column_width(col=list(range(len(top_transfers_in.columns))))

    # Format table
    for cell in table_2.get_children():
        cell_text = cell.get_text().get_text()
        cell.get_text().set_color('w')
        cell.set_edgecolor('w')
        if cell_text in headers:
            cell.get_text().set_weight('bold')
            cell.set_fontsize(11)
    ax2.axis('off')
    ax2.axis('tight')
    ax2.set_facecolor(background_color)
    ax2.set_title('Top 10 køb i 3F Superligaen',
                y=0.75,
                color='w', fontsize=22, fontweight='bold')

    # Global table settings
    fig.set_facecolor(background_color)

    fig.text(s='twitter.com/C_Roensholt',
            y=0.3, x=0.9, ha='right',
            color='w', fontsize=10, fontweight='regular')
    fig.text(s='Data | transfermarkt.com',
            y=0.32, x=0.9, ha='right',
            color='w', fontsize=10, fontweight='regular')
    if save_name:
        plt.savefig(f'output/{save_name}.png', dpi=300)