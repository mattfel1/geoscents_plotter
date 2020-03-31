import matplotlib.image as mpimg
import scipy.stats as stats 
import sys
import os
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
outdir_prefix = '/home/mattfel/' # lagos path
#outdir_prefix = '/' # local path

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
    with open(outdir_prefix + "/plots/" + continent + '.js', 'w+') as f:
        f.write('var dataSet = [')

def writeIndex():
    with open(outdir_prefix + "/plots/index.html", 'w+') as f:
        f.write("""
<script src="https://code.jquery.com/jquery-3.3.1.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
<link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css">
<link rel="stylesheet" href="theme.css">
<button class="lobby-btn" onclick="window.location.href = 'http://geoscents.net';">Back to Game</button>
<button class="room-btn" onclick="window.location.href = 'World.html';">World</button>
<button class="room-btn" onclick="window.location.href = 'Trivia.html';">Trivia</button>
<button class="room-btn" onclick="window.location.href = 'Europe.html';">Europe</button>
<button class="room-btn" onclick="window.location.href = 'Africa.html';">Africa</button>
<button class="room-btn" onclick="window.location.href = 'Asia.html';">Asia</button>
<button class="room-btn" onclick="window.location.href = 'Oceania.html';">Oceania</button>
<button class="room-btn" onclick="window.location.href = 'NAmerica.html';">N. America</button>
<button class="room-btn" onclick="window.location.href = 'SAmerica.html';">S. America</button>
<h1>Choose a map from above to view a data table!</h1>
NOTE: distance data was collected for a while before lat/lon data started getting collected. This is why the histograms show more data points than the animations.
<br><br>
Raw data can be found <a href="https://github.com/mattfel1/geoscents_stats">here</a>
""")

def writeCss():
    with open(outdir_prefix + "/plots/theme.css", 'w+') as f:
        f.write("""
.room-btn {
    cursor: pointer;
    border: 1px solid #333;
    width: 100px;
    padding: 2px 2px;
    margin: 3px 3px;
    font-size: 16px;
    background: #a9e7f9; /* fallback */
    background: -moz-linear-gradient(top,  #a9e7f9 0%, #77d3ef 4%, #05abe0 100%);
    background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#a9e7f9), color-stop(4%,#77d3ef), color-stop(100%,#05abe0));
    background: -webkit-linear-gradient(top,  #a9e7f9 0%,#77d3ef 4%,#05abe0 100%);
    background: -o-linear-gradient(top,  #a9e7f9 0%,#77d3ef 4%,#05abe0 100%);
    background: -ms-linear-gradient(top,  #a9e7f9 0%,#77d3ef 4%,#05abe0 100%);
    background: linear-gradient(to bottom,  #a9e7f9 0%,#77d3ef 4%,#05abe0 100%);
    border-radius: 2px;
    box-shadow: 0 0 4px rgba(0,0,0,0.3);
}

.lobby-btn {
	cursor: pointer;
	border: 1px solid #333;
	padding: 2px 2px;
	margin: 3px 3px;
	font-size: 16px;
	background: #ffcccc; /* fallback */
	background: -moz-linear-gradient(top,  #ffcccc 0%, #ff9999 4%, #ff6666 100%);
	background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#ffcccc), color-stop(4%,#ff9999), color-stop(100%,#ff6666));
	background: -webkit-linear-gradient(top,  #ffcccc 0%,#ff9999 4%,#ff6666 100%);
	background: -o-linear-gradient(top,  #ffcccc 0%,#ff9999 4%,#ff6666 100%);
	background: -ms-linear-gradient(top,  #ffcccc 0%,#ff9999 4%,#ff6666 100%);
	background: linear-gradient(to bottom,  #ffcccc 0%,#ff9999 4%,#ff6666 100%);
	border-radius: 2px;
	box-shadow: 0 0 4px rgba(0,0,0,0.3);
}

.special-room-btn {
    cursor: pointer;
    border: 1px solid #333;
    width: 100px;
    padding: 2px 2px;
    margin: 3px 3px;
    font-size: 16px;
    background: #ffe200; /* fallback */
    background: -moz-linear-gradient(top,  #ffe200 0%, #dbc300 4%, #bda800 100%);
    background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#ffe200), color-stop(4%,#dbc300), color-stop(100%,#bda800));
    background: -webkit-linear-gradient(top,  #ffe200 0%,#dbc300 4%,#bda800 100%);
    background: -o-linear-gradient(top,  #ffe200 0%,#dbc300 4%,#bda800 100%);
    background: -ms-linear-gradient(top,  #ffe200 0%,#dbc300 4%,#bda800 100%);
    background: linear-gradient(to bottom,  #ffe200 0%,#dbc300 4%,#bda800 100%);
    border-radius: 2px;
    box-shadow: 0 0 4px rgba(0,0,0,0.3);
}

.dataTables_filter {
   float: left !important;
}


.filter-btn {
    cursor: pointer;
    border: 1px solid #333;
    width: 200px;
    padding: 2px 2px;
    margin: 3px 3px;
    font-size: 16px;
    background: #a9e7f9; /* fallback */
    border-radius: 2px;
    box-shadow: 0 0 4px rgba(0,0,0,0.3);
}
""")
def addJs(entry):
    with open(outdir_prefix + "/plots/" + continent + '.js', 'a') as f:
        f.write('[%s],\n' % entry)
    
def finishJs(continent):
    with open(outdir_prefix + "/plots/" + continent + '.js', 'a') as f:
        f.write("""
];

$(document).ready(function() {
    $("#all").css("background","yellow");
    const table = $('#%s').DataTable( {
        data: dataSet,
        "lengthChange": true,
        "pageLength": 50,
        "search": {
            "search": ".*",
            "regex": true
        },
        "dom": '<"top"f>rt<"bottom"ipl><"clear">',
        deferRender:    true,
        "order": [[5, 'asc']],
        columns: [
            { title: "Type", "width": "5%%"},
            { title: "Country", "width": "5%%" },
            { title: "Admin", "width": "5%%"},
            { title: "City", "width": "5%%" },
            { title: "Avg Dist (km)", "width": "5%%" },
            { title: "Std Dist (km)", "width": "5%%" },
            { title: "# Clicks", "width": "5%%" },
            { title: "Histogram", "width": "5%%"},
            { title: "Game Replay", "width": "5%%"}
        ],
        columnDefs: [
            {
                render: function (data, type, full, meta) {
                    return "<div class='text-wrap width-150'>" + data + "</div>";
                },
                targets: [2,3,4]
            }
        ],
    } );
    $('#aggregates').on('click', function () {
        $("#aggregates").css("background","yellow");
        $("#entry").css("background","#a9e7f9");
        $("#all").css("background","#a9e7f9");
        table.columns(0).search("Aggregate").draw();
    });
    $('#all').on('click', function () {
        $("#aggregates").css("background","#a9e7f9");
        $("#entry").css("background","#a9e7f9");
        $("#all").css("background","yellow");
        table.columns(0).search("").draw();
    });
    $('#entry').on('click', function () {
        $("#aggregates").css("background","#a9e7f9");
        $("#entry").css("background","yellow");
        $("#all").css("background","#a9e7f9");
        table.columns(0).search("Entry").draw();
    });
    $(window).keydown(function(e){
        if ((e.ctrlKey || e.metaKey) && e.keyCode === 70) {
            e.preventDefault();
            $('#%s_filter input').focus();
            $('#%s_filter input').select();
        }
    });
} );
""" % (continent, continent, continent))
    
def trackAdmin(country):
    return country == 'United States' or country == 'Canada' or country == 'China' or country == 'India' or country == 'Brazil' or country == 'Russia' or country == 'Australia' or country == 'Indonesia'

def stripSpecial(x):
    # return re.sub(r'[^\x00-\x7F]','x', x)
    return re.sub(r'[^A-Za-z0-9\(\),. ]+','_',x)

def writeHtml(continent):
    with open(outdir_prefix + "/plots/" + continent + '.html', 'w+') as f:
        specialworld = 'special-' if continent == "World" else ""
        specialtrivia = 'special-' if continent == "Trivia" else ""
        specialeurope = 'special-' if continent == "Europe" else ""
        specialafrica = 'special-' if continent == "Africa" else ""
        specialasia = 'special-' if continent == "Asia" else ""
        specialoceania = 'special-' if continent == "Oceania" else ""
        specialnamerica = 'special-' if continent == "NAmerica" else ""
        specialsamerica = 'special-' if continent == "SAmerica" else ""
        f.write("""

<script src="https://code.jquery.com/jquery-3.3.1.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
<link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css">
<link rel="stylesheet" href="theme.css">
<button class="lobby-btn" onclick="window.location.href = 'http://geoscents.net';">Back to Game</button>
<button class="%sroom-btn" onclick="window.location.href = 'World.html';">World</button>
<button class="%sroom-btn" onclick="window.location.href = 'Trivia.html';">Trivia</button>
<button class="%sroom-btn" onclick="window.location.href = 'Europe.html';">Europe</button>
<button class="%sroom-btn" onclick="window.location.href = 'Africa.html';">Africa</button>
<button class="%sroom-btn" onclick="window.location.href = 'Asia.html';">Asia</button>
<button class="%sroom-btn" onclick="window.location.href = 'Oceania.html';">Oceania</button>
<button class="%sroom-btn" onclick="window.location.href = 'NAmerica.html';">N. America</button>
<button class="%sroom-btn" onclick="window.location.href = 'SAmerica.html';">S. America</button>
<h1>Data Table for %s Map</h1>
<button id="all" class="filter-btn">Show All</button>
<button id="aggregates" class="filter-btn">Show Aggregates Only</button>
<button id="entry" class="filter-btn">Show Entries Only</button>
<table id="%s" class="display" width="100%%"></table>
<script  type="text/javascript" src="%s.js"></script>

""" % (specialworld,specialtrivia,specialeurope,specialafrica,specialasia,specialoceania,specialnamerica,specialsamerica,continent, continent, continent))


def nextColor(color_idx, num_colors):
    spread = 11
    g = (1 + np.cos(color_idx * spread / num_colors * 2 * np.pi)) / 2.0
    r = (1 + np.cos((color_idx * spread + num_colors / 3) / num_colors * 2 * np.pi)) / 2.0
    b = (1 + np.cos((color_idx * spread + 2 * num_colors / 3) / num_colors * 2 * np.pi)) / 2.0
    return (r,g,b,0.75)


########
# MAIN #
########
pathlist = Path('.').glob('**/*.json')

writeIndex()
writeCss()

print('Output dir = %s' % (outdir_prefix + '/plots/'))
admin_to_country = {}
num_colors = 49.
color_idx = 0
dpi = 250

mapFilter = '' if (sys.argv) == 1 else sys.argv[1]
for path in [x for x in pathlist if mapFilter in str(x)]:
    # because path is object not string
    file = str(path)
    continent = file.replace('.json','')
    print(file)
    continent_map = mpimg.imread('./' + continent + '.png')
    writeHtml(continent)
    initJs(continent) 
   

    with open(file) as json_file:
        aggregate_dists = {} 
        aggregate_lats = {} 
        aggregate_lons = {} 
        aggregate_times = {} 
        aggregate_player_countries = {} 
        entriesSummary = []
        continentSummary = []
        data = json.load(json_file)
        entry_id = 0
        for entry in data:
            # if (entry_id == 5): break # early quit
            print('%s: (%d / %d): %s' % (continent, entry_id, len(data), entry))
            entry_id = entry_id + 1
            # Create entry for this city
            try:
                dist_data = data[entry]['dists']
                country = '-' if 'country' not in data[entry] else data[entry]['country']
                if trackAdmin(country):
                    aggregate_name = data[entry]['admin']
                    admin_to_country[aggregate_name] = country
                else:
                    aggregate_name = country
                if (aggregate_name in aggregate_dists): 
                    aggregate_dists[aggregate_name] = aggregate_dists[aggregate_name] + dist_data
                else:
                    aggregate_dists[aggregate_name] = dist_data
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
                plt.savefig(outdir_prefix + '/plots/' + fname, optimize=True)
                plt.clf()
                # # Interactive plot show
                #plt.show(block=False)
                #input("Press Enter to continue...")
                #plt.close('all')


                # Save entry in table
                anim_name = 'animation_' + continent + '_' + country + '_' + stripSpecial(entry.replace(' ','-').replace('/','-'))
                admin = "N/A" if 'admin' not in data[entry] else data[entry]['admin']
                reghist = '<a href=\\"%s\\"><img src=\\"%s\\" alt=\\"link\\" height=40px></a>' % (fname, fname)
                anim = '<a href=\\"%s\\"><img src=\\"%s\\" alt=\\"link\\" height=40px></a>' % (anim_name + '.gif', anim_name + '.gif')
                link = "https://en.wikipedia.org/wiki/Special:Search?search=" + stripSpecial(entry) + "&go=Go&ns0=1" if ('wiki' not in data[entry]) else data[entry]['wiki']
                linkedEntry = '<a href=\\"%s\\">%s</a>' % (link, stripSpecial(data[entry]['city'])) 
                addJs('"Entry","' + country + '","' + admin + '","' + linkedEntry + '","' + '%.1f' % mean_dist + '","' + '%.1f' % std_dist + '","' + str(len(dist_data)) + '","' + reghist + '","' + anim + '"')

                # Generate animation
                fileList = glob.glob(outdir_prefix + '/plots/raw_animation_' + continent + '*')
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
                if (aggregate_name in aggregate_lats): 
                    aggregate_lats[aggregate_name] = aggregate_lats[aggregate_name] + lats
                    aggregate_lons[aggregate_name] = aggregate_lons[aggregate_name] + lons
                    aggregate_times[aggregate_name] = aggregate_times[aggregate_name] + times
                    aggregate_player_countries[aggregate_name] = aggregate_player_countries[aggregate_name] + player_countries
                else:
                    aggregate_lats[aggregate_name] = lats
                    aggregate_lons[aggregate_name] = lons
                    aggregate_lats[aggregate_name] = lats
                    aggregate_times[aggregate_name] = times
                    aggregate_player_countries[aggregate_name] = player_countries
                timestep = 0.5
                final_frames = 1
                plt.figure(figsize=(MAP_WIDTH/dpi, MAP_HEIGHT/dpi), dpi=dpi)
                plt.imshow(continent_map)
                ax = plt.gca()
                plt.ylim([MAP_HEIGHT,0])
                plt.xlim([0,MAP_WIDTH])
                plt.title(entry)
                plt.axis('off')
                true_x, true_y = (0,0) if "true_lat" not in data[entry] else geoToMerc(continent, data[entry]["true_lat"], data[entry]["true_lon"]) 
                plt.scatter([true_x], [true_y], marker='*', color='w', s = 20, edgecolors = 'black')
                frame = 0
                legend_countries = []
                player_country_colors = {}
                color_idx = 0
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
                plt.legend(handles=patchList, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=3, title_fontsize=3, title='Player Country')
                rect = patches.Rectangle((0,0),80,80,linewidth=1,edgecolor='#17eb5e',facecolor='#17eb5e')
                ax.add_patch(rect)                
                for t in np.arange(10, 0, -timestep):
                    lowerbound = t - timestep
                    frame_lats = [x for x,stamp in zip(lats, times) if stamp > lowerbound and stamp <= t]
                    frame_lons = [x for x,stamp in zip(lons, times) if stamp > lowerbound and stamp <= t]
                    frame_player_countries = [x for x,stamp in zip(player_countries, times) if stamp > lowerbound and stamp <= t]
                    frame_ctr = int(np.ceil(t))
                    for i in range(len(frame_lats)):
                        x,y = geoToMerc(continent, float(frame_lats[i]), float(frame_lons[i]))
                        color = player_country_colors[frame_player_countries[i]]
                        plt.scatter([x],[y], color = color, s = 2)

                    time = plt.text(0, 60,str(frame_ctr),fontsize=12)
                    plt.savefig(outdir_prefix + '/plots/raw_' + anim_name + "_" + '%03d' % frame + ".png", optimize=True)
                    frame = frame + 1
                    time.set_visible(False)
                # make final frame
                rect = patches.Rectangle((0,0),80,80,linewidth=1,edgecolor='#ffad99',facecolor='#ffad99')
                ax.add_patch(rect)
                plt.text(0, 60,0,fontsize=12)
                for i in range(final_frames):
                    plt.savefig(outdir_prefix + '/plots/raw_' + anim_name + "_" + '%03d' % frame + ".png", optimize=True)
                    frame = frame + 1
                # export animation
                fp_in = outdir_prefix + "/plots/raw_" + anim_name + "_*.png"
                fp_out = outdir_prefix + "/plots/" + anim_name + ".gif"
                img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
                img.save(fp=fp_out, format='GIF', append_images=imgs,
                         save_all=True, duration=timestep*1000, loop=1)
                plt.clf()
                plt.close()
                fileList = glob.glob(outdir_prefix + '/plots/raw_animation_' + continent + '*')
                for filePath in fileList:
                    os.remove(filePath)

            except Exception as e: # work on python 3.x
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)


        # Add aggregate for each country
        if (continent != "Trivia"): 
            entry_id = 0
            for aggregate_name in aggregate_dists:
                print('%s: (%d / %d): %s' % (continent, entry_id, len(aggregate_dists), aggregate_name))
                entry_id = entry_id + 1
                try:
                    if (aggregate_name in admin_to_country):
                        country = admin_to_country[aggregate_name]
                        admin = aggregate_name
                    else:
                        country = aggregate_name
                    dist_data = aggregate_dists[aggregate_name]
                    mean_dist = np.mean(dist_data)
                    std_dist = np.std(dist_data)
                    bins = plt.hist(dist_data, bins=20)
                    x = np.linspace(0,max(dist_data),100)
                    fit = stats.norm.pdf(x, mean_dist, std_dist)
                    plt.plot(x,(max(bins[0]) / max(fit)) * fit)
                    plt.title('Aggregate for ' + aggregate_name)
                    plt.xlim([0,max(dist_data)])
                    fname = 'country_' + continent + '_' + aggregate_name + '.jpg'
                    fname = stripSpecial(fname.replace(' ','-').replace('/','-'))
                    plt.savefig(outdir_prefix + '/plots/' + fname, optimize=True)
                    plt.clf()
                    reghist = '<a href=\\"%s\\"><img src=\\"%s\\" alt=\\"link\\" height=40px></a>' % (fname, fname)
                    anim_name = 'animation_' + continent + '_' + aggregate_name
                    anim = '<a href=\\"%s\\"><img src=\\"%s\\" alt=\\"link\\" height=40px></a>' % (anim_name + '.gif', anim_name + '.gif')
                    link = "https://en.wikipedia.org/wiki/Special:Search?search=" + aggregate_name + "&go=Go&ns0=1" if ('wiki' not in data[entry]) else data[entry]['wiki']
                    if (aggregate_name in admin_to_country):
                        linkedAdmin = '<a href=\\"%s\\">%s</a>' % (link, admin)  
                        linkedCountry = country
                    else:
                        linkedAdmin = '-'
                        linkedCountry = '<a href=\\"%s\\">%s</a>' % (link, country) 
                    addJs('"Aggregate","' + linkedCountry + '","' + linkedAdmin + '","-","' + '%.1f' % mean_dist + '","' + '%.1f' % std_dist + '","' + str(len(dist_data)) + '","' + reghist + '","' + anim + '"')
        
                    # Generate animation
                    fileList = glob.glob(outdir_prefix + '/plots/raw_animation_' + continent + '*')
                    for filePath in fileList:
                        os.remove(filePath)
                    lats = aggregate_lats[aggregate_name]
                    lons = aggregate_lons[aggregate_name]
                    times = aggregate_times[aggregate_name]
                    player_countries = aggregate_player_countries[aggregate_name]
                    timestep = 0.25
                    final_frames = 30
                    plt.figure(figsize=(MAP_WIDTH/dpi, MAP_HEIGHT/dpi), dpi=dpi)
                    plt.imshow(continent_map)
                    ax = plt.gca()
                    plt.ylim([MAP_HEIGHT,0])
                    plt.xlim([0,MAP_WIDTH])
                    plt.title(aggregate_name)
                    plt.axis('off')
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
                    plt.legend(handles=patchList, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=3, title_fontsize=3, title='Player Country')
                    rect = patches.Rectangle((0,0),80,80,linewidth=1,edgecolor='#17eb5e',facecolor='#17eb5e')
                    ax.add_patch(rect)
                    for t in np.arange(10, 0, -timestep):
                        lowerbound = t - timestep
                        frame_lats = [x for x,stamp in zip(lats, times) if stamp > lowerbound and stamp <= t]
                        frame_lons = [x for x,stamp in zip(lons, times) if stamp > lowerbound and stamp <= t]
                        frame_player_countries = [x for x,stamp in zip(player_countries, times) if stamp > lowerbound and stamp <= t]
                        frame_ctr = int(np.ceil(t))
                        for i in range(len(frame_lats)):
                            x,y = geoToMerc(continent, float(frame_lats[i]), float(frame_lons[i]))
                            color = player_country_colors[frame_player_countries[i]]
                            plt.scatter([x],[y], color = color, s = 2)
                        time = plt.text(0, 60,str(frame_ctr),fontsize=20)
                        plt.savefig(outdir_prefix + '/plots/raw_' + anim_name + "_" + '%03d' % frame + ".png", optimize=True)
                        frame = frame + 1
                        time.set_visible(False)
                    # make final frame
                    rect = patches.Rectangle((0,0),80,80,linewidth=1,edgecolor='#ffad99',facecolor='#ffad99')
                    ax.add_patch(rect)
                    plt.text(0, 60,0,fontsize=20)
                    for i in range(final_frames):
                        plt.savefig(outdir_prefix + '/plots/raw_' + anim_name + "_" + '%03d' % frame + ".png", optimize=True)
                        frame = frame + 1
                    # export animation
                    fp_in = outdir_prefix + "/plots/raw_" + anim_name + "_*.png"
                    fp_out = outdir_prefix + "/plots/" + anim_name + ".gif"
                    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
                    img.save(fp=fp_out, format='GIF', append_images=imgs,
                             save_all=True, duration=timestep*1000, loop=1)
                    plt.clf()
                    plt.close()
                    fileList = glob.glob(outdir_prefix + '/plots/raw_animation_' + continent + '*')
                    for filePath in fileList:
                        os.remove(filePath)
                except Exception as e: # work on python 3.x
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)



    finishJs(continent)
            
        
