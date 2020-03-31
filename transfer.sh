#!/bin/bash
scp /home/mattfel/plots/*js geoscents.net:~/visualization/
scp /home/mattfel/plots/*html geoscents.net:~/visualization/
scp /home/mattfel/plots/*css geoscents.net:~/visualization/
scp /home/mattfel/plots/*jpg geoscents.net:~/visualization/
for i in /home/mattfel/plots/*.gif; do
    [ -f "$i" ] || break
    [[ $(find $i -type f -size +1000000c 2>/dev/null) ]] && echo "compress $i" && gifsicle -i $i -O3 --colors 256 -o $i || echo "$i already compressed!"
done
scp /home/mattfel/plots/*gif geoscents.net:~/visualization/

#rsync --bwlimit=50000 -avzh $1/plots/*js geoscents.net:~/visualization/
#rsync --bwlimit=50000 -avzh $1/plots/*html geoscents.net:~/visualization/
#rsync --bwlimit=50000 -avzh $1/plots/*css geoscents.net:~/visualization/
#rsync --bwlimit=50000 -avzh $1/plots/*jpg geoscents.net:~/visualization/
#rsync --bwlimit=50000 -avzh $1/plots/*gif geoscents.net:~/visualization/

