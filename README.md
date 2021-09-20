# Analysis of the 2021 Superliga transfer window

The is a repository containing the code to analyze the Danish Superliga transfer windows from 2010 to 2021.

A Danish version blog post can be found on my website [here](http://roensholt-stats.com/2021-09-18-Superliga-Transfers/),
where I put some words on the visualisation which can be found in the `output` folder.

---------------

The repository consists of to folders `data` and `output`, and the main repo containing four `.py` files.

- `main_overall` - The main file where all functions are called in-order to create all visualizations.
- `plt_utils` - The plotting file which contains functions to create the different type of visualizations used in the analysis.
- `scrape_transfersmarkt` - The file used to gather transfer history data from the Danish Superliga (and all other leagues if necessary) from <transfermarkt.com>.
- `metadata` - The file contains data about colors used for plotting, academy teams and which area different countries are placed in.

--------------

This project is hugely inspired by the piece from [Tom Worville](https://twitter.com/Worville) in [The Athletic](https://theathletic.com/2802812/2021/09/02/transfer-window-analysed-less-spent-young-players-targeted-and-free-agents-have-defined-key-moves/?article_source=search&search_query=tow%20worville)
Furthermore, a huge thanks to [danzn1](https://twitter.com/danzn1) GitHub repository [tmscrape](https://github.com/znstrider/tmscrape) and FcRstats [tyrone_mings](https://github.com/FCrSTATS/tyrone_mings) package which I both have used in order to gather the data for the analysis.
