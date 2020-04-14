#!/bin/bash

echo "Update the geoscents_stats repo to get the latest data!"
cd ~/geoscents_stats
git pull
cd ~/geoscents_plotter
cp ~/geoscents_stats/*.json . && rm metadata.json
cp ~/geoscents_stats/player_countries.csv .
mv ~/plots/* ~/old_plots/
python3 plot_hist.py Africa &
python3 plot_hist.py Asia &
python3 plot_hist.py NAmerica &
python3 plot_hist.py SAmerica &
python3 plot_hist.py Europe &
python3 plot_hist.py Oceania &
python3 plot_hist.py World &
python3 plot_hist.py Trivia &

wait

bash transfer.sh
