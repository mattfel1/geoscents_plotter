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

from time import gmtime, strftime
import time

update_stamp = time.strftime("%a, %b %d %Y @ %I:%M %p %Z", time.gmtime())
MAP_WIDTH = 1530
MAP_HEIGHT = 900
outdir_prefix = '/home/mattfel/'
generate_gifs = True

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
        zero_lat = 28
        max_lat = -54.5
        min_lon = 92.
        max_lon = 252.
        lat_ts = 0.
    elif (room == "SAmerica"):
        zero_lat = 24.
        max_lat = -56.
        min_lon = -140.
        max_lon = 17.
        lat_ts = 0.
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
    $(window).keydown(function(e){
        if ((e.ctrlKey || e.metaKey) && e.keyCode === 70) {
            e.preventDefault();
            $('#%s_filter input').focus();
            $('#%s_filter input').select();
        }
    });
} );

var dataSet = [
""" % (continent, continent, continent))

def writeIndex(countries):
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
</head>
<body>
<script src="https://code.jquery.com/jquery-3.3.1.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
<link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css">
<link rel="stylesheet" href="theme.css">
<button class="lobby-btn" onclick="window.location.href = 'https://geoscents.net';">Back to Game</button>
<button class="special-room-btn" onclick="window.location.href = 'index.html';">Home</button>
<button class="room-btn" onclick="window.location.href = 'World.html';">World<br><small><div id="World_count"></div></small></button>
<button class="room-btn" onclick="window.location.href = 'Trivia.html';">Trivia<br><small><div id="Trivia_count"></div></small></button>
<button class="room-btn" onclick="window.location.href = 'Europe.html';">Europe<br><small><div id="Europe_count"></div></small></button>
<button class="room-btn" onclick="window.location.href = 'Africa.html';">Africa<br><small><div id="Africa_count"></div></small></button>
<button class="room-btn" onclick="window.location.href = 'Asia.html';">Asia<br><small><div id="Asia_count"></div></small></button>
<button class="room-btn" onclick="window.location.href = 'Oceania.html';">Oceania<br><small><div id="Oceania_count"></div></small></button>
<button class="room-btn" onclick="window.location.href = 'NAmerica.html';">N. America<br><small><div id="NAmerica_count"></div></small></button>
<button class="room-btn" onclick="window.location.href = 'SAmerica.html';">S. America<br><small><div id="SAmerica_count"></div></small></button>
<h1>Choose a map from above to view a data table!</h1>
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
            { title: "Player Country", "width": "5%%"},
            { title: "Total # Clicks", "width": "5%%" },
            { title: "World<br>(avg. error, km)", "width": "5%%"},
            { title: "Trivia<br>(avg. error, km)", "width": "5%%" },
            { title: "Europe<br>(avg. error, km)", "width": "5%%" },
            { title: "Africa<br>(avg. error, km)", "width": "5%%" },
            { title: "Asia<br>(avg. error, km)", "width": "5%%" },
            { title: "Oceania<br>(avg. error, km)", "width": "5%%"},
            { title: "N. America<br>(avg. error, km)", "width": "5%%"},
            { title: "S. America<br>(avg. error, km)", "width": "5%%"}
        ],
        columnDefs: [
            {
                render: function (data, type, full, meta) {
                    return "<div class='text-wrap width-150'>" + data + "</div>";
                },
                targets: [3,4,5,6,7,8,9,10]
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

def writeCount(count):
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

</head>
<body>

<script src="https://code.jquery.com/jquery-3.3.1.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
<link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css">
<link rel="stylesheet" href="theme.css">
<button class="lobby-btn" onclick="window.location.href = 'https://geoscents.net';">Back to Game</button>
<button class="room-btn" onclick="window.location.href = 'index.html';">Home</button>
<button class="%sroom-btn" onclick="window.location.href = 'World.html';">World<br><small><div id="World_count"></div></small></button>
<button class="%sroom-btn" onclick="window.location.href = 'Trivia.html';">Trivia<br><small><div id="Trivia_count"></div></small></button>
<button class="%sroom-btn" onclick="window.location.href = 'Europe.html';">Europe<br><small><div id="Europe_count"></div></small></button>
<button class="%sroom-btn" onclick="window.location.href = 'Africa.html';">Africa<br><small><div id="Africa_count"></div></small></button>
<button class="%sroom-btn" onclick="window.location.href = 'Asia.html';">Asia<br><small><div id="Asia_count"></div></small></button>
<button class="%sroom-btn" onclick="window.location.href = 'Oceania.html';">Oceania<br><small><div id="Oceania_count"></div></small></button>
<button class="%sroom-btn" onclick="window.location.href = 'NAmerica.html';">N. America<br><small><div id="NAmerica_count"></div></small></button>
<button class="%sroom-btn" onclick="window.location.href = 'SAmerica.html';">S. America<br><small><div id="SAmerica_count"></div></small></button>
<h1>Data Table for %s Map <!-- <a href="all_%s.jpg"><img src="all_%s.jpg" class="img-thumbnail" alt="link" height=75px></a> --> </h1>
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

""" % (continent, continent, specialworld,specialtrivia,specialeurope,specialafrica,specialasia,specialoceania,specialnamerica,specialsamerica,continent,continent,continent, update_stamp, continent, continent, continent))

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

def finishAnim(fname, continent, title, countries, maxframe, stepsize):
    with open(outdir_prefix + "/plots/" + fname + '.js', 'a') as f:
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
        "source": "https://geoscents.net/resources/%s.png",
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
frames = [""" % (','.join([x.replace(' ','') + str(maxframe) for x in sorted(countries)]), continent, title, stepsize * 1000))
        for i in range(0,maxframe+1):
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
pathlist = Path('.').glob('**/*.json')
sorted_countries = []
i = 0
with open('./player_countries.csv') as fp:
    for cnt, line in enumerate(fp):
        sorted_countries.append(line)
        # if ("Total" in line.split(',')[0]):
        #     sorted_countries.append("""<tr><td> </td><td><b>""" + ','.join(line.split(',')[0:-1]) + """</b></td><td><b>""" + line.split(',')[-1] + "</b></td></tr>\n")
        # else:
        #     i = i + 1
        #     sorted_countries.append(("""<tr><td>%d.""" % i) + """</td><td>""" + ','.join(line.split(',')[0:-1]) + """</td><td>""" + line.split(',')[-1] + "</td></tr>\n")

writeIndex('\n'.join(sorted_countries))
writeCss()

print('Output dir = %s' % (outdir_prefix + '/plots/'))
admin_to_country = {}
admin_to_iso2 = {}
num_colors = 49.
color_idx = 0
dpi = 250
timestep = 0.2


mapFilter = '' if (sys.argv) == 1 else sys.argv[1]
initCount() 
for path in [x for x in pathlist if mapFilter in str(x)]:
    # because path is object not string
    file = str(path)
    continent = file.replace('.json','')
    continent_count = 0
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
        continentTrueXs = []
        continentTrueYs = []
        data = json.load(json_file)
        entry_id = 0
        for entry in data:
            # if (entry_id == 5): break # early quit
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
                mean_dist = data[entry]['mean_dist']
                std_dist = data[entry]['std_dist']
                outliers = [x for x in dist_data if x - mean_dist > 3 * std_dist]
                inliers = [x for x in dist_data if x - mean_dist <= 3 * std_dist]
                x = np.linspace(0,max(inliers),100)
                bins = plt.hist(inliers, bins=20)
                fit = stats.norm.pdf(x, mean_dist, std_dist)
                # Generate hist
                plt.plot(x,(max(bins[0]) / max(fit)) * fit)
                plt.title(entry)
                plt.xlabel('Error in km (%d outliers omitted)' % len(outliers))
                plt.ylabel('# of players')
                plt.xlim([0,max(inliers)])
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
                reghist = '<a href=\\"%s\\"><img src=\\"%s\\" class=\\"img-thumbnail\\" alt=\\"link\\" height=40px></a>' % (fname, fname)
                anim = '<a href=\\"%s\\"><img src=\\"%s\\" class=\\"img-thumbnail\\" alt=\\"link\\" height=40px></a>' % (anim_name + '.html', continent + '.jpg')
                link = "https://en.wikipedia.org/wiki/Special:Search?search=" + stripSpecial(entry) + "&go=Go&ns0=1" if ('wiki' not in data[entry]) else data[entry]['wiki']
                linkedEntry = '<a href=\\"%s\\">%s</a>' % (link, data[entry]['city']) 
                flag = " " if (iso2 == 'NONE') else '<img src=\\"flags/%s.png\\" class=\\"img-thumbnail\\" style=\\"border:1px solid black;\\" alt=\\"%s\\" height=20px>' % (iso2.lower(), iso2.lower())
                bigflag = " " if (iso2.lower() == 'none') else '<img src="flags/%s.png" style="border:1px solid black;display:block;margin:0 auto" class="img-thumbnail" height=40px>' % iso2.lower()
                addJs('"Entry","' + flag + '","' + country + '","' + admin + '","' + linkedEntry + '","' + '%.1f' % mean_dist + '","' + '%.1f' % std_dist + '","' + str(len(dist_data)) + '","' + reghist + '","' + anim + '"')

                if (entry_id == 1):
                    plt.figure(figsize=(MAP_WIDTH/dpi, MAP_HEIGHT/dpi), dpi=dpi)
                    plt.imshow(continent_map)
                    plt.axis('off')
                    plt.savefig(outdir_prefix + '/plots/' + continent + '.jpg')
                    plt.clf()
                    plt.close()

                initAnim(anim_name, timestep, bigflag)
                true_x, true_y = (0,0) if "true_lat" not in data[entry] else geoToMerc(continent, data[entry]["true_lat"], data[entry]["true_lon"]) 
                addFrame(anim_name, "truth", "truth", 1, [true_x], [900 - true_y], 'size: 9, symbol: \'star-open\', color: \'black\'')
                continentTrueXs.append(true_x)
                continentTrueYs.append(true_y)
                if (generate_gifs):
                    # Generate animation
                    lats = data[entry]['lats']
                    lons = data[entry]['lons']
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
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                if hasattr(e, 'message'):
                    print(e.message)


        # Report total count for continent and make continent aggregate map
        writeCount(continent_count)
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
        plt.savefig(outdir_prefix + '/plots/all_' + continent + ".jpg", optimize=True)

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
                    iso2 = "NONE" if (aggregate_name not in admin_to_iso2) else admin_to_iso2[aggregate_name].lower()
                    dist_data = aggregate_dists[aggregate_name]
                    mean_dist = np.mean(dist_data)
                    std_dist = np.std(dist_data)
                    outliers = [x for x in dist_data if x - mean_dist > 3 * std_dist]
                    inliers = [x for x in dist_data if x - mean_dist <= 3 * std_dist]
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
                    plt.savefig(outdir_prefix + '/plots/' + fname, optimize=True)
                    plt.clf()
                    reghist = '<a href=\\"%s\\"><img src=\\"%s\\" class=\\"img-thumbnail\\" alt=\\"link\\" height=40px></a>' % (fname, fname)
                    anim_name = 'animation_' + continent + '_' + aggregate_name.replace(' ','-').replace('/','-')
                    anim = '<a href=\\"%s\\"><img src=\\"%s\\" class=\\"img-thumbnail\\" alt=\\"link\\" height=40px></a>' % (anim_name + '.html', continent + '.jpg')
                    link = "https://en.wikipedia.org/wiki/Special:Search?search=" + aggregate_name + "&go=Go&ns0=1" if ('wiki' not in data[entry]) else data[entry]['wiki']
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
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    if hasattr(e, 'message'):
                        print(e.message)



    finishJs(continent)
            
        
