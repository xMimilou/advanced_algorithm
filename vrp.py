import random
import math
grid_size = 10
nb_ville = 2
nb_camion = 4


def random_city():
    coordinate_ville = [(random.randint(1,grid_size),random.randint(1,grid_size)) for i in range(nb_ville)]
    base_coordinate = (0,0)
    coordinate_ville.insert(0,base_coordinate)
    return coordinate_ville

def distance_between_coord(coord_ville):
    table_distance_point = []
    for coord in coord_ville:        
        list_distance_point = []
        for point in coord_ville:
            coord_x = (point[0]-coord[0])
            coord_y = (point[1]-coord[1])
            dist = math.sqrt(coord_x**2+coord_y**2)
            list_distance_point.append(dist)
        table_distance_point.append(list_distance_point)
    return table_distance_point

print(distance_between_coord(random_city()))