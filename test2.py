import datetime
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


import math
class Node:
    def __init__(self,coordinates,distance):
        self.coordinates=coordinates
        self.distance=distance
    
    def set_distance(self,distance):
        self.distance=distance

    def lt(self,other):
        return self.distance < other.distance
    
class Fire_Station:
    def __init__(self, name, geometry, zip_code, city, state, address, global_id, distance):
        self.name = name
        self.geometry = geometry
        self.zip_code = zip_code
        self.city = city
        self.state = state
        self.address = address
        self.global_id = global_id 
        self.distance=distance

    def set_distance(self,distance):
        self.distance=distance

    def lt(self,other):
        return self.distance < other.distance
    
def get_frames_by_zip_code_or_state(file_path, zip_code, state):
        start_time = datetime.datetime.now()
        print(f'Preprocessing Fire stations first..')
        # Read the GeoJSON file into a GeoDataFrame
        gdf = gpd.read_file(file_path)
        # Filter the GeoDataFrame based on the specified ZIP code
        frames_in_zip = gdf[gdf['ZIPCODE'] == zip_code]
        # Check the number of fire stations within the ZIP code
        if len(frames_in_zip) >= 2:
            print(f'Found {len(frames_in_zip)} fire stations in the specified ZIP code.')
            end_time = datetime.datetime.now() - start_time
            print(f'Done preprocessing... {end_time}')
            return frames_in_zip[['NAME', 'geometry', 'ZIPCODE', 'CITY', 'STATE', 'ADDRESS', 'GLOBALID']]
        # If less than 2 fire stations in the ZIP code, search by state
        frames_in_state = gdf[gdf['STATE'] == state]
        if not frames_in_state.empty:
            print(f'Found {len(frames_in_state)} fire stations in the specified state.')
            end_time = datetime.datetime.now() - start_time
            print(f'Done preprocessing... {end_time}')
            return frames_in_state[['NAME', 'geometry', 'ZIPCODE', 'CITY', 'STATE', 'ADDRESS', 'GLOBALID']]
        else:
            print(f'No fire stations found in the specified ZIP code or state.')
            end_time = datetime.datetime.now() - start_time
            print(f'Done preprocessing... {end_time}')
            return pd.DataFrame()  # Return empty DataFrame if no results found

def brute_force(fire_stations, starting_point):
    start_time = datetime.datetime.now()
    print(f'Finding nearest station..')
    distances=[]
    #brute force
    for i in fire_stations:
        total_distance=math.sqrt((i.geometry[1]-starting_point.coordinates[0])**2+(i.geometry[0]-starting_point.coordinates[1])**2)
        i.set_distance(total_distance)
        distances.append(i)
    minimum_point=min(distances, key=lambda x: x.distance)
    end_time=datetime.datetime.now()-start_time
    print(f'Station found ... {end_time}')
    return minimum_point, distances

#populate the list of nearby fire stations
def create_fire_stations(geodf):
    fire_stations = []
    inf=float('inf')

    for index, row in geodf.iterrows():
        name = row['NAME']
        geometry = tuple(row['geometry'].coords[0])  # Extracting the tuple from the geometry
        zip_code = row['ZIPCODE']
        city = row['CITY']
        state = row['STATE']
        address = row['ADDRESS']
        global_id = row['GLOBALID']
        fire_station = Fire_Station(name, geometry, zip_code, city, state, address, global_id,inf)
        fire_stations.append(fire_station)

        return fire_stations




def get_stations(starting_point,specified_state,specified_zip_code):
    file_path='Fire_Stations.geojson'
    # Get frames information for the specified ZIP code or state
    frames_info = get_frames_by_zip_code_or_state(file_path, specified_zip_code, specified_state)
    # Display the frames information
    print(frames_info)
    fire_stations= create_fire_stations(frames_info)
    closest_fire_station, other_stations=brute_force(fire_stations,starting_point)
    print(f'Closest fire station to disaster at {starting_point.coordinates} is {closest_fire_station.name},\nAt {closest_fire_station.address} with coords: {closest_fire_station.geometry}\n with distance:{closest_fire_station.distance}')
    return closest_fire_station
    
    # for j in other_stations:
    #     print(f'{j.name}, {j.address}, {j.distance}')

# #example code
# specified_zip_code = '30080'
# specified_state = 'GA'
# starting_point=Node((33.883647588413304, -84.49361801147461),0)
# target=get_stations(starting_point,specified_state,specified_zip_code)