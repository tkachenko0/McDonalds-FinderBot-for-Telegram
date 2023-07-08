from math import sin, cos, sqrt, atan2, radians
import pandas as pd
from custom_libs import classification


def get_closest_restaurants(df, current_position, max_distance):
    selected_points = []
    earth_radius = 6371.0

    current_latitude = current_position[0]
    current_longitude = current_position[1]

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
        a = sin(d_lat / 2)**2 + cos(current_lat_rad) * \
            cos(poi_lat_rad) * sin(d_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = earth_radius * c

        # Check if the distance is within the maximum distance
        if distance <= max_distance:
            selected_points.append(row)

    if selected_points == []:
        return df.drop(df.index[:])

    df_points = pd.DataFrame(selected_points)
    return df_points.drop(df_points.columns[0], axis=1)


def select_best_restaurant_from_stars(df, current_position, max_distance):
    closest_restaurants = get_closest_restaurants(
        df, current_position, max_distance)
    
    if closest_restaurants.empty:
        raise Exception("No restaurant found")
    
    df_app = closest_restaurants.groupby('id')['rating_number'].mean()
    df_app.sort_values(ascending=False)
    id = df_app.index[0]

    result = df.loc[df['id'] == id, ['store_address', 'latitude', 'longitude', 'id']]

    return result.groupby('id').first()

def select_best_restaurant_from_sentiment(df, current_position, max_distance, sentiment_column='sentiment'):
    closest_restaurants = get_closest_restaurants(
        df, current_position, max_distance)
    
    if closest_restaurants.empty:
        raise Exception("No restaurant found")

    count_df = closest_restaurants.groupby(['id', sentiment_column]).size().unstack(fill_value=0)

    count_df.columns = classification.Sentiment.get_all()
    count_df = count_df.reset_index()

    count_df['Total'] = count_df['Negative'] + count_df['Neutral'] + count_df['Positive']
    count_df['Positive'] = count_df['Positive'] / count_df['Total']
    count_df['Neutral'] = count_df['Neutral'] / count_df['Total']
    count_df['Negative'] = count_df['Negative'] / count_df['Total']

    count_df['Score'] = ((count_df['Positive']*(1)) + (count_df['Neutral'] * (0)) + (count_df['Negative']*(-2))) / count_df['Total']

    sorted_df = count_df.sort_values(by='Score', ascending=False)
    best_restaurant_id = sorted_df.iloc[0]['id']
    result = df.loc[df['id'] == best_restaurant_id, ['store_address', 'latitude', 'longitude', 'id']]

    return result.groupby('id').first()