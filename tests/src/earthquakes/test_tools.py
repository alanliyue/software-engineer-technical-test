import pytest
from earthquakes.tools import get_haversine_distance



@pytest.mark.parametrize("lat1, lon1, lat2, lon2, expected_distances", [
    ([35.025, 40.7128], [25.763, -74.0060], 35.0, 25.0, [0.0, 0.0]), 
])
def test_get_haversine_distance(mock_haversine_distance, lat1, lon1, lat2, lon2, expected_distances):
    distances = get_haversine_distance(lat1, lon1, lat2, lon2)
    assert distances == expected_distances