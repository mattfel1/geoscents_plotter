import matplotlib.pyplot as plt
import csv
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time

x = []
y = []

with open('growth.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    next(plots)
    for row in plots:
        x.append(dt.datetime.fromtimestamp(int(row[0])))
        y.append(int(row[1]))

plt.plot(x,y)
plt.xlabel('Date')
plt.ylabel('# Clicks')

ax=plt.gca()
xfmt = md.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(xfmt)
plt.xticks( rotation=25 )

plt.title('Number of recorded data points over time')
plt.legend()
plt.savefig('/home/mattfel/plots/growth.png', optimize=True)
#plt.show()
