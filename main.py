import requests         # Library for making HTTP requests
import json             # Allows conversion between JSON objects and python objects
from bs4 import BeautifulSoup    # Library that makes web-scraping easy   
import datetime         # Allows manipulation of date and time
import sys              # Allows script to terminate if error is encountered

# Strava uses these values to indentify the activity type (key)
type_dict = {
'Ride': 1, 'Alpine Ski': 2, 'Backcountry Ski': 3, 'Hike': 4, 
'Ice Skate': 5, 'Inline Skate': 6, 'Nordic Ski': 7, 'Roller Ski': 8, 
'Run': 9, 'Walk': 10, 'Workout': 11, 'Snowboard': 12, 'Snowshoe': 13, 
'Kitesurf': 14, 'Windsurf': 15, 'Swim': 16, 'Virtual Ride': 17, 
'E-Bike Ride': 18, 'Velomobile': 19, 'Canoe': 21, 'Kayaking': 22, 
'Rowing': 23, 'Stand Up Paddling': 24, 'Surfing': 25, 'Crossfit': 26, 
'Elliptical': 27, 'Rock Climb': 28, 'Stair-Stepper': 29, 'Weight Training': 30, 
'Yoga': 31, 'Handcycle': 51, 'Wheelchair': 52, 'Virtual Run': 53
}

timestart = datetime.datetime.now()
print("Gathering Strava Activity Data . . .")

# Activity URL from which the route will be scrubbed from
url = 'https://www.strava.com/activities/7521121367'
urlr = requests.get(url)

# Code for loading the http and scrubbing the relevant information
if urlr.status_code == 429:
    print('ERROR: Too many requests have been made')
elif urlr.status_code == 200:
    soup = BeautifulSoup(urlr.content, 'html.parser')

    divdata = soup.find('div', {'data-react-class':'ActivityPublic'})
    try:
        activity_dict = json.loads(divdata.get('data-react-props'))
    except AttributeError:
        print('This activity is private. Only public activities can be converted.')
        sys.exit(1)

    name = activity_dict['activity']['name']
    type = type_dict.get(activity_dict['activity']['type'])
    altitude = activity_dict['activity']['streams']['altitude']
    latlng = activity_dict['activity']['streams']['latlng']

    latitude = []
    longitude = []

    for i in range(len(latlng)):
        latitude.append(latlng[i][0])
        longitude.append(latlng[i][1])

    # Writing the .gpx file
    print('Creating .gpx File . . .')

    with open(name + '.gpx', 'w') as gpx:
        gpx.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n')
        gpx.write('<gpx creator="duncantee">' + '\n')
        gpx.write(' <trk>' + '\n')
        gpx.write('  <name>' + name + '</name>' + '\n')
        gpx.write('  <type>' + str(type) + '</type>' + '\n')
        gpx.write('  <trkseg>' + '\n')
        for i in range(len(latlng)):
            gpx.write('   <trkpt lat="' + str(latitude[i]) +'" lon="' + str(longitude[i]) + '">' + '\n')
            gpx.write('    <ele>' + str(altitude[i]) + '</ele>' + '\n')
            gpx.write('   </trkpt>' + '\n')
        gpx.write('  </trkseg>' + '\n')
        gpx.write(' </trk>' + '\n')
        gpx.write('</gpx>')

        timeend = datetime.datetime.now()
        delta = timeend - timestart
        print('Done in ', delta.total_seconds(), ' seconds!')
else:
    print('ERROR: Unexpected error occured.')