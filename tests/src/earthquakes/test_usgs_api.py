from datetime import datetime, timedelta
import pytest
from earthquakes.usgs_api import build_api_url

@pytest.mark.parametrize("end_date, latitude, longitude, minimum_magnitude, radius_km, expected_url", [
    (datetime(2023, 8, 16), 35.025, 25.763, 4.5, 200, "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=1823-08-16&endtime=2023-08-16&minmagnitude=4.5&latitude=35.025&longitude=25.763&maxradiuskm=200"),
])
def test_build_api_url(end_date, latitude, longitude, minimum_magnitude, radius_km, expected_url):
    generated_url = build_api_url(end_date, latitude, longitude, minimum_magnitude, radius_km)
    assert generated_url == expected_url