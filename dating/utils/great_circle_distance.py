from geopy.distance import great_circle


def get_great_circle_distance(coodinatesA, coodinatesB, distance):
    return great_circle(coodinatesA, coodinatesB).miles <= distance
