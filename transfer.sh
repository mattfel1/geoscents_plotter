#!/bin/bash
# $1 = base directory with data
rsync -avzh $1/plots/* geoscents.net:~/visualization/
