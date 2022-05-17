#!/bin/bash

echo "Update the geoscents_stats repo to get the latest data!"
cd ~/geoscents_stats
git pull

# Get click data
cd ~/geoscents_plotter
cp ~/geoscents_stats/data/*.json . && rm metadata.json
# Get player location data
cp ~/geoscents_stats/data/player_countries.csv .
# Get maps
cp ~/geoscents/resources/maps/*_terrain.png .

mv ~/plots/* ~/old_plots/
cp -r ~/geoscents/resources/flags ~/plots/

python3 plot_hist.py
# python3 plot_hist.py Asia &
# python3 plot_hist.py NAmerica &
# python3 plot_hist.py SAmerica &
# python3 plot_hist.py Europe &
# python3 plot_hist.py Oceania &
# python3 plot_hist.py World &
# sleep 10
# python3 plot_hist.py Trivia &
# python3 plot_hist.py Ukraine &
# python3 plot_hist.py Japan &
# python3 plot_hist.py Canada &
# python3 plot_hist.py Romania &
# python3 plot_hist.py Kenya &
# python3 plot_hist.py Argentina &
# python3 plot_hist.py Australia &
# python3 plot_hist.py Japan &
# python3 plot_hist.py Indonesia &
# python3 plot_hist.py Egypt &
# python3 plot_hist.py Spain &
# python3 plot_hist.py Iran &
# python3 plot_hist.py UnitedStates & # ????
# python3 plot_hist.py China &

wait

# Plot growth
bash plot_growth.sh

# bash transfer.sh
