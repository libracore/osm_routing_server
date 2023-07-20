# -*- coding: utf-8 -*-
# Copyright (c) 2023, libracore and contributors
# For license information, please see LICENSE
#
# This creates a simple routing server based on OpenStreetMaps
#
# Use the API like
#
#   http://127.0.0.1:5002/routing/<from_lat>/<from_long>/<to_lat>/<to_long>
#    http://127.0.0.1:5002/routing/47.6566683/8.693854/47.6380233/8.6952064
#
# See README for dependencies

from flask import Flask, request
from flask_restful import Resource, Api
import osmnx as ox
import networkx as nx
from datetime import timedelta
import os

HOST = "127.0.0.1"
PORT = 5002
MAP = "Switzerland"

### preparing the rounting app
graph_area = (MAP)
graph_temp_file = "{0}.graphml".format(MAP)

ox.settings.use_cache=True
ox.settings.cache_folder='./cache'

if not os.path.exists(graph_temp_file):
    print("creating graph...")
    # Create the graph of the area from OSM data. It will download the data and create the graph
    G = ox.graph_from_place(graph_area, network_type='drive')

    # OSM data are sometime incomplete so we use the speed module of osmnx to add missing edge speeds and travel times
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    # Save graph to disk if you want to reuse it
    ox.save_graphml(G, graph_temp_file)
else:
    print("loading graph...")
    G = ox.io.load_graphml(graph_temp_file)

print("creating server...")
### create server
app = Flask(__name__)
api = Api(app)

print("load routing...")
class routing(Resource):
    def get(self, from_lat, from_long, to_lat, to_long):
        # In the graph, get the nodes closest to the points
        origin_node = ox.nearest_nodes(G, Y=float(from_lat), X=float(from_long))
        destination_node = ox.nearest_nodes(G, Y=float(to_lat), X=float(to_long))

        # Get the travel time, in seconds
        travel_time_in_seconds = nx.shortest_path_length(G, origin_node, destination_node, weight='travel_time')
        #The travel time in "HOURS:MINUTES:SECONDS" format
        travel_time_in_hours_minutes_seconds = str(timedelta(seconds=travel_time_in_seconds))

        # Get the distance in meters
        distance_in_meters = nx.shortest_path_length(G, origin_node, destination_node, weight='length')
        # Distance in kilometers
        distance_in_kilometers = distance_in_meters / 1000
        return {
            'data': {
                'distance_in_kilometers': distance_in_kilometers,
                'travel_time': travel_time_in_hours_minutes_seconds
            }
        }
        
api.add_resource(routing, '/routing/<from_lat>/<from_long>/<to_lat>/<to_long>')

if __name__ == '__main__':
    from waitress import serve
    print("listening on {0}:{1}".format(HOST, PORT))
    serve(app, host=HOST, port=PORT)
    
