import math


def great_circle_distance(lat1, long1, lat2, long2, r):
    """
    Given the latitude and logitude of two landing sites,
    calculates and returns the distance between the two landing sites using the great circle distance formula.

    Args: 
        lat1: latitude of the first landing (float)
        long1: longitude of the first landing (float)
        lat2: latitude of the second landing (float)
        long2: longitude of the second landing (float)
        r: radius of the planet the meteorite lands on (float)

    Returns: 
        dist: the distance between the two meteorite landings (float)
    """
    latrad1 = lat1 * (math.pi / 180)
    latrad2 = lat2 * (math.pi / 180)
    longrad1 = long1 * (math.pi / 180)
    longrad2 = long2 * (math.pi / 180)
    lawcos = math.acos(
            (math.sin(latrad1) * math.sin(latrad2)) 
            + (math.cos(latrad1) * math.cos(latrad2) * math.cos(longrad2-longrad1)))
    dist = r * lawcos
    return dist
