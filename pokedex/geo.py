from __future__ import unicode_literals
from prompt_toolkit import prompt
from geopy.geocoders import GoogleV3
from s2sphere import CellId, LatLng
from .utils import *

class Geo(object):
    def __init__(self):
        super(Geo, self).__init__()

    def get_location(self):
        try:
            self.location = load_config('config/location.yaml')
        except IOError:
            print('You do not have your location set yet!')
            self.location = self.set_location()


    def do_location(self, line):
        print('You are currently at {}, {}.'.format(
            self.location['latitude'], self.location['longitude']
        ))

        self.location = self.set_location()


    def set_location(self):
        location = prompt('Enter an address or location (ex. Washington, DC): ')
        if not location:
            raise Exception('No address entered, leaving current position.')

        position = self.get_pos_by_name(location)

        with open('config/location.yaml', 'w') as yaml_file:
            yaml_file.write(yaml.safe_dump(position, default_flow_style=False))

        return position


    def get_pos_by_name(self, location_name):
        geolocator = GoogleV3()
        loc = geolocator.geocode(location_name)

        return {
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'altitude': loc.altitude
        }

