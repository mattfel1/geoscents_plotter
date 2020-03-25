import scipy.stats as stats 
import sys
import os
import ipinfo
import json
from pathlib import Path
import urllib.request
import re
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def initJs(continent):
    with open("/plots/" + continent + '.js', 'w+') as f:
        f.write('var dataSet = [')

def addJs(entry):
    with open("/plots/" + continent + '.js', 'a') as f:
        f.write('[%s],\n' % entry)
    
def finishJs(continent):
    with open("/plots/" + continent + '.js', 'a') as f:
        f.write("""
];

$(document).ready(function() {
    $('#%s').DataTable( {
        data: dataSet,
        "lengthChange": false,
        "pageLength": 9999,
        "search": {
            "search": ".*",
            "regex": true
        },
        "order": [[5, 'asc']],
        columns: [
            { title: "Type" },
            { title: "Country" },
            { title: "Admin" },
            { title: "City" },
            { title: "In-game Name" },
            { title: "Mean distance (km)" },
            { title: "Stddev distance (km)" },
            { title: "Standard plot"},
            { title: "On-map plot"}
        ]
    } );
} );
""" % continent)
    

def stripSpecial(x):
    return re.sub(r'[^\x00-\x7F]','x', x)

def writeHtml(continent):
    with open("/plots/" + continent + '.html', 'w+') as f:
        f.write("""
<script src="https://code.jquery.com/jquery-3.3.1.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
<link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css">
<h1>Data for %s</h1>
<table id="%s" class="display" width="100%%"></table>
<script  type="text/javascript" src="%s.js"></script>
""" % (continent, continent, continent))


pathlist = Path('.').glob('**/*.json')

for path in pathlist:
    # because path is object not string
    file = str(path)
    continent = file.replace('.json','')
    print(file)
    i = 0
    writeHtml(continent)
    initJs(continent) 
   

    with open(file) as json_file:
        countries = {} 
        entriesSummary = []
        continentSummary = []
        data = json.load(json_file)
        for entry in data:
            try:
                dist_data = data[entry]['dists']
                country = data[entry]['country']
                if (country in countries): 
                    countries[country] = countries[country] + dist_data
                else:
                    countries[country] = dist_data
                mean_dist = data[entry]['mean_dist']
                std_dist = data[entry]['std_dist']
                x = np.linspace(0,max(dist_data),100)
                bins = plt.hist(dist_data, bins=20)
                fit = stats.norm.pdf(x, mean_dist, std_dist)
                plt.plot(x,(max(bins[0]) / max(fit)) * fit)
                plt.title(entry)
                plt.xlim([0,max(dist_data)])
                fname = 'entry_' + continent + '_' + data[entry]['country'] + '_' + entry + '.jpg'
                fname = stripSpecial(fname.replace(' ','-').replace('/','-'))
                plt.savefig('/plots/' + fname, optimize=True)
                plt.clf()
                try: 
                    admin = data[entry]['admin']
                except:
                    admin = "N/A"
                reghist = '<a href=\\"%s\\"><img src=\\"%s\\" height=60px></a>' % (fname, fname)
                addJs('"Entry","' + country + '","' + admin + '","' + stripSpecial(data[entry]['city']) + '","' + stripSpecial(entry) + '","' + '%.1f' % mean_dist + '","' + '%.1f' % std_dist + '","' + reghist + '","' + 'tbd' + '"')
            except: 
                print('Failed on %s' % entry)
                print(sys.exc_info()[0])
                continue
            #plt.show(block=False)
            #input("Press Enter to continue...")
            #plt.close('all')
            #i = i + 1
            #if (i == 20): 
            #    break
        if (continent != "Trivia"): 
            for country in countries:
                dist_data = countries[country]
                mean_dist = np.mean(dist_data)
                std_dist = np.std(dist_data)
                bins = plt.hist(dist_data, bins=20)
                x = np.linspace(0,max(dist_data),100)
                fit = stats.norm.pdf(x, mean_dist, std_dist)
                plt.plot(x,(max(bins[0]) / max(fit)) * fit)
                plt.title('Aggregate for ' + country)
                plt.xlim([0,max(dist_data)])
                fname = 'country_' + continent + '_' + country + '.jpg'
                fname = stripSpecial(fname.replace(' ','-').replace('/','-'))
                plt.savefig('/plots/' + fname, optimize=True)
                plt.clf()
                reghist = '<a href=\\"%s\\"><img src=\\"%s\\" height=60px></a>' % (fname, fname)
                addJs('"Aggregate","' + country + '","","","","' + '%.1f' % mean_dist + '","' + '%.1f' % std_dist + '","' + reghist + '","' + 'tbd' + '"')
    
    finishJs(continent)
            
        
