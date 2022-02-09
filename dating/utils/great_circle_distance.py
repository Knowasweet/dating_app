from geopy.distance import great_circle


def get_great_circle_distance(client_latitude, client_longitude, latitude, longitude, distance):
    newport_ri = (client_latitude, client_longitude)
    cleveland_oh = (latitude, longitude)
    return great_circle(newport_ri, cleveland_oh).miles <= distance
