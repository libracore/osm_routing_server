# osm_routing_server
Simple project to create a Python-based OSM routing server (API)

This software is free and open source and comes with no warranty as-is.

The maps used are from OpenStreetMaps: https://openstreetmaps.org

# Dependencies
Make sure to have this installed

    # pip install flask
    # pip install flask_restful
    # pip install waitress
    # pip install osmnx
    # pip install pyrosm
    # pip install scikit-learn

# Create the server
* Clone the repo
* Install the dependencies
* Adapt configuration as required
* Run standalone as

    python routing_server.py
    
* or as a service using the linux service file: 
    * copy the osm_routing_server.service to /etc/systemd/system/osm_routing_server.service
    * modify the ExecStart to the cloned routing_server.py
    * reload systemd deamon: $ sudo systemctl daemon-reload
    * enable the service: $ sudo systemctl enable osm_routing_server.service
    * start service: $ sudo systemctl start osm_routing_server.service
    * check status with: $ sudo systemctl status osm_routing_server.service
    * stop service with: $ sudo systemctl stop osm_routing_server.service
    
# Usage
Call the API like this

    http://127.0.0.1:5002/routing/<from_lat>/<from_long>/<to_lat>/<to_long>
    http://127.0.0.1:5002/routing/47.6566683/8.693854/47.6380233/8.6952064

and you get the distance and travel time

    {"data": 
        {
            "distance_in_kilometers": 2.362132, 
            "travel_time": "0:02:36.300000"
        }
    }
    
