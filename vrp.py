import random

grid_size = 10
nb_ville = 10

def random_city():
    coordinate_ville = [(random.randint(1,grid_size),random.randint(1,grid_size)) for i in range(nb_ville)]
    base_coordinate = (0,0)
    coordinate_ville.insert(0,base_coordinate)
    return coordinate_ville

