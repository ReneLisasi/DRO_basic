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
    
def preprocess(file_path):
    print(f'Preprocessing Fire stations first..')
    start_time = datetime.datetime.now()
    
    # Read the GeoJSON file into a GeoDataFrame
    gdf = gpd.read_file(file_path)
    end_time = datetime.datetime.now() - start_time

    print(f'Done preprocessing... {end_time}')
    return gdf

file_path='Fire_Stations.geojson'
gdf=preprocess(file_path)
    
def get_frames_by_zip_code_or_state(zip_code, state,gdf):
        start_time = datetime.datetime.now()
        print(f'SIfting through json by zipcode/state..')
        # # Read the GeoJSON file into a GeoDataFrame
        # gdf = gpd.read_file(file_path)
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
            print(f'Done sifting... {end_time}')
            return pd.DataFrame()  # Return empty DataFrame if no results found



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



def bubble_sort(unordered_list):
    iteration_number = len(unordered_list)-1
    for i in range(iteration_number,0,-1):
        for j in range(i):
            if unordered_list[j].distance > unordered_list[j+1].distance:
                temp = unordered_list[j]
                unordered_list[j] = unordered_list[j+1]
                unordered_list[j+1] = temp
    return unordered_list



def merge(first_sublist, second_sublist): 
    i = j = 0
    merged_list = []
    while i < len(first_sublist) and j < len(second_sublist):
        if first_sublist[i].distance < second_sublist[j].distance:
            merged_list.append(first_sublist[i]) 
            i += 1 
        else:
            merged_list.append(second_sublist[j]) 
            j += 1
    while i < len(first_sublist): 
        merged_list.append(first_sublist[i]) 
        i += 1 
    while j < len(second_sublist):
        merged_list.append(second_sublist[j]) 
        j += 1
    return merged_list 

def merge_sort(unsorted_list):
    if len(unsorted_list) == 1: 
        return unsorted_list
    mid_point = int(len(unsorted_list)/2)
    first_half = unsorted_list[:mid_point] 
    second_half = unsorted_list[mid_point:] 
    half_a = merge_sort(first_half) 
    half_b = merge_sort(second_half) 
    return merge(half_a, half_b) 

def selection_sort(unsorted_list): 
    size_of_list = len(unsorted_list) 
    for i in range(size_of_list): 
        small = i
        for j in range(i+1, size_of_list): 
            if unsorted_list[j].distance < unsorted_list[small].distance: 
                small = j
        temp = unsorted_list[i] 
        unsorted_list[i] = unsorted_list[small] 
        unsorted_list[small] = temp
    return unsorted_list

def brute_force(fire_stations, starting_point,sorting_algorithm):
    start_time = datetime.datetime.now()
    print(f'Finding nearest station..')
    stations=[]

    #brute force collection of distances for every available node
    for i in fire_stations:
        total_distance=math.sqrt((i.geometry[1]-starting_point.coordinates[0])**2+(i.geometry[0]-starting_point.coordinates[1])**2)
        i.set_distance(total_distance)
        stations.append(i)

    print(f'Sorting using {sorting_algorithm}_sort')
    sort_start_time=datetime.datetime.now()
    #choose your fighter:
    if sorting_algorithm=='merge':
        ordered_list=merge_sort(stations)
    elif sorting_algorithm=='selection':
        ordered_list=selection_sort(stations)
    elif sorting_algorithm=='bubble':
        ordered_list=bubble_sort(stations)
    sort_end_time=datetime.datetime.now()-sort_start_time
    print(f'Done sorting, time taken to {sorting_algorithm}_sort was {sort_end_time}')

    #get the minimum distanced node
    minimum_point=ordered_list[0]
    end_time=datetime.datetime.now()-start_time
    print(f'Station found ... {end_time}')
    return minimum_point, stations

def get_stations(starting_point,specified_state,specified_zip_code,sorting_algorithm):
    # Get frames information for the specified ZIP code or state
    frames_info = get_frames_by_zip_code_or_state(specified_zip_code, specified_state,gdf)
    # Display the frames information
    print(frames_info)
    fire_stations= create_fire_stations(frames_info)
    closest_fire_station, other_stations=brute_force(fire_stations,starting_point,sorting_algorithm)
    print(f'Closest fire station to disaster at {starting_point.coordinates} is {closest_fire_station.name},\nAt {closest_fire_station.address} with coords: {closest_fire_station.geometry}\n with distance:{closest_fire_station.distance}')
    return closest_fire_station
    
    # for j in other_stations:
    #     print(f'{j.name}, {j.address}, {j.distance}')

# #example code
# specified_zip_code = '30080'
# specified_state = 'GA'
# starting_point=Node((33.883647588413304, -84.49361801147461),0)
# target=get_stations(starting_point,specified_state,specified_zip_code,'selection')

