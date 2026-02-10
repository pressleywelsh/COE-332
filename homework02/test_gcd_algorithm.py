from gcd_algorithm import great_circle_distance
import pytest


def test_great_circle_distance():
    assert great_circle_distance(50.775, 6.08333, 56.18333, 10.23333, 6371) == 660.8248602419454
    assert great_circle_distance(54.21667, -113.0, 16.88333, -99.9, 6371) == 4301.925195956915

def test_great_circle_distance_exceptions():
    assert great_circle_distance(50.775, 6.08333, 50.775, 6.08333, 6371) == 0
    with pytest.raises(AttributeError):
        great_circle_distance(54.21667, -113.0, 16.88333, "foo", 6371)
