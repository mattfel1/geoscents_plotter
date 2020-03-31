#!/bin/bash
# $1 = base directory with data
rsync -avzh $1/plots/*js geoscents.net:~/visualization/
rsync -avzh $1/plots/*html geoscents.net:~/visualization/
rsync -avzh $1/plots/*css geoscents.net:~/visualization/
rsync -avzh $1/plots/*jpg geoscents.net:~/visualization/
rsync -avzh $1/plots/*gif geoscents.net:~/visualization/

