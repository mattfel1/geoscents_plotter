#!/bin/bash
#scp /home/mattfel/plots/*js geoscents.net:~/plots/
#scp /home/mattfel/plots/*html geoscents.net:~/plots/
#scp /home/mattfel/plots/*css geoscents.net:~/plots/
#scp /home/mattfel/plots/*jpg geoscents.net:~/plots/
#for i in /home/mattfel/plots/*.gif; do
#    [ -f "$i" ] || break
#    [[ $(find $i -type f -size +1000000c 2>/dev/null) ]] && echo "compress $i" && gifsicle -i $i -O3 --colors 256 -o $i || echo "$i already compressed!"
#done
#scp /home/mattfel/plots/*gif geoscents.net:~/plots/

rsync --bwlimit=50000 -avzh /home/mattfel/plots/flags/* geoscents.net:~/plots/flags/
rsync --bwlimit=50000 -avzh /home/mattfel/plots/*js geoscents.net:~/plots/
rsync --bwlimit=50000 -avzh /home/mattfel/plots/*html geoscents.net:~/plots/
rsync --bwlimit=50000 -avzh /home/mattfel/plots/*css geoscents.net:~/plots/
rsync --bwlimit=50000 -avzh /home/mattfel/plots/*jpg geoscents.net:~/plots/
rsync --bwlimit=50000 -avzh /home/mattfel/plots/growth.png geoscents.net:~/plots/
#rsync --bwlimit=50000 -avzh $1/plots/*gif geoscents.net:~/plots/

