#!/bin/bash

echo "Update the geoscents_stats repo to get the latest data!"
cd ~/geoscents_stats
git pull

# Get click data
cd ~/geoscents_plotter
cp ~/geoscents_stats/data/*.json . && rm metadata.json
# Get player location data
cp ~/geoscents_stats/data/player_countries.csv .

mv ~/plots/* ~/old_plots/
cp -r ~/geoscents/resources/flags ~/plots/

python3 plot_hist.py

wait

# Plot growth
bash plot_growth.sh

bash transfer.sh
