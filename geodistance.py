from math import cos, asin, sqrt, pi


def distance(lat1, lon1, lat2, lon2):
    p = pi / 180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))


if __name__ == '__main__':
    dis = distance(1.396266, 103.892740, 1.3292210508705853, 103.93197977151728)
    print(dis)