import math


def great_circle_distance(lat1, long1, lat2, long2, r):
    latrad1 = lat1 * (math.pi / 180)
    latrad2 = lat2 * (math.pi / 180)
    longrad1 = long1 * (math.pi / 180)
    longrad2 = long2 * (math.pi / 180)
    lawcos = math.acos(
            (math.sin(latrad1) * math.sin(latrad2)) 
            + (math.cos(latrad1) * math.cos(latrad2) * math.cos(longrad2-longrad1)))
    dist = r * lawcos
    return dist
