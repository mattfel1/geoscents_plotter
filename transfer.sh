#!/bin/bash
# $1 = base directory with data
scp $1/plots/*js geoscents.net:~/visualization/
scp $1/plots/*html geoscents.net:~/visualization/
scp $1/plots/*css geoscents.net:~/visualization/
scp $1/plots/*jpg geoscents.net:~/visualization/
scp $1/plots/*gif geoscents.net:~/visualization/

rsync --bwlimit=50000 -avzh $1/plots/*js geoscents.net:~/visualization/
rsync --bwlimit=50000 -avzh $1/plots/*html geoscents.net:~/visualization/
rsync --bwlimit=50000 -avzh $1/plots/*css geoscents.net:~/visualization/
rsync --bwlimit=50000 -avzh $1/plots/*jpg geoscents.net:~/visualization/
rsync --bwlimit=50000 -avzh $1/plots/*gif geoscents.net:~/visualization/

