import requests


def api_connect():
  response = requests.get('https://data.cityofnewyork.us/resource/erm2-nwe9.json')

  response.raise_for_status()

  return response.json()
