from math import sin, cos, sqrt, atan2, radians
import pandas as pd

#comments in python start with a hash
#this is a function that takes a dataframe, array of current position, max distance and returns a dataframe 
#with the points of interest that are within the max distance from the current position
def select_points_of_interest(df,current_position, max_distance):
    selected_points = []
    
    # Approximate radius of the Earth in kilometers
    earth_radius = 6371.0
    
    #current coords
    current_latitude = current_position[0] 
    current_longitude = current_position[1]
    
    # Convert current latitude and longitude to radians
    current_lat_rad = radians(current_latitude)
    current_lon_rad = radians(current_longitude)
    
    for row in df.itertuples():
       
        poi_lat = float(row[df.columns.get_loc("latitude")+1])
        poi_lon = float(row[df.columns.get_loc("longitude")+1])
        
        # Convert point of interest latitude and longitude to radians
        poi_lat_rad = radians(poi_lat)
        poi_lon_rad = radians(poi_lon)
        
        # Calculate the difference between the latitudes and longitudes
        d_lat = poi_lat_rad - current_lat_rad
        d_lon = poi_lon_rad - current_lon_rad
        
        # Haversine formula to calculate the distance between two points on the Earth's surface
        a = sin(d_lat / 2)**2 + cos(current_lat_rad) * cos(poi_lat_rad) * sin(d_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = earth_radius * c
        
        # Check if the distance is within the maximum distance
        if distance <= max_distance:
            selected_points.append(row)
    
    #if the list is empty return an empty dataframe
    if selected_points == []:
        return df.drop(df.index[:])
    
    #else return the dataframe with the selected points
    df_points = pd.DataFrame(selected_points) 
    return df_points.drop(df_points.columns[0], axis=1)  


#function that takes a dataframe with point of interest and returns the id 
# of the restaurant with the best rating
def get_id_restaurant_best_rated(df):
   
    #if the dataframe is empty return -1
    if df.empty:
        return -1
    
    #else return the id of the restaurant with the best rating
    df_app = df.copy()
    df_app = df_app.groupby('id')['rating_number'].mean()
    df_app.sort_values(ascending=False)

    return df_app.index[0]


#function that takes a dataframe with point of interest 
# and returns the restaurant with the best rating
def get_restaurant_best_rated(df):
    id = get_id_restaurant_best_rated(df)
    if id == -1:
        return 'no restaurant found'
    
    result = df.loc[df['id'] == id, ['store_address','latitude','longitude', 'id']]
   
    return result.groupby('id').first()