#!/bin/bash

echo "Update the geoscents_stats repo to get the latest data!"
cp ~/geoscents_stats/*.json . && rm metadata.json
python3 plot_hist.py
