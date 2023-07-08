from math import sin, cos, sqrt, atan2, radians
import pandas as pd
from custom_libs import db
from custom_libs import classification


def get_closest_restaurants(df, current_position, max_distance):
    """Takes a dataframe, array of current position, max distance and returns a dataframe
       with the points of interest that are within the max distance from the current position"""
    selected_points = []

    # Approximate radius of the Earth in kilometers
    earth_radius = 6371.0

    # Current coords
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
        a = sin(d_lat / 2)**2 + cos(current_lat_rad) * \
            cos(poi_lat_rad) * sin(d_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = earth_radius * c

        # Check if the distance is within the maximum distance
        if distance <= max_distance:
            selected_points.append(row)

    # If the list is empty return an empty dataframe
    if selected_points == []:
        return df.drop(df.index[:])

    # Else return the dataframe with the selected points
    df_points = pd.DataFrame(selected_points)
    return df_points.drop(df_points.columns[0], axis=1)


def get_best_rated_restaurant(df):
    """Takes a dataframe with point of interest and returns the restaurant with the best rating"""
    df_app = df.groupby('id')['rating_number'].mean()
    df_app.sort_values(ascending=False)

    id = df_app.index[0]

    result = df.loc[df['id'] == id, [
        'store_address', 'latitude', 'longitude', 'id']]

    return result.groupby('id').first()


def get_best_sentiment_restaurant(df):
    count_df = df.groupby(['id', 'sentiment']).size().unstack(fill_value=0)

    # Rename the columns for better clarity
    count_df.columns = classification.Sentiment.get_all()

    # Reset the index to make 'id' a regular column
    count_df = count_df.reset_index()

    # Calculate the total reviews for each ID
    count_df['Total'] = count_df['Negative'] + \
        count_df['Neutral'] + count_df['Positive']

    # Divide Positive, Neutral, and Negative columns by Total
    count_df['Positive'] = count_df['Positive'] / count_df['Total']
    count_df['Neutral'] = count_df['Neutral'] / count_df['Total']
    count_df['Negative'] = count_df['Negative'] / count_df['Total']

    # Sort the dataframe by 'Positive' column in descending order
    sorted_df = count_df.sort_values(by='Positive', ascending=False)

    # Select the restaurant with the highest positive rating percentage
    best_restaurant_id = sorted_df.iloc[0]['id']

    result = df.loc[df['id'] == best_restaurant_id, [
        'store_address', 'latitude', 'longitude', 'id']]

    return result.groupby('id').first()


def select_best_restaurant_from_stars(df, current_position, max_distance):
    closest_restaurants = get_closest_restaurants(
        df, current_position, max_distance)
    if closest_restaurants.empty:
        raise Exception("No restaurant found")
    return get_best_rated_restaurant(closest_restaurants)


def select_best_restaurant_from_sentiment(df, current_position, max_distance):
    closest_restaurants = get_closest_restaurants(
        df, current_position, max_distance)
    if closest_restaurants.empty:
        raise Exception("No restaurant found")
    return get_best_sentiment_restaurant(closest_restaurants)


def best_restaurant_from_stars_reply(current_position, max_distance):
    df = db.get_dataset('McDonald_s_Reviews_preprocessed')
    try:
        best_restaurant_df = select_best_restaurant_from_stars(
            df, current_position, max_distance)
        return best_restaurant_df['store_address'].values[0]
    except Exception as e:
        return str(e)


def best_restaurant_from_sentiment_reply(current_position, max_distance):
    df = db.get_dataset('McDonald_s_Reviews_preprocessed')
    try:
        best_restaurant_df = select_best_restaurant_from_sentiment(
            df, current_position, max_distance)
        return best_restaurant_df['store_address'].values[0]
    except Exception as e:
        return str(e)
