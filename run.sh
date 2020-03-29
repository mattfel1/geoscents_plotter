#!/bin/bash

cp ~/geoscents_stats/*.json . && rm metadata.json
python3 plot_hist.py
