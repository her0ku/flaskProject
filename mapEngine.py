import openrouteservice
from openrouteservice import convert
import json
import requests
import folium
import os


def calculate_route(route1, route2):
    #coords = ((37.724291, 55.797326), (37.723913, 55.798299))
    #coords = ((37.763445, 55.805075), (37.763336, 55.806007))
    path = os.path.join(os.path.abspath(os.path.dirname('templates/')), 'results.html')
    #os.remove(path)
    coords = (route1, route2)
    lat = coords[0][0]
    len = coords[0][1]
    client = openrouteservice.Client(key='5b3ce3597851110001cf6248d6500bcd34974596b5f7055a5aad3e8d')
    routes = client.directions(coords, profile='wheelchair', optimize_waypoints=True, format='geojson')
    map_directions = folium.Map(location=[len, lat], zoom_start=17)
    folium.GeoJson(routes, name='route').add_to(map_directions)
    folium.LayerControl().add_to(map_directions)
    map_directions.save('templates/results.html')


def add_custom_mark(data):
    map_code = folium.Map(location=[55.797326, 37.724291], zoom_start=17)
    for i in data:
        folium.Marker(location=(i[5], i[6]), icon=folium.Icon(icon='building', color='green', prefix='fa'),
                        popup=folium.Popup('Тип: ' + i[3] + '\nКомментарий: ' + i[2])).add_to(map_code)
    map_code.save('templates/marks.html')
#es = requests.get('https://maps.openrouteservice.org/#/directions/%D0%9C%D1%8F%D1%81%D0%BD%D0%BE%D0%B2%D1%8A,%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0,MS,%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F/%D0%B4%D0%BE%D0%BC%2010,%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81%201,%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BD%D0%B8%D0%B5%201%20%D0%91%D0%BE%D0%BB%D1%8C%D1%88%D0%B0%D1%8F%20%D0%A7%D0%B5%D1%80%D0%BA%D0%B8%D0%B7%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%A3%D0%BB%D0%B8%D1%86%D0%B0,%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0,MS,%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F')
#print(res.text)
#json_res = res.json()
#for i in json_res['features']:
#    for n in i['geometry']['coordinates']:
#        print(n)