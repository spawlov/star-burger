import requests
from geopy import distance


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    try:
        response = requests.get(base_url, params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        })
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return e
    else:
        found_places = response.json()['response']['GeoObjectCollection'][
            'featureMember']

        if not found_places:
            return response

        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        return lon, lat


def calc_distance(restaurant, client):
    api_key = 'e99634f6-ec6c-49fb-900d-b4112b1adb45'
    return distance.distance(
        fetch_coordinates(api_key, restaurant),
        fetch_coordinates(api_key, client)
    ).km
