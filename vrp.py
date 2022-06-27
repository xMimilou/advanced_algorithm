'''
:license:
    BSD 3-Clause License

    Copyright (c) 2022, xMimilou
    All rights reserved.
    
:author: Mathilde BALLOUHEY
:author: Tanguy DELANNOY
:author: Louka MILLON
:author: Maxime THOMAS

:school: CESI Saint-Nazaire
:year: 2022

===============================================================
:name: vrp.py

:description: Solve the VRP problem via tabu search.
TODO: Ajouter la contrainte de la distance.
'''

import random
from collections import deque
import math
from numpy import Infinity
import matplotlib.pyplot as plt
import time

# Entry parameters
grid_size = 50
nbr_cities = 25
nbr_truck = 4
size_tabu = 200
iter_max = 1000

road_pile = [0 for i in range(nbr_truck)]

# Colors for the graph
list_color = {
    1: "red",
    2: "blue",
    3: "green",
    4: "orange",
    5: "c",
    6: "m",
    7: "y",
    8: "purple",
    9: "k",
    10: "lime",
    11: "darkblue",
    12: "lavender",
    13: "blueviolet",
    14: "plum",
    15: "deeppink",
    16: "lightpink",
    17: "teal",
    18: "turquoise",
    19: "tan",
    20: "olive"
}
random.seed(a=3)

#TODO: Pas de voisinage ? C'est normal ?
def random_city() -> list[list[int]]:
    '''
    Generate a random list of cities with coordinates.

    :return coordinates_cities: List of the coordinates of the cities.
    '''
    coordinates_cities = [(random.randint(-grid_size, grid_size), random.randint(
        -grid_size, grid_size), random.randint(1, nbr_truck), i) for i in range(nbr_cities)]
    print(coordinates_cities)
    return coordinates_cities

# TODO: Utile?
def alea_distance_bet_point(cities) -> list[list[int]]:
    '''
    Calculate the distance between 2 cities.

    :param cities: List of cities. #TODO: Quel type?
    '''
    matrice = []
    for i in range(len(cities)):
        list_distance = []
        for j in range(len(cities)):
            if i == j:
                list_distance.append(0)
            else:
                list_distance.append(random.randint(0, 10))
        matrice.append(list_distance)
    return matrice

# TODO: Utile?
def distance_between_all_coord(coordinates_cities: list[list[int]]) -> list[list[float]]:
    '''
    Calculate the distance between 2 cities.

    :param coordinates_cities: List of cities.
    :return matrice: Matrix of the distance between 2 cities.
    '''
    table_distance_point = []
    for coord in coordinates_cities:
        ligne_distance_point = []
        for point in coordinates_cities:
            coord_x = (point[0]-coord[0])
            coord_y = (point[1]-coord[1])
            dist = math.sqrt(coord_x**2+coord_y**2)
            ligne_distance_point.append(dist)
        table_distance_point.append(ligne_distance_point)
    return table_distance_point


def distance_between_coord(coord_1: list[int], coord_2: list[int]) -> float:
    '''
    Calculate the distance between 2 coordonnates.

    :param coord_1: Coordinates of the first point.
    :param coord_2: Coordinates of the second point.
    :return distance: Distance between the 2 points.
    '''
    coord_x = (coord_1[0]-coord_2[0])
    coord_y = (coord_1[1]-coord_2[1])
    return math.sqrt(coord_x**2+coord_y**2)

# TODO : Pas plutôt le quatrième ?
def takethird(element: list[int]) -> int:
    '''
    Return the 3rd element of a list.

    :param element: List of elements.
    :return element[3]: 3rd element of the list.

    remplacer avec un dictionnaire?
    '''
    return element[3]


def length_trip(solution: list[list[int]], num_traject: int) -> float:
    '''
    Calculate the travel distance.

    :param solution: Solution of the problem.
    :param num_traject: Number of the trajectory.
    :return distance: Distance of the trajectory.
    '''
    lenght: float = 0
    last_item: tuple[int] = (0, 0, 0, 0)
    val = sorted(solution, key=takethird)

    for item in val:
        if item[2] == num_traject or (item[0] == 0 and item[1] == 0):
            lenght += distance_between_coord(last_item, item)
            last_item = item
    lenght += distance_between_coord(last_item, (0, 0))
    return lenght


def total_distance(solution: list[list[int]]) -> float:
    '''
    Calculate the total distance of the solution.

    :param solution: Solution of the problem.
    :return distance: Total distance of the solution.
    '''
    total_lenght = 0
    for i in range(1, nbr_truck+1):
        total_lenght += length_trip(solution, i)
    return total_lenght

# TODO: Si sort pk chercher le max ? Voir si Python à un max sur une liste directement
def last_element(solution: list[list[int]], num) -> int:
    '''
    Return the last element of a list.

    :param solution: List of elements.
    :param num: TODO c qwa ?
    :return element: Last element of the list. TODO Vraiment ? Pas plutôt le max ?
    '''
    val = sorted(solution, key=takethird)
    higher = 0
    for element in val:
        if element[2] == num:
            if element[3] > higher:
                higher = element[3]
    return higher

# TODO: À implémenter
# TODO: Réadapter pour la structure (x, y, p, n) ou optimiser avec une matrice de poids
def two_opt(cost_mat: list[list[float]], route: list[list[int]]) -> list[list[int]]:
    '''
    Implement the 2-opt algorithm.

    :param cost_mat: Matrix of the distance between 2 cities.
    :param route: List of cities defining a route to test.
    :return route: Solution of the problem.
    '''
    best: list[list[int]] = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue  # changes nothing, skip then
                new_route = route[:]    # Creates a copy of route
                new_route[i:j] = route[j - 1:i - 1:-1]  # this is the 2-optSwap since j >= i we use -1
                if length_trip(cost_mat, new_route) < length_trip(cost_mat, best): #TODO: Pour l'instant pas la bonne structure de données.
                    best = new_route
                    improved = True
                    route = best
    return best

def neighbourhood(solution: list[list[int]], num_cam) -> list[list[int]]:
    '''
    Get the list of the neighbours.

    :param solution: List of elements.
    :param num_cam: truck number TODO C qwa ?
    :return list_neighbours: List of the neighbours.
    '''
    list_neighbours = []
    for k in range(len(solution)):
        if (solution[k][2] == num_cam):
            if solution[k][2] == nbr_truck:
                new_val = 1
            else:
                new_val = solution[k][2] + 1
            sol_val = ([solution[k][0], solution[k][1], new_val, 0])
        else:
            new_val = num_cam
            sol_val = ([solution[k][0], solution[k][1], new_val,
                       last_element(solution, num_cam)+1])

        neighbour = solution[:k] + [sol_val] + solution[k+1:]
        list_neighbours.append(neighbour)
    return list_neighbours


def tabu_search(initial_solution: list[list[int]], size_tabu: int, iter_max: int) -> list[list[int]]:
    '''
    Calculate the tabou search with max length and interation.

    :param initial_solution: Initial solution of the problem.
    :param size_tabu: Max length of the tabou list.
    :param iter_max: Max iteration of the algorithm.
    :return solution: Solution of the problem.
    '''
    nbr_iter: int = 0
    list_tabu = deque((), maxlen=size_tabu)

    # solution variables for the optimal neighbour search (no tabu)
    current_solution = initial_solution
    best = initial_solution
    best_overrall = initial_solution

    # values variables for the optimal neighbour search (no tabu)
    value_best = total_distance(initial_solution)
    value_best_overrall = value_best

    while (nbr_iter < iter_max):

        # look amoung all neighbours the current solution
        for i in range(1, nbr_truck+1):
            for neighbour in neighbourhood(current_solution, i):
                value_neighbour = total_distance(neighbour)
                # update best solution not tabu found
                # TODO : faire une fonction qui utilise la fonction two opt

                if value_neighbour < value_best and neighbour not in list_tabu:
                    value_best = value_neighbour
                    best = neighbour

        # update best solution meet
        if value_best < value_best_overrall:
            best_overrall = best
            value_best_overrall = value_best
            nbr_iter = 0
        else:
            nbr_iter += 1

        # current_solution takes value of best solution not tabfound
        current_solution = best

        # update tabu list
        list_tabu.append(current_solution)

    return best_overrall


def display_result(solution: list[list[int]]) -> None:
    '''
    Display the solution of the problem.

    :param solution: Solution of the problem.
    '''
    val = sorted(solution, key=takethird)
    plt.title("Connected Scatterplot points with lines")

    # plot scatter plot with x and y data

    for truck in range(1, nbr_truck+1):
        x = [0]
        y = [0]
        plt.scatter(x, y)
        print("Camion numéro : " + str(truck))
        print("(0, 0, 0, 0)" + " -> ", end='')
        for item in val:
            if (item[2] == truck):
                x.append(item[0])
                y.append(item[1])
                print(str(item) + " -> ", end='')
        print("(0, 0, 0, 0)")
        x.append(0)
        y.append(0)
        plt.plot(x, y, label="label " + str(truck), color=list_color[truck])
        plt.legend()
        print(length_trip(val, truck))
    print(total_distance(val))
    plt.show()


start = time.time()

random.seed(a=5)
nb_starts = 50
val_max: list[list[int]] = [[-Infinity, -Infinity, 1, 0]]
for iter in range(nb_starts):
    val = tabu_search(random_city(), size_tabu, iter_max)
    print(total_distance(val))
    print(val)
    if total_distance(val) < total_distance(val_max):

        val_max = val
        print(val_max)
    print(iter)
display_result(val_max)

end = time.time()
elapsed = end - start

print(f'Temps d\'exécution : {elapsed} ms')
