import geopandas as gpd
import pandas as pd
import math
import time
# Function to get coordinates by ZIP code, and if none are found, by city
def get_coordinates_by_zip_then_city_gdf(gdf, zip_code):
    coordinates_by_zip = gdf[gdf['ZIPCODE'] == zip_code]
    if not coordinates_by_zip.empty:
        return coordinates_by_zip[['ZIPCODE', 'CITY', 'geometry']]
    else:
        cities = gdf[gdf['ZIPCODE'] == zip_code]['CITY'].unique()
        if cities.size > 0:
            city = cities[0]
            coordinates_by_city = gdf[gdf['CITY'] == city]
            return coordinates_by_city[['ZIPCODE', 'CITY', 'geometry']]
        else:
            return pd.DataFrame()
# Load the GeoJSON file
start_preprocessing_time = time.time()
file_path_geojson = 'D:\Presence_Abscence_Data\Final_Outputs\Fire_Stations.geojson'  # Replace with your file path
fire_stations_gdf = gpd.read_file(file_path_geojson)
# Get coordinates for a specific ZIP code
placeholder_zip_code = '30080'  # Replace with the ZIP code you want to query
coordinates_df = get_coordinates_by_zip_then_city_gdf(fire_stations_gdf, placeholder_zip_code)
# Extracting coordinates and removing duplicates
points_with_info = [(row['ZIPCODE'], row['CITY'], (row.geometry.x, row.geometry.y)) for index, row in coordinates_df.iterrows()]
unique_points_dict = {info[2]: (info[0], info[1]) for info in points_with_info}
unique_points = list(unique_points_dict.keys())
end_preprocessing_time = time.time()
# Closest pair algorithm functions
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
def brute_force_closest_pair(points):
    min_dist = float('inf')
    closest_pair = None
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                closest_pair = (points[i], points[j])
    return closest_pair
def sort_points_by_x(points):
    return sorted(points, key=lambda point: point[0])
def closest_pair_in_strip(strip, d):
    min_d = d
    closest_pair = None
    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if strip[j][1] - strip[i][1] < min_d:
                distance = euclidean_distance(strip[i], strip[j])
                if distance < min_d:
                    min_d = distance
                    closest_pair = (strip[i], strip[j])
    return closest_pair if closest_pair else (None, None)
def closest_pair_recursive(points_sorted_by_x):
    n = len(points_sorted_by_x)
    if n <= 3:
        return brute_force_closest_pair(points_sorted_by_x)
    mid = n // 2
    left_half = points_sorted_by_x[:mid]
    right_half = points_sorted_by_x[mid:]
    left_closest_pair = closest_pair_recursive(left_half)
    right_closest_pair = closest_pair_recursive(right_half)
    min_pair = min(left_closest_pair, right_closest_pair, key=lambda pair: euclidean_distance(pair[0], pair[1]) if pair[0] and pair[1] else float('inf'))
    mid_x = points_sorted_by_x[mid][0]
    dist = euclidean_distance(min_pair[0], min_pair[1]) if min_pair[0] and min_pair[1] else float('inf')
    strip = [point for point in points_sorted_by_x if abs(point[0] - mid_x) < dist]
    if strip:
        strip_closest_pair = closest_pair_in_strip(strip, dist)
        if strip_closest_pair[0] and strip_closest_pair[1]:
            min_pair = min(min_pair, strip_closest_pair, key=lambda pair: euclidean_distance(pair[0], pair[1]))
    return min_pair
def closest_pair(points):
    points_sorted_by_x = sort_points_by_x(points)
    return closest_pair_recursive(points_sorted_by_x)
start_algorithm_time = time.time()
closest_pair_result = closest_pair(unique_points)
end_algorithm_time = time.time()
# Print processing times
preprocessing_time = end_preprocessing_time - start_preprocessing_time
algorithm_time = end_algorithm_time - start_algorithm_time
print("Time for preprocessing: {:.2f} seconds".format(preprocessing_time))
print("Time for running the algorithm: {:.2f} seconds".format(algorithm_time))
print("Closest Pair of Fire Stations:", closest_pair_result)

