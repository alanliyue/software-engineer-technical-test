from math import radians, cos, sin, asin, sqrt
import pandas as pd

EARTH_RADIUS = 6378

TIME_COLUMN = "time"
PAYOUT_COLUMN = "payout"
MAGNITUDE_COLUMN = "mag"
DISTANCE_COLUMN = "distance"
LATITUDE_COLUMN = "latitude"
LONGITUDE_COLUMN = "longitude"

def haversine_distance(lat1, lon1, lat2, lon2):
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = EARTH_RADIUS 
    
    return c * r


def get_haversine_distance(lat1, lon1, lat2, lon2):
    lat1_list = list(lat1)
    lon1_list = list(lon1)
    distance_list = []
    for i in range(len(lat1_list)):
        lat_1, lon_1 = lat1_list[i], lon1_list[i]
        dist = haversine_distance(lat_1, lon_1, lat2, lon2)
        distance_list.append(dist)
    
    return distance_list

def compute_payouts(earthquake_data, payout_structure):
    mag_list, dis_list = list(earthquake_data['mag']), list(earthquake_data['distance'])
    payout_list = []
    for i in range(len(mag_list)):
        payout_found = False
        for index, row in payout_structure.iterrows():
            if mag_list[i] >= float(row['Magnitude']) and dis_list[i] <= float(row['Radius'][:-2]):
                payout_list.append(float(row['Payout'][:-1]))
                payout_found = True 
                continue
        if not payout_found:
             payout_list.append(0)

    temp_df = pd.DataFrame()
    temp_df['time'] = earthquake_data['time']
    temp_df['payout'] = pd.DataFrame(payout_list)
    temp_df['year'] = temp_df['time'].apply(lambda x:x.split('-')[0])
    payouts_result = temp_df.groupby('year')['payout'].max().to_dict()
    return payouts_result

def compute_burning_cost(payouts, start_year, end_year):
    total_payouts = 0
    for key in list(payouts.keys()):
        if int(key) >= start_year and int(key) <= end_year:
            total_payouts += payouts[key]
    nb_years = (end_year-start_year+1)
    return total_payouts / nb_years

