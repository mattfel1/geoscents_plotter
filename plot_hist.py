import matplotlib.image as mpimg
import scipy.stats as stats 
import sys
import os
import ipinfo
import json
from pathlib import Path
import urllib.request
import re
import subprocess
import imageio
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import glob
from PIL import Image


MAP_WIDTH = 1530
MAP_HEIGHT = 900

def geoToMerc(room,lat,lon):
    if (room == "World"):
        zero_lat = 77.
        max_lat = -65.5
        min_lon = -180.
        max_lon = 180.
        lat_ts = 0.
    elif (room == "NAmerica"):
        zero_lat = 56.
        max_lat = 10.
        min_lon = -141.
        max_lon = -43.
        lat_ts = 0
    elif (room == "Europe"):
        zero_lat = 66.3
        max_lat = 35.
        min_lon = -36.
        max_lon = 52.
        lat_ts = 0.
    elif (room == "Trivia"):
        zero_lat = 81.
        max_lat = -56.
        min_lon = -180.
        max_lon = 180.
        lat_ts = 0.
    elif (room == "Africa"):
        zero_lat = 41.
        max_lat = -36.
        min_lon = -60.
        max_lon = 82.
        lat_ts = 0.
    elif (room == "Asia"):
        zero_lat = 61.
        max_lat = -0.5
        min_lon = 25.
        max_lon = 158.
        lat_ts = 0.
    elif (room == "Oceania"):
        zero_lat = 10.5
        max_lat = -48.
        min_lon = 69.
        max_lon = 180.
        lat_ts = 0.
    elif (room == "SAmerica"):
        zero_lat = 24.
        max_lat = -56.
        min_lon = -140.
        max_lon = 17.
        lat_ts = 0.
    # get col value
    col = (lon - min_lon) * (MAP_WIDTH / (max_lon - min_lon));
    # convert from degrees to radians
    latRad = lat * np.pi / 180;

    eqMin = np.arctanh(np.sin(zero_lat * np.pi/180));
    eqRange = np.arctanh(np.sin(max_lat * np.pi/180)) - eqMin;

    # get row value
    row = (MAP_HEIGHT / eqRange) * (np.arctanh(np.sin(latRad)) - eqMin);
    return col, row # transposed in python coords compared to js coords

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
        deferRender:    true,
        "order": [[5, 'asc']],
        columns: [
            { title: "Type", "width": "5%"},
            { title: "Country", "width": "5%" },
            { title: "Admin", "width": "5%"},
            { title: "City", "width": "5%" },
            { title: "In-game Name", "width": "20%"},
            { title: "Avg Dist (km)", "width": "5%" },
            { title: "Std Dist (km)", "width": "5%" },
            { title: "# Clicks", "width": "5%" },
            { title: "Standard plot", "width": "5%"},
            { title: "On-map plot", "width": "5%"}
        ],
        columnDefs: [
            {
                render: function (data, type, full, meta) {
                    return "<div class='text-wrap width-150'>" + data + "</div>";
                },
                targets: [2,3,4]
            }
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


def nextColor(color_idx, num_colors):
    g = (1 + np.cos(color_idx * 11 / num_colors * 2 * np.pi)) / 2.0
    r = (1 + np.cos((color_idx * 11 + num_colors / 3) / num_colors * 2 * np.pi)) / 2.0
    b = (1 + np.cos((color_idx * 11 + 2 * num_colors / 3) / num_colors * 2 * np.pi)) / 2.0
    return (r,g,b,0.75)


########
# MAIN #
########
pathlist = Path('.').glob('**/*.json')

player_country_colors = {}
num_colors = 30.
color_idx = 0

for path in pathlist:
    # because path is object not string
    file = str(path)
    continent = file.replace('.json','')
    print(file)
    continent_map = mpimg.imread('./' + continent + '.png')
    writeHtml(continent)
    initJs(continent) 
   

    with open(file) as json_file:
        countries = {} 
        entriesSummary = []
        continentSummary = []
        data = json.load(json_file)
        entry_id = 0
        for entry in data:
            if (entry_id == 5): break
            print('(%d / %d): %s' % (entry_id, len(data), entry))
            entry_id = entry_id + 1
            # Create entry for this city
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
                # Generate hist
                plt.plot(x,(max(bins[0]) / max(fit)) * fit)
                plt.title(entry)
                plt.xlim([0,max(dist_data)])
                fname = 'entry_' + continent + '_' + data[entry]['country'] + '_' + entry + '.jpg'
                fname = stripSpecial(fname.replace(' ','-').replace('/','-'))
                plt.savefig('/plots/' + fname, optimize=True)
                plt.clf()
                # # Interactive plot show
                #plt.show(block=False)
                #input("Press Enter to continue...")
                #plt.close('all')


                # Save entry in table
                anim_name = 'animation_' + continent + '_' + data[entry]['country'] + '_' + entry
                admin = "N/A" if 'admin' not in data[entry] else data[entry]['admin']
                reghist = '<a href=\\"%s\\"><img src=\\"%s\\" height=60px></a>' % (fname, fname)
                anim = '<a href=\\"%s\\"><img src=\\"%s\\" height = 60px></a>' % (anim_name + '.gif', anim_name + '.gif')
                link = "https://en.wikipedia.org/wiki/Special:Search?search=" + stripSpecial(entry) + "&go=Go&ns0=1" if ('wiki' not in data[entry]) else data[entry]['wiki']
                linkedEntry = '<a href=\\"%s\\">%s</a>' % (link, stripSpecial(entry)) 
                addJs('"Entry","' + country + '","' + admin + '","' + stripSpecial(data[entry]['city']) + '","' + linkedEntry + '","' + '%.1f' % mean_dist + '","' + '%.1f' % std_dist + '","' + str(len(dist_data)) + '","' + reghist + '","' + anim + '"')

                # Generate animation
                fileList = glob.glob('/plots/raw_animation*')
                for filePath in fileList:
                    os.remove(filePath)
                lats = data[entry]['lats']
                lons = data[entry]['lons']
                times = data[entry]['times']
                player_countries = data[entry]['countries']
                lons = [l for l,x in zip(lons,lats) if x != "x"]
                times = [l for l,x in zip(times,lats) if x != "x"]
                player_countries = [l for l,x in zip(player_countries,lats) if x != "x"]
                lats = [x for x in lats if x != "x"]
                timestep = 0.25
                final_frames = 30
                dpi = 200
                plt.figure(figsize=(MAP_WIDTH/dpi, MAP_HEIGHT/dpi), dpi=dpi)
                plt.imshow(continent_map)
                ax = plt.gca()
                plt.ylim([MAP_HEIGHT,0])
                plt.xlim([0,MAP_WIDTH])
                plt.title(entry)
                plt.axis('off')
                true_x, true_y = (0,0) if "true_lat" not in data[entry] else geoToMerc(continent, data[entry]["true_lat"], data[entry]["true_lon"]) 
                plt.scatter([true_x], [true_y], marker='*', color='w', s = 60, edgecolors = 'black')
                frame = 0
                legend_countries = []
                patchList = []
                for c in player_countries:
                    if (c not in player_country_colors):
                        player_country_colors[c] = nextColor(color_idx, num_colors)
                        color_idx = (color_idx + 1) % num_colors
                    if (c not in legend_countries):
                        legend_countries.append(c)
                        dk = patches.Patch(color=player_country_colors[c], label=c)
                        patchList.append(dk)
                # lines = [Line2D([0], [0], color=c, linewidth=3, linestyle='--') for c in colors]
                plt.legend(handles=patchList, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=4)


                for t in np.arange(10, 0, -timestep):
                    lowerbound = t - timestep
                    frame_lats = [x for x,stamp in zip(lats, times) if stamp > lowerbound and stamp <= t]
                    frame_lons = [x for x,stamp in zip(lons, times) if stamp > lowerbound and stamp <= t]
                    frame_player_countries = [x for x,stamp in zip(player_countries, times) if stamp > lowerbound and stamp <= t]
                    frame_ctr = int(np.ceil(t))
                    for i in range(len(frame_lats)):
                        x,y = geoToMerc(continent, float(frame_lats[i]), float(frame_lons[i]))
                        color = player_country_colors[frame_player_countries[i]]
                        plt.scatter([x],[y], color = color, s = 5)
                    rect = patches.Rectangle((0,0),80,80,linewidth=1,edgecolor='#17eb5e',facecolor='#17eb5e')
                    ax.add_patch(rect)
                    time = plt.text(0, 60,str(frame_ctr),fontsize=20)
                    plt.savefig('/plots/raw_' + anim_name + "_" + '%03d' % frame + ".png", optimize=True)
                    frame = frame + 1
                    time.set_visible(False)
                # make final frame
                rect = patches.Rectangle((0,0),80,80,linewidth=1,edgecolor='#ffad99',facecolor='#ffad99')
                ax.add_patch(rect)
                plt.text(0, 60,0,fontsize=20)
                for i in range(final_frames):
                    plt.savefig('/plots/raw_' + anim_name + "_" + '%03d' % frame + ".png", optimize=True)
                    frame = frame + 1
                # export animation
                fp_in = "/plots/raw_" + anim_name + "_*.png"
                fp_out = "/plots/" + anim_name + ".gif"
                img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
                img.save(fp=fp_out, format='GIF', append_images=imgs,
                         save_all=True, duration=250, loop=0)
                plt.clf()


            except: 
                print('Failed on %s' % entry)
                print(sys.exc_info()[0])
                continue


        # Add aggregate for each country
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
                link = "https://en.wikipedia.org/wiki/Special:Search?search=" + country + "&go=Go&ns0=1" if ('wiki' not in data[entry]) else data[entry]['wiki']
                linkedCountry = '<a href=\\"%s\\">%s</a>' % (link, country) 
                addJs('"Aggregate","' + linkedCountry + '","","","","' + '%.1f' % mean_dist + '","' + '%.1f' % std_dist + '","' + str(len(dist_data)) + '","' + reghist + '","' + '-' + '"')
    
    finishJs(continent)
            
        
