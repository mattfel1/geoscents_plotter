import matplotlib.image as mpimg
import scipy.stats as stats 
import sys
import os
import json
from pathlib import Path
import random
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
import glob

from time import gmtime, strftime
import time


import warnings
warnings.filterwarnings("ignore")


update_stamp = time.strftime("%a, %b %d %Y @ %I:%M %p %Z", time.gmtime())
MAP_WIDTH = 1530
MAP_HEIGHT = 900
outdir_prefix = '/home/mattfel/'
generate_gifs = True
verbose = False

def geoToMerc(room,lat,lon):
    # Copy from geoscents resources/constants.js

    MAP_BOUNDS = {
        "World": {
            "min_lon": -180,
            "max_lon": 180,
            "max_lat": -65.5,
            "min_lat": 77.2,
            "lat_ts": 0
        },
        "World Capitals": {
            "min_lon": -180,
            "max_lon": 180,
            "max_lat": -65.5,
            "min_lat": 77.2,
            "lat_ts": 0
        },
        "Trivia": {
            "min_lon": -180,
            "max_lon": 180,
            "max_lat": -56.0,
            "min_lat": 80.85,
            "lat_ts": 0
        },
        "N. America": {
            "min_lon": -141,
            "max_lon": -43,
            "max_lat": 10.0,
            "min_lat": 56.0,
            "lat_ts": 0
        },
        "S. America": {
            "min_lon": -140,
            "max_lon": 17,
            "max_lat": -56.0,
            "min_lat": 24.1,
            "lat_ts": 0
        },
        "Europe": {
            "min_lon": -36.3,
            "max_lon": 52,
            "max_lat": 35.0,
            "min_lat": 66.3,
            "lat_ts": 0
        },
        "Africa": {
            "min_lon": -60,
            "max_lon": 82,
            "max_lat": -36.3,
            "min_lat": 41.0,
            "lat_ts": 0
        },
        "Asia": {
            "min_lon": 25,
            "max_lon": 158,
            "max_lat": -1,
            "min_lat": 61.05,
            "lat_ts": 0
        },
        "Oceania": {
            "min_lon": 92,
            "max_lon": 252,
            "max_lat": -54.55,
            "min_lat": 28,
            "lat_ts": 0
        },
        "Argentina": {
            "min_lon": -102,
            "max_lon": -20,
            "max_lat": -56.5,
            "min_lat": -20,
            "lat_ts": 0
        },
        "Australia": {
            "min_lon": 97,
            "max_lon": 170,
            "max_lat": -45.5,
            "min_lat": -8,
            "lat_ts": 0
        },
        "Canada": {
            "min_lon": -152.1,
            "max_lon": -40,
            "max_lat": 38,
            "min_lat": 72.5,
            "lat_ts": 0
        },
        "Japan": {
            "min_lon": 110,
            "max_lon": 164.5,
            "max_lat": 23.5,
            "min_lat": 49,
            "lat_ts": 0
        },
        "Kenya": {
            "min_lon": 30,
            "max_lon": 49,
            "max_lat": -5.33,
            "min_lat": 5.9,
            "lat_ts": 0
        },
        "Romania": {
            "min_lon": 18.8,
            "max_lon": 33.7,
            "max_lat": 43,
            "min_lat": 49,
            "lat_ts": 0
        },
        "Ukraine": {
            "min_lon": 17.4,
            "max_lon": 45.3,
            "max_lat": 43.18,
            "min_lat": 54,
            "lat_ts": 0
        },
        "Peru": {
            "min_lon": -92,
            "max_lon": -55,
            "max_lat": -19.5,
            "min_lat": 2,
            "lat_ts": 0
        },
        "Egypt": {
            "min_lon": 16.5,
            "max_lon": 41.7,
            "max_lat": 20.81,
            "min_lat": 34,
            "lat_ts": 0
        },
        "Indonesia": {
            "min_lon": 84.5,
            "max_lon": 151,
            "max_lat": -23.5,
            "min_lat": 15,
            "lat_ts": 0
        },
        "Spain": {
            "min_lon": -14.18,
            "max_lon": 8,
            "max_lat": 35,
            "min_lat": 45,
            "lat_ts": 0
        },
        "China": {
            "min_lon": 62,
            "max_lon": 148,
            "max_lat": 16.85,
            "min_lat": 56,
            "lat_ts": 0
        },
        "United States": {
            "min_lon": -130,
            "max_lon": -60,
            "max_lat": 22,
            "min_lat": 53.7,
            "lat_ts": 0
        },
        "Iran": {
            "min_lon": 36,
            "max_lon": 72.6,
            "max_lat": 24,
            "min_lat": 42,
            "lat_ts": 0
        },
        "Brazil": {
            "min_lon": -91.7,
            "max_lon": -17,
            "max_lat": -34,
            "min_lat": 8,
            "lat_ts": 0
        },
        "Mexico": {
            "min_lon": -120,
            "max_lon": -80,
            "max_lat": 13.61,
            "min_lat": 35,
            "lat_ts": 0
        },
        "India": {
            "min_lon": 50,
            "max_lon": 107.3,
            "max_lat": 6,
            "min_lat": 37,
            "lat_ts": 0
        },
        "Italy": {
            "min_lon": -2.1,
            "max_lon": 25.4,
            "max_lat": 36,
            "min_lat": 48,
            "lat_ts": 0
        },
        "United Kingdom": {
            "min_lon": -19.55,
            "max_lon": 15,
            "max_lat": 49.5,
            "min_lat": 61,
            "lat_ts": 0
        },
        "Germany": {
            "min_lon": -2.1,
            "max_lon": 23,
            "max_lat": 46.8,
            "min_lat": 56,
            "lat_ts": 0
        },
        "France": {
            "min_lon": -10.2,
            "max_lon": 17,
            "max_lat": 41,
            "min_lat": 52,
            "lat_ts": 0
        },
        "Nigeria": {
            "min_lon": -2.48,
            "max_lon": 19,
            "max_lat": 3.5,
            "min_lat": 16,
            "lat_ts": 0
        },
        "South Africa": {
            "min_lon": 9,
            "max_lon": 37,
            "max_lat": -35.51,
            "min_lat": -21,
            "lat_ts": 0
        },
        "Vatican City": {
            "min_lon": 12.440,
            "max_lon": 12.4605,
            "max_lat": 41.899,
            "min_lat": 41.908,
            "lat_ts": 0
        },
        "Pakistan": {
            "min_lon": 52.25,
            "max_lon": 84,
            "max_lat": 23,
            "min_lat": 39,
            "lat_ts": 0
        },
        "Democratic Republic of the Congo": {
            "min_lon": 3.53,
            "max_lon": 41,
            "max_lat": -14,
            "min_lat": 8,
            "lat_ts": 0
        },
        "New Zealand": {
            "min_lon": 151,
            "max_lon": 190.4,
            "max_lat": -49,
            "min_lat": -31.4,
            "lat_ts": 0
        },
        "Turkey": {
            "min_lon": 22,
            "max_lon": 48,
            "max_lat": 33.14,
            "min_lat": 45,
            "lat_ts": 0
        },
        "Switzerland": {
            "min_lon": 4,
            "max_lon": 12.66,
            "max_lat": 45,
            "min_lat": 48.5,
            "lat_ts": 0
        },
        "Morocco": {
            "min_lon": -25,
            "max_lon": 10,
            "max_lat": 20.03,
            "min_lat": 38,
            "lat_ts": 0
        },
        "Philippines": {
            "min_lon": 105,
            "max_lon": 140,
            "max_lat": 2,
            "min_lat": 22.15,
            "lat_ts": 0
        },
        "Vietnam": {
            "min_lon": 90,
            "max_lon": 120.1,
            "max_lat": 8,
            "min_lat": 25,
            "lat_ts": 0
        },
        "South Korea": {
            "min_lon": 121,
            "max_lon": 135.75,
            "max_lat": 33,
            "min_lat": 40,
            "lat_ts": 0
        },
        "Saudi Arabia": {
            "min_lon": 23.8,
            "max_lon": 63.5,
            "max_lat": 15,
            "min_lat": 36,
            "lat_ts": 0
        }
    }
    if (room not in MAP_BOUNDS):
        return 0, 0

    zero_lat = MAP_BOUNDS[room]["min_lat"]
    max_lat = MAP_BOUNDS[room]["max_lat"]
    min_lon = MAP_BOUNDS[room]["min_lon"]
    max_lon = MAP_BOUNDS[room]["max_lon"]
    lat_ts = MAP_BOUNDS[room]["lat_ts"]

    # get col value
    if (lon < min_lon):
        col = (lon + 360 - min_lon) * (MAP_WIDTH / (max_lon - min_lon));
    else: 
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
        f.write("""
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
        stateSave: true,
        "stateDuration": 60 * 5,
        "dom": '<"top"f>rt<"bottom"ipl><"clear">',
        deferRender:    true,
        "order": [[4, 'asc']],
        columns: [
            { title: "Type", "width": "3%%"},
            { title: "Flag", "width": "3%%"},
            { title: "Country", "width": "5%%" },
            { title: "Admin", "width": "5%%"},
            { title: "City", "width": "10%%" },
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
                targets: [3,4,5]
            },
            { "type": "alt-string", targets: 1 }
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
    // Hijack ctrl+f to jump to filter bar
    // $(window).keydown(function(e){
    //     if ((e.ctrlKey || e.metaKey) && e.keyCode === 70) {
    //         e.preventDefault();
    //         $('#%s_filter input').focus();
    //         $('#%s_filter input').select();
    //     }
    // });
} );

var dataSet = [
""" % (continent.replace(" ","_").replace(".","_"), continent, continent))

def writeIndex(header, countries):
    with open(outdir_prefix + "/plots/index.html", 'w+') as f:
        f.write("""
<!DOCTYPE html>
<head prefix="og: http://ogp.me/ns#">
    <meta charset="UTF-8">
    <meta name="description" content="Plots for Geoscents. An online multiplayer world geography game!  Test your knowledge of city locations." />
    <title>GeoScents Plots</title>
    <!-- Place this tag in your head or just before your close body tag. -->
    <link rel="icon" type="image/png" href="https://geoscents.net/resources/favicon.png" sizes="48x48">
    <meta name="GeoScents Plots" content="Plots for Geoscents.  An online multiplayer world geography game!  Test your knowledge of city locations. This is a recreation of the game Geosense from geosense.net.">
    <meta property="og:image" content="https://geoscents.net/resources/ogimage.png" />
<script src="https://code.jquery.com/jquery-3.3.1.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
<style>
table, td, th {
  border: 1px solid black;
}

table {
  border-collapse: collapse;
}

th {
  height: 50px;
}
</style>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6780905379201491"
     crossorigin="anonymous"></script>
</head>
<body>
<script src="https://code.jquery.com/jquery-3.3.1.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
<link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css">
<link rel="stylesheet" href="theme.css">
<button class="lobby-btn" onclick="window.location.href = 'https://geoscents.net';">Back to Game</button>
<button class="special-room-btn" onclick="window.location.href = 'index.html';">Home</button>""")
        # skip first two columns in header
        i = 0;
        for x in header:
            if (i >= 2):
                f.write("""<button class="room-btn" onclick="window.location.href = '""" + x + """.html';">""" + x + "<br><small><div id=\"" + x + """_count"></div></small></button>
""")
            i = i + 1



        f.write("""<h1>Choose a map from above to view a data table!</h1>
<small>(Last updated %s)</small><br><br>
You can opt-out of contributing to this database by typing /private in the chat box while playing the game. <br><br>
<br><br>
This page is updated approximately every 8 hours.  Raw data can be found <a href="https://github.com/mattfel1/geoscents_stats">here</a>.  <br><br>

<h3>Mean Error by Player Country (<a href="growth.png">Collected Data Points Over Time</a>)</h3>
<!--<table>
  <tr>
    <th> </th>
    <th>Country</th>
    <th># Clicks</th> 
  </tr>
s
</table>-->
<table id="index" class="display" width="75%%" align="left"></table>
<br><br>

<script  type="text/javascript" src="index.js"></script>

<script src="counts.js"></script>
</body>
</html>
""" % (update_stamp))

    with open(outdir_prefix + "/plots/index.js", 'w+') as f:
        f.write("""
$(document).ready(function() {
    $("#all").css("background","yellow");
    const table = $('#index').DataTable( {
        data: dataSet,
        "lengthChange": true,
        "pageLength": 200,
        "search": {
            "search": ".*",
            "regex": true
        },
        stateSave: true,
        "stateDuration": 60 * 5,
        "dom": '<"top"f>rt<"bottom"ipl><"clear">',
        deferRender:    true,
        "order": [[2, 'des']],
        columns: [
            { title: "", "width": "1%%"},
            """)
        i = 0
        targets = []
        for x in header:
            sfx = "<br>(avg. error, km)" if i > 1 else ""
            f.write("{ title: \"" + x.replace('"','') + sfx + "\", \"width\": \"5%%\"}")
            if (i < len(header) - 1):
                f.write(",\n")
            if (i >= 2):
                targets.append(str(i))

            i = i + 1

        f.write("""],
        columnDefs: [
            {
                render: function (data, type, full, meta) {
                    return "<div class='text-wrap width-150'>" + data + "</div>";
                },
                targets: [""" + ",".join(targets) + """]
            }
        ],
    } );
    table.on( 'order.dt search.dt', function () {
        table.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        } );
    } ).draw();
} );

var dataSet = [ %s ];
""" % countries)

def initCount():
    with open(outdir_prefix + "/plots/counts.js", 'w+') as f:
        f.write("")

def writeCount(continent, count):
    with open(outdir_prefix + "/plots/counts.js", 'a') as f:
        f.write("\ndocument.getElementById(\"" + continent + "_count\").innerHTML = \"(" + str(count) + " clicks)\";")

def writeCss():
    with open(outdir_prefix + "/plots/theme.css", 'w+') as f:
        f.write("""
.room-btn {
    cursor: pointer;
    border: 1px solid #333;
    width: 120px;
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
    width: 120px;
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
        f.write("""];""")
    
def trackAdmin(country):
    return country == 'United States' or country == 'Canada' or country == 'China' or country == 'India' or country == 'Brazil' or country == 'Russia' or country == 'Australia' or country == 'Indonesia' or country == "Ukraine"

def stripSpecial(x):
    # return re.sub(r'[^\x00-\x7F]','x', x)
    return re.sub(r'[^A-Za-z0-9\(\),. ]+','_',x)

def writeHtml(continent, cols):
    with open(outdir_prefix + "/plots/" + continent + '.html', 'w+') as f:
        f.write("""
<!DOCTYPE html>
<head prefix="og: http://ogp.me/ns#">
    <meta name="description" content="Plots for Geoscents. An online multiplayer world geography game!  Test your knowledge of city locations." />
    <title>(%s) GeoScents Plots</title>
    <!-- Place this tag in your head or just before your close body tag. -->
    <link rel="icon" type="image/png" href="https://geoscents.net/resources/favicon.png" sizes="48x48">
    <meta name="(%s) GeoScents Plots" content="Plots for Geoscents.  An online multiplayer world geography game!  Test your knowledge of city locations. This is a recreation of the game Geosense from geosense.net.">
    <meta property="og:image" content="https://geoscents.net/resources/ogimage.png" />
<script src="https://code.jquery.com/jquery-3.3.1.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6780905379201491"
     crossorigin="anonymous"></script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6780905379201491"
     crossorigin="anonymous"></script>
</head>
<body>

<script src="https://code.jquery.com/jquery-3.3.1.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
<link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css">
<link rel="stylesheet" href="theme.css">
<button class="lobby-btn" onclick="window.location.href = 'https://geoscents.net';">Back to Game</button>
<button class="room-btn" onclick="window.location.href = 'index.html';">Home</button>""" % (continent, continent))
        for x in cols:
            btn_class = "special-room-btn" if continent == x else "room-btn"
            f.write("""<button class='""" + btn_class + """' onclick="window.location.href = '""" + x + """.html';">""" + x + """<br><small><div id='""" + x + """_count'></div></small></button>""")

        f.write("""<h1>Data Table for %s Map <!-- <a href="all_%s.jpg"><img src="all_%s.jpg" class="img-thumbnail" alt="link" height=75px></a> --> </h1>
<small>(Last updated %s)</small><br>
<button id="all" class="filter-btn">Show All</button>
<button id="aggregates" class="filter-btn">Show Aggregates Only</button>
<button id="entry" class="filter-btn">Show Entries Only</button>
<table id="%s" class="display" width="100%%"></table>
<br><br>
<a href="all_%s.jpg" style="color:#F0F0F0;">cheatsheet</a>
<script  type="text/javascript" src="%s.js"></script>
<script src="counts.js"></script>
</body>
</html>

""" % (continent,continent,continent, update_stamp, continent.replace(" ","_").replace(".","_"), continent, continent))

def initAnim(fname, stepsize, flag):
    with open(outdir_prefix + "/plots/" + fname + '.js', 'w+') as f:
        f.write("""
  var sliderSteps = [];
  for (i = 0; i < %d; i++) {
    sliderSteps.push({
      method: 'animate',
      label: Math.floor(10*(10 - i * %f)) / 10,
      args: [['frame' + (i)], {
        mode: 'immediate',
        transition: {duration: 0},
        frame: {duration: %d, redraw: false},
      }]
    });
  }

function bubbles(center, radius, n_points=10) {
    var step = 1 / (n_points-1)
    var x = []
    var y = []
    for (var p = 0; p < n_points; p++) {
      x.push(center[0]+radius*Math.cos(2*3.14159*step*p))
      y.push(center[1]+radius*Math.sin(2*3.14159*step*p))
    }
    return [x, y]
  }


""" % (10 / stepsize + 1, stepsize, stepsize * 1000))

    with open(outdir_prefix + "/plots/" + fname + '.html', 'w+') as f:
        f.write("""
<head>
    <!-- Load plotly.js into the DOM -->
    %s
    <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
</head>

<body>
    <div id='%s'><!-- Plotly chart will be drawn inside this DIV --></div>
    <script src='%s'></script>
</body>
""" % (flag, fname, fname + '.js'))

def addFrame(fname, serieslabel, raw_country, numclicks, xdata, ydata, marker):
    with open(outdir_prefix + "/plots/" + fname + '.js', 'a') as f:
        f.write("""var %s = {
  name: '%s (%d)',
  rawname: '%s',
  x: [null,%s],
  y: [null,%s],
  mode: 'markers',
  hoverinfo: 'name',
  type: 'scatter', 
  marker: {%s}
}
""" % (serieslabel, raw_country, numclicks, raw_country, ','.join([str(int(x)) for x in xdata]), ','.join([str(int(x)) for x in ydata]), marker))


def addMean(fname, xmean, ymean, xvar, yvar):
    with open(outdir_prefix + "/plots/" + fname + '.js', 'a') as f:
        f.write("""
let bubble = bubbles([%s, %s], %s)
var average = {
  name: 'average joe (1)',
  rawname: 'average joe',
            type: 'circle',
            xref: 'x',
            yref: 'y',
            x: bubble[0],
            y: bubble[1],
            opacity: 0.8,
            fillcolor: 'blue',
            line: {
                color: 'blue'
            }
}
""" % (xmean, ymean, xvar))

def finishAnim(fname, continent, title, countries, maxframe, stepsize):
    with open(outdir_prefix + "/plots/" + fname + '.js', 'a') as f:
        # f.write("""var traces = [ truth, average, %s]
        f.write("""var traces = [ truth, %s]
var layout = {
  xaxis: {
    range: [ 0, 1530 ],
    showgrid: false,
    zeroline: false,
    visible: false
  },
  yaxis: {
    range: [0, 900],
    showgrid: false,
    zeroline: false,
    visible: false
  },
  width: 1530,
  height: 900,
  images: [
      {
        "source": "https://geoscents.net/resources/maps/%s_terrain.png",
        "xref": "x",
        "yref": "y",
        "x": 0,
        "y": 900,
        "opacity": 0.4,
        "sizex": 1530,
        "sizey": 900,
        "sizing": "stretch",
        "layer": "below"
      }
      ],
  title:"%s",
  hovermode: 'closest',
    updatemenus: [{
      x: 0,
      y: 0,
      yanchor: 'top',
      xanchor: 'left',
      showactive: false,
      direction: 'left',
      type: 'buttons',
      pad: {t: 0, r: 0},
      buttons: [{
        method: 'animate',
        args: [null, {
          mode: 'immediate',
          fromcurrent: true,
          transition: {duration: 0},
          frame: {duration: %d, redraw: false}
        }],
        label: 'Play'
      }, {
        method: 'animate',
        args: [[null], {
          mode: 'immediate',
          transition: {duration: 0},
          frame: {duration: 0, redraw: false}
        }],
        label: 'Pause'
      }]
    }],
   // Finally, add the slider and use `pad` to position it
   // nicely next to the buttons.
    sliders: [{
      pad: {l: 0, t: 0},
      currentvalue: {
        visible: true,
        prefix: 'Time Remaining: ',
        xanchor: 'right',
        font: {size: 20, color: '#666'}
      },
      steps: sliderSteps
    }]
    };
frames = [""" % (','.join([x.replace(' ','') + str(maxframe) for x in sorted(countries)]), continent.lower().replace(" ", "").replace(".", ""), title, stepsize * 1000))
        for i in range(0,maxframe+1):
            # f.write("""{data: [truth,average,%s], name: "frame%d"},
            f.write("""{data: [truth,%s], name: "frame%d"},
""" % (','.join([x.replace(' ','') + str(i) for x in sorted(countries)]), i))

        f.write("""]
Plotly.newPlot('%s', {data: traces, layout: layout, frames: frames})

const isFirefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1; // hack for scaling
var noScale = false;

setInterval(() => {
    // Set zoom for resolution
    const scale = Math.floor(50*Math.max(0.6, Math.min(1, window.innerWidth / 1800)))/50;
    document.documentElement.style.zoom = scale;
    document.documentElement.style.MozTransform = "scale(" + scale + ")";
    document.documentElement.style.MozTransformOrigin = "0 0";
}, 1000);


""" % fname)


def nextColor(color_idx, num_colors):
    spread = 11
    g = (1 + np.cos(color_idx * spread / num_colors * 2 * np.pi)) / 2.0
    r = (1 + np.cos((color_idx * spread + num_colors / 3) / num_colors * 2 * np.pi)) / 2.0
    b = (1 + np.cos((color_idx * spread + 2 * num_colors / 3) / num_colors * 2 * np.pi)) / 2.0
    return (r,g,b,0.75)


########
# MAIN #
########
pathlist = glob.glob("*.json")

sorted_countries = []
i = 0
header = ""
with open('./player_countries.csv') as fp:
    for cnt, line in enumerate(fp):
        if (cnt < 1):
            header = line.replace("[","").replace("]","").replace("\n","").split(",")
        else:
            sorted_countries.append(line)
        # if ("Total" in line.split(',')[0]):
        #     sorted_countries.append("""<tr><td> </td><td><b>""" + ','.join(line.split(',')[0:-1]) + """</b></td><td><b>""" + line.split(',')[-1] + "</b></td></tr>\n")
        # else:
        #     i = i + 1
        #     sorted_countries.append(("""<tr><td>%d.""" % i) + """</td><td>""" + ','.join(line.split(',')[0:-1]) + """</td><td>""" + line.split(',')[-1] + "</td></tr>\n")

writeIndex(header, '\n'.join(sorted_countries))
writeCss()

print('Output dir = %s' % (outdir_prefix + '/plots/'))
admin_to_country = {}
admin_to_iso2 = {}
num_colors = 49.
color_idx = 0
dpi = 250
timestep = 0.2

initCount() 

errors = []

for path in pathlist:
    
    # because path is object not string
    file = str(path)
    continent = file.split('/')[-1].replace('.json','')
    continent_count = 0
    if (continent not in header):
        continue
    print(file)
    continent_map = mpimg.imread('/home/mattfel/geoscents/resources/maps/' + continent.lower().replace(" ", "").replace(".", "") + '_terrain.png')
    writeHtml(continent, header[2:])
    initJs(continent) 
   

    with open(file) as json_file:
        aggregate_dists = {} 
        aggregate_lats = {} 
        aggregate_lons = {} 
        aggregate_times = {} 
        aggregate_player_countries = {} 
        entriesSummary = []
        continentSummary = []
        continentTrueXs = []
        continentTrueYs = []
        data = json.load(json_file)
        entry_id = 0
        for entry in data:
            # if (entry_id == 5): break # early quit
            if (verbose):
                print('%s: (%d / %d): %s' % (continent, entry_id, len(data), entry))
            entry_id = entry_id + 1
            # Create entry for this city
            try:
                dist_data = data[entry]['dists']
                iso2 = 'NONE' if (not 'iso2' in data[entry]) else data[entry]['iso2']
                continent_count = continent_count + len(dist_data)
                country = '-' if 'country' not in data[entry] else data[entry]['country']
                if trackAdmin(country):
                    aggregate_name = data[entry]['admin']
                    admin_to_iso2[aggregate_name] = iso2
                    admin_to_country[aggregate_name] = country
                else:
                    aggregate_name = country
                    admin_to_iso2[aggregate_name] = iso2
                if (aggregate_name in aggregate_dists): 
                    aggregate_dists[aggregate_name] = aggregate_dists[aggregate_name] + dist_data
                else:
                    aggregate_dists[aggregate_name] = dist_data
                mean_dist = data[entry]['mean_dist'] if 'mean_dist' in data[entry] else 0
                std_dist = data[entry]['std_dist'] if 'std_dist' in data[entry] else 0
                outliers = [x for x in dist_data if x - mean_dist > 3 * std_dist]
                inliers = [x for x in dist_data if x - mean_dist <= 3 * std_dist]
                if (len(inliers) == 0):
                    inliers = [0]
                max_inlier = max(inliers)
                x = np.linspace(0,max_inlier,100)
                bins = plt.hist(inliers, bins=20)
                fit = stats.norm.pdf(x, mean_dist, std_dist)
                # Generate hist
                plt.plot(x,(max(bins[0]) / max(fit)) * fit)
                plt.title(entry)
                plt.xlabel('Error in km (%d outliers omitted)' % len(outliers))
                plt.ylabel('# of players')
                plt.xlim([0,max_inlier])
                fname_country = data[entry]['country'] if 'country' in data[entry] else 'unk_country'
                fname = 'entry_' + continent + '_' + fname_country + '_' + entry + '.jpg'
                fname = stripSpecial(fname.replace(' ','-').replace('/','-'))
                plt.savefig(outdir_prefix + '/plots/' + fname)
                plt.clf()
                # # Interactive plot show
                #plt.show(block=False)
                #input("Press Enter to continue...")
                #plt.close('all')


                # Save entry in table
                anim_name = 'animation_' + continent + '_' + country.replace('/','-') + '_' + stripSpecial(entry.replace(' ','-').replace('/','-'))
                admin = "N/A" if 'admin' not in data[entry] else data[entry]['admin']
                reghist = '<a href=\\"%s\\"><img src=\\"%s\\" class=\\"img-thumbnail\\" alt=\\"link\\" height=40px></a>' % (fname, fname)
                anim = '<a href=\\"%s\\"><img src=\\"%s\\" class=\\"img-thumbnail\\" alt=\\"link\\" height=40px></a>' % (anim_name + '.html', continent + '.jpg')
                link = "https://en.wikipedia.org/wiki/Special:Search?search=" + stripSpecial(entry) + "&go=Go&ns0=1" if ('wiki' not in data[entry]) else data[entry]['wiki']
                linkedCity = data[entry]['city'] if 'city' in data[entry] else "unknown_city"
                linkedEntry = '<a href=\\"%s\\">%s</a>' % (link, linkedCity) 
                flag = " " if (iso2 == 'NONE') else '<img src=\\"flags/%s.png\\" class=\\"img-thumbnail\\" style=\\"border:1px solid black;\\" alt=\\"%s\\" height=20px>' % (iso2.lower(), iso2.lower())
                bigflag = " " if (iso2.lower() == 'none') else '<img src="flags/%s.png" style="border:1px solid black;display:block;margin:0 auto" class="img-thumbnail" height=40px>' % iso2.lower()
                addJs('"Entry","' + flag + '","' + country + '","' + admin + '","' + linkedEntry + '","' + '%.1f' % mean_dist + '","' + '%.1f' % std_dist + '","' + str(len(dist_data)) + '","' + reghist + '","' + anim + '"')

                # Source image from game resources/maps now, so no need to copy here?

                # if (entry_id == 1):
                #     plt.figure(figsize=(MAP_WIDTH/dpi, MAP_HEIGHT/dpi), dpi=dpi)
                #     plt.imshow(continent_map)
                #     plt.axis('off')
                #     plt.savefig(outdir_prefix + '/plots/' + continent + '.jpg')
                #     plt.clf()
                #     plt.close()

                initAnim(anim_name, timestep, bigflag)
                true_x, true_y = (0,0) if ("true_lat" not in data[entry] or "true_lon" not in data[entry]) else geoToMerc(continent, data[entry]["true_lat"], data[entry]["true_lon"]) 
                addFrame(anim_name, "truth", "truth", 1, [true_x], [900 - true_y], 'size: 9, symbol: \'star-open\', color: \'black\'')
                continentTrueXs.append(true_x)
                continentTrueYs.append(true_y)
                if (generate_gifs):
                    # Generate animation
                    lats = data[entry]['lats']
                    lons = data[entry]['lons']
                    mean_lat = np.mean([x for x in lats if type(x) == float])
                    mean_lon = np.mean([x for x in lons if type(x) == float])
                    mean_x, mean_y = geoToMerc(continent, mean_lat, mean_lon) 
                    # addMean(anim_name, mean_x, 900 - mean_y, 2, 2)
                    times = data[entry]['times']
                    player_countries = data[entry]['countries']
                    lons = [l for l,x in zip(lons,lats) if x != "x"]
                    times = [l for l,x in zip(times,lats) if x != "x"]
                    player_countries = [l for l,x in zip(player_countries,lats) if x != "x"]
                    lats = [x for x in lats if x != "x"]
                    x_by_country = {}
                    y_by_country = {}
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
                    all_countries = []
                    country_numclicks = {}
                    for c in player_countries:
                        if (c not in all_countries):
                            all_countries.append(c)
                            country_numclicks[c] = player_countries.count(c)
                            x_by_country[c] = []
                            y_by_country[c] = []
                    frame = 0
                    for t in np.arange(10, -timestep, -timestep):
                        lowerbound = t - timestep
                        frame_lats = [x for x,stamp in zip(lats, times) if stamp > lowerbound and stamp <= t]
                        frame_lons = [x for x,stamp in zip(lons, times) if stamp > lowerbound and stamp <= t]
                        frame_player_countries = [x for x,stamp in zip(player_countries, times) if stamp > lowerbound and stamp <= t]
                        for i in range(len(frame_lats)):
                            x,y = geoToMerc(continent, float(frame_lats[i]), float(frame_lons[i]))
                            x_by_country[frame_player_countries[i]] = x_by_country[frame_player_countries[i]] + [x]
                            y_by_country[frame_player_countries[i]] = y_by_country[frame_player_countries[i]] + [900-y]
                        for c in all_countries:
                            addFrame(anim_name, c.replace(' ','') + str(frame), c, country_numclicks[c], x_by_country[c], y_by_country[c], 'size: 5')
                        frame = frame + 1
                    finishAnim(anim_name, continent, entry, all_countries, frame - 1, timestep)


            except Exception as e: # work on python 3.x
                errors.append("problem with entry " + entry + " in " + continent)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                if hasattr(e, 'message'):
                    print(e.message)


        # Report total count for continent and make continent aggregate map
        writeCount(continent, continent_count)
        plt.clf()
        plt.figure(figsize=(MAP_WIDTH/dpi, MAP_HEIGHT/dpi), dpi=dpi)
        plt.imshow(continent_map)
        ax = plt.gca()
        plt.ylim([MAP_HEIGHT,0])
        plt.xlim([0,MAP_WIDTH])
        plt.title("All " + str(len(continentTrueXs)) + " entries for " + continent)
        plt.axis('off')
        for i in range(len(continentTrueXs)):
            x,y = continentTrueXs[i], continentTrueYs[i]
            plt.scatter([x], [y], marker='*', color='w', s = 20, edgecolors = 'black')
        plt.savefig(outdir_prefix + '/plots/all_' + continent + ".jpg")
        plt.clf()

        # Add aggregate for each country
        if (continent != "Trivia"): 
            entry_id = 0
            for aggregate_name in aggregate_dists:
                if (verbose):
                    print('%s: (%d / %d): %s' % (continent, entry_id, len(aggregate_dists), aggregate_name))
                entry_id = entry_id + 1
                try:
                    if (aggregate_name in admin_to_country):
                        country = admin_to_country[aggregate_name]
                        admin = aggregate_name
                    else:
                        country = aggregate_name
                    iso2 = "NONE" if (aggregate_name not in admin_to_iso2) else admin_to_iso2[aggregate_name].lower()
                    dist_data = aggregate_dists[aggregate_name]
                    mean_dist = np.mean(dist_data)
                    std_dist = np.std(dist_data)
                    outliers = [x for x in dist_data if x - mean_dist > 3 * std_dist]
                    inliers = [x for x in dist_data if x - mean_dist <= 3 * std_dist]
                    if (len(inliers) == 0):
                        inliers = [1]
                    bins = plt.hist(inliers, bins=20)
                    x = np.linspace(0,max(inliers),100)
                    fit = stats.norm.pdf(x, mean_dist, std_dist)
                    plt.plot(x,(max(bins[0]) / max(fit)) * fit)
                    plt.title('Aggregate for ' + aggregate_name)
                    plt.xlim([0,max(inliers)])
                    plt.xlabel('Error in km (%d outliers omitted)' % len(outliers))
                    plt.ylabel('# of players')
                    fname = 'country_' + continent + '_' + aggregate_name + '.jpg'
                    fname = stripSpecial(fname.replace(' ','-').replace('/','-'))
                    plt.savefig(outdir_prefix + '/plots/' + fname)
                    plt.clf()
                    reghist = '<a href=\\"%s\\"><img src=\\"%s\\" class=\\"img-thumbnail\\" alt=\\"link\\" height=40px></a>' % (fname, fname)
                    anim_name = 'animation_' + continent + '_' + aggregate_name.replace(' ','-').replace('/','-')
                    anim = '<a href=\\"%s\\"><img src=\\"%s\\" class=\\"img-thumbnail\\" alt=\\"link\\" height=40px></a>' % (anim_name + '.html', continent + '.jpg')
                    link = "https://en.wikipedia.org/wiki/Special:Search?search=" + aggregate_name + "&go=Go&ns0=1"
                    flag = " " if (iso2.lower() == 'none') else '<img src=\\"flags/%s.png\\" style=\\"border:1px solid black;\\" class=\\"img-thumbnail\\" alt=\\"%s\\" height=20px>' % (iso2, iso2)
                    bigflag = " " if (iso2.lower() == 'none') else '<img src="flags/%s.png" style="border:1px solid black;display:block;margin:0 auto" class="img-thumbnail" height=40px>' % iso2.lower()
                    if (aggregate_name in admin_to_country):
                        linkedAdmin = '<a href=\\"%s\\">%s</a>' % (link, admin)  
                        linkedCountry = country
                    else:
                        linkedAdmin = '-'
                        linkedCountry = '<a href=\\"%s\\">%s</a>' % (link, country) 
                    addJs('"Aggregate","' + flag + '","' + linkedCountry + '","' + linkedAdmin + '","-","' + '%.1f' % mean_dist + '","' + '%.1f' % std_dist + '","' + str(len(dist_data)) + '","' + reghist + '","' + anim + '"')
        
                    # Generate animation
                    if (generate_gifs):
                        initAnim(anim_name, timestep, bigflag)
                        addFrame(anim_name, "truth", "truth", 0, [], [], 'size: 8, symbol: \'star-open\', color: \'black\'')
                        lats = aggregate_lats[aggregate_name]
                        lons = aggregate_lons[aggregate_name]
                        mean_lat = np.mean([x for x in lats if type(x) == float])
                        mean_lon = np.mean([x for x in lons if type(x) == float])
                        mean_x, mean_y = geoToMerc(continent, mean_lat, mean_lon) 
                        # addMean(anim_name, mean_x, 900 - mean_y, 2, 2)
                        times = aggregate_times[aggregate_name]
                        player_countries = aggregate_player_countries[aggregate_name]
                        lons = [l for l,x in zip(lons,lats) if x != "x"]
                        times = [l for l,x in zip(times,lats) if x != "x"]
                        player_countries = [l for l,x in zip(player_countries,lats) if x != "x"]
                        lats = [x for x in lats if x != "x"]
                        x_by_country = {}
                        y_by_country = {}
                        all_countries = []
                        country_numclicks = {}
                        for c in player_countries:
                            if (c not in all_countries):
                                all_countries.append(c)
                                country_numclicks[c] = player_countries.count(c)
                                x_by_country[c] = []
                                y_by_country[c] = []
                        frame = 0
                        for t in np.arange(10, -timestep, -timestep):
                            lowerbound = t - timestep
                            frame_lats = [x for x,stamp in zip(lats, times) if stamp > lowerbound and stamp <= t]
                            frame_lons = [x for x,stamp in zip(lons, times) if stamp > lowerbound and stamp <= t]
                            frame_player_countries = [x for x,stamp in zip(player_countries, times) if stamp > lowerbound and stamp <= t]
                            for i in range(len(frame_lats)):
                                x,y = geoToMerc(continent, float(frame_lats[i]), float(frame_lons[i]))
                                x_by_country[frame_player_countries[i]] = x_by_country[frame_player_countries[i]] + [x]
                                y_by_country[frame_player_countries[i]] = y_by_country[frame_player_countries[i]] + [900-y]
                            for c in all_countries:
                                addFrame(anim_name, c.replace(' ','') + str(frame), c, country_numclicks[c], x_by_country[c], y_by_country[c], 'size: 5')
                            frame = frame + 1
                        finishAnim(anim_name, continent, aggregate_name, all_countries, frame - 1, timestep)

                            
                except Exception as e: # work on python 3.x
                    errors.append("problem with aggregate " + aggregate + " in " + continent)
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    if hasattr(e, 'message'):
                        print(e.message)



    finishJs(continent)

for x in errors:
    print(x)
            
        
