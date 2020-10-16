#!/bin/bash

cp ~/geoscents_stats/growth.csv .
python3 ./plot_growth.py
rm growth.csv

