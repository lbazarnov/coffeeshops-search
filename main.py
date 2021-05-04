import json
import requests
from geopy import distance
import folium

apikey = '2165c418-0c63-4111-8bfe-a6d7531cdb24'
user_location = input('Где вы находитесь?\n')

with open('coffee.json', 'r', encoding='CP1251') as my_file:
    file_content = my_file.read()

coffeeshops = json.loads(file_content)

# функция получения координат места по его названию


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


user_coordinates = fetch_coordinates(apikey, user_location)

# получаем название, долготу и широту кофеен
coffeeshops_list = []
for coffeeshop in coffeeshops:

    coffeeshop_dict = {}

    coffeeshop_title = coffeeshop['Name']
    coffeeshop_longtitude = coffeeshop['Longitude_WGS84']
    coffeeshop_latitude = coffeeshop['Latitude_WGS84']
    coffeeshop_coordinates = [coffeeshop_latitude, coffeeshop_longtitude]
    distance_to_coffeeshop = distance.distance(
        user_coordinates, coffeeshop_coordinates).km

    coffeeshop_dict['title'] = coffeeshop_title
    coffeeshop_dict['distance'] = distance_to_coffeeshop
    coffeeshop_dict['longtitude'] = coffeeshop_longtitude
    coffeeshop_dict['latitude'] = coffeeshop_latitude

    coffeeshops_list.append(coffeeshop_dict)


def get_distance_to_coffeeshop(coffeeshops_list):
    return coffeeshops_list['distance']


print(f'Ваши координаты: {user_coordinates}')
nearby_coffeeshops = sorted(
    coffeeshops_list, key=get_distance_to_coffeeshop)[:5]

coffeeshops_map = folium.Map(location=user_coordinates, zoom_start=16)

for coffeeshop_index in range(5):
    folium.Marker(
        location=[nearby_coffeeshops[coffeeshop_index]['latitude'],
                  nearby_coffeeshops[coffeeshop_index]['longtitude']],
        popup=nearby_coffeeshops[coffeeshop_index]['title'],
        icon=folium.Icon(icon='coffee', prefix='fa', color='red')
    ).add_to(coffeeshops_map)

coffeeshops_map.save('map.html')
