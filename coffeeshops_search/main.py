import json
import requests
import folium
import os
from dotenv import load_dotenv
from geopy import distance
from flask import Flask

NEAREST_BARS_AMOUNT = 5
HTML_MAP = 'map.html'


def load_file(file):
    with open(file, 'r', encoding='CP1251') as json_file:
        file_content = json_file.read()
    return json.loads(file_content)


def fetch_coordinates(apikey, place):
    base_url = 'https://geocode-maps.yandex.ru/1.x'
    params = {'geocode': place, 'apikey': apikey, 'format': 'json'}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    found_places = response.json(
    )['response']['GeoObjectCollection']['featureMember']
    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')
    return lat, lon


def get_coffeeshops_coordinates(coffeeshops_list, user_coordinates):
    coffeeshops = []

    for coffeeshop in coffeeshops_list:
        coffeeshop_title = coffeeshop['Name']
        coffeeshop_longtitude = coffeeshop['Longitude_WGS84']
        coffeeshop_latitude = coffeeshop['Latitude_WGS84']
        coffeeshop_coordinates = [coffeeshop_latitude, coffeeshop_longtitude]
        distance_to_coffeeshop = distance.distance(user_coordinates,
                                                   coffeeshop_coordinates).km
        coffeeshop_details = {
            'title': coffeeshop_title,
            'distance': distance_to_coffeeshop,
            'longtitude': coffeeshop_longtitude,
            'latitude': coffeeshop_latitude
        }

        coffeeshops.append(coffeeshop_details)

    return coffeeshops


def get_distance_to_coffeeshop(coffeeshop):
    return coffeeshop['distance']


def get_nearby_coffeeshops(coffeeshops_data):
    nearby_coffeeshops = sorted(
        coffeeshops_data, key=get_distance_to_coffeeshop)[:NEAREST_BARS_AMOUNT]

    return nearby_coffeeshops


def get_markers_on_map(user_coordinates, nearby_coffeeshops):
    coffeeshops_map = folium.Map(location=user_coordinates, zoom_start=16)

    folium.Marker(location=user_coordinates,
                  popup='Ваше местоположение',
                  icon=folium.Icon(icon='user', prefix='fa',
                                   color='green')).add_to(coffeeshops_map)

    for nearby_coffeeshop in nearby_coffeeshops:
        folium.Marker(location=[
            nearby_coffeeshop['latitude'], nearby_coffeeshop['longtitude']
        ],
            popup=nearby_coffeeshop['title'],
            icon=folium.Icon(icon='coffee', prefix='fa',
                             color='red')).add_to(coffeeshops_map)

    return coffeeshops_map.save(HTML_MAP)


def render_map():
    with open(HTML_MAP) as file:
        return file.read()


def run_webserver(host='0.0.0.0', port=5000):
    app = Flask(__name__)
    app.add_url_rule('/', 'Moscow Coffeshops Map', render_map)
    app.run(host=host, port=port)


def main():
    load_dotenv()
    api_key = os.getenv('APIKEY')
    user_location = input('Введите ваше местоположение: ')
    user_coordinates = fetch_coordinates(api_key, user_location)
    coffeeshops_list = load_file('coffee.json')
    coffeeshops = get_coffeeshops_coordinates(coffeeshops_list, user_coordinates)  # noqa: 501
    nearby_coffeeshops = get_nearby_coffeeshops(coffeeshops)
    get_markers_on_map(user_coordinates, nearby_coffeeshops)
    run_webserver()


if __name__ == '__main__':
    main()
