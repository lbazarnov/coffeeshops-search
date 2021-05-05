import json
import requests
from geopy import distance
import folium
from flask import Flask

NEAREST_BARS_AMOUNT = 5


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


def get_distance_to_coffeeshop(coffeeshops_list):
    return coffeeshops_list['distance']


def render_map():
    with open('map.html') as file:
        return file.read()


def main():
    with open('coffee.json', 'r', encoding='CP1251') as my_file:
        file_content = my_file.read()

    coffeeshops = json.loads(file_content)
    apikey = '2165c418-0c63-4111-8bfe-a6d7531cdb24'
    user_location = input('Где вы находитесь?\n')
    user_coordinates = fetch_coordinates(apikey, user_location)

    coffeeshops_list = []
    for coffeeshop in coffeeshops:
        coffeeshop_title = coffeeshop['Name']
        coffeeshop_longtitude = coffeeshop['Longitude_WGS84']
        coffeeshop_latitude = coffeeshop['Latitude_WGS84']
        coffeeshop_coordinates = [coffeeshop_latitude, coffeeshop_longtitude]
        distance_to_coffeeshop = distance.distance(
            user_coordinates, coffeeshop_coordinates).km

        coffeeshop_dict = {
            'title': coffeeshop_title,
            'distance': distance_to_coffeeshop,
            'longtitude': coffeeshop_longtitude,
            'latitude': coffeeshop_latitude
        }

        coffeeshops_list.append(coffeeshop_dict)

    nearby_coffeeshops = sorted(
        coffeeshops_list, key=get_distance_to_coffeeshop)[:NEAREST_BARS_AMOUNT]

    coffeeshops_map = folium.Map(location=user_coordinates, zoom_start=16)

    for nearby_coffeeshop in nearby_coffeeshops:
        folium.Marker(
            location=[nearby_coffeeshop['latitude'],
                      nearby_coffeeshop['longtitude']],
            popup=nearby_coffeeshop['title'],
            icon=folium.Icon(icon='coffee', prefix='fa', color='red')
        ).add_to(coffeeshops_map)

    coffeeshops_map.save('map.html')

    app = Flask(__name__)
    app.add_url_rule('/', 'Moscow Coffeshops Map', render_map)
    app.run('0.0.0.0')


if __name__ == '__main__':
    main()
