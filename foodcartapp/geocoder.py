import requests
from geopy import distance

from django.conf import settings
from loguru import logger


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    try:
        response = requests.get(base_url, params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        })
        response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(e)
    else:
        found_places = response.json()['response']['GeoObjectCollection']['featureMember']

        if not found_places:
            return None

        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        return lon, lat


def calculate_distance(restaurant, client):
    api_key = settings.GEO_API_KEY
    restaurant_coords = fetch_coordinates(api_key, restaurant)
    client_coords = fetch_coordinates(api_key, client)

    if not all([restaurant_coords, client_coords]):
        return 100

    return distance.distance(restaurant_coords, client_coords).km