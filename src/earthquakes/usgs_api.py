import urllib.request
import pandas as pd
from datetime import timedelta
import asyncio
import aiohttp
import time

def convert_data(x):
    try:
        return float(x)
    except:
        return float("NAN")
def build_api_url(end_date, latitude, longitude,  minimum_magnitude, radius_km):
    start_date = (end_date - timedelta(days=365*200)).strftime("%Y-%m-%d")
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    format_url = f"{base_url}?format=csv"
    start_date_url = f"&starttime={start_date}"
    end_date_url = f"&endtime={end_date.strftime('%Y-%m-%d')}"
    location_url = f"&latitude={latitude}&longitude={longitude}&maxradiuskm={radius_km}"
    minimum_magnitude_url = f"&minmagnitude={minimum_magnitude}"
    return format_url + start_date_url + end_date_url + minimum_magnitude_url + location_url

def get_earthquake_data(end_date, latitude, longitude, minimum_magnitude, radius):
    api_url = build_api_url(end_date, latitude, longitude, minimum_magnitude, radius)
    with urllib.request.urlopen(api_url) as response:
        data = response.read().decode('utf-8')
    
    str_list = data.split('\n')
    all_data_list = []
    for i in range(len(str_list)):
        if i != 0:
            temp_list = str_list[i].split(',')
            temp_list = temp_list[0:13] + [','.join(temp_list[13:15]).replace('"','')] + temp_list[15:]
        else:
            temp_list = str_list[i].split(',')
        all_data_list.append(temp_list)
    all_df = pd.DataFrame(all_data_list[1:-1])
    all_df.columns = all_data_list[0]


        
    for col in ['latitude', 'longitude', 'depth', 'mag', 'nst', 'gap', 'dmin', 'rms', 'horizontalError', 'depthError', 'magError', 'magNst']:
        all_df[col] = all_df[col].apply(lambda x:convert_data(x))

    return all_df

async def fetch_earthquake_data(session, url):
    async with session.get(url) as response:
        return await response.text()

async def process_location(session, location, radius, minimum_magnitude, end_date):
    latitude, longitude = location
    url = build_api_url(end_date=end_date,
                        latitude=latitude,
                        longitude=longitude,
                        minimum_magnitude=minimum_magnitude,
                        radius_km=radius)
    earthquake_data = await fetch_earthquake_data(session, url)

    str_list = earthquake_data.split('\n')
    if(str_list[1] !=''):
        all_data_list = []
        for i in range(len(str_list)):
            if i != 0:
                temp_list = str_list[i].split(',')
                temp_list = temp_list[0:13] + [','.join(temp_list[13:15]).replace('"','')] + temp_list[15:]
            else:
                temp_list = str_list[i].split(',')
            all_data_list.append(temp_list)
        all_df = pd.DataFrame(all_data_list[1:-1])
        all_df.columns = all_data_list[0]
            
        for col in ['latitude', 'longitude', 'depth', 'mag', 'nst', 'gap', 'dmin', 'rms', 'horizontalError', 'depthError', 'magError', 'magNst']:
            all_df[col] = all_df[col].apply(lambda x:convert_data(x)) 
        return all_df

async def get_earthquake_data_for_multiple_locations(locations, radius, minimum_magnitude, end_date):
    async with aiohttp.ClientSession() as session:
        tasks = [process_location(session, location, radius, minimum_magnitude, end_date) for location in locations]
        earthquake_data_list = await asyncio.gather(*tasks)
        return earthquake_data_list


