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
import copy
from itertools import combinations,permutations
import random
from collections import deque
import math
from matplotlib import container
from numpy import Infinity
import matplotlib.pyplot as plt
import time

# Entry parameters
grid_size = 50
nbr_cities = 25
nbr_truck = 5
size_tabu = 20
iter_max = 100

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

def truck_container() -> dict[list[int]]:
    '''
    Generate a list of containers for each truck.

    :return containers: List of containers.
    '''
    containers = {i : [] for i in range(1, nbr_truck+1)}
    return containers



#TODO: Pas de voisinage ? C'est normal ?
'''
def random_city() -> list[list[int]]:
   
    #Generate a random list of cities with coordinates.

    #:return coordinates_cities: List of the coordinates of the cities.
    
    coordinates_cities = [(random.randint(-grid_size, grid_size), random.randint(
        -grid_size, grid_size), random.randint(1, nbr_truck), i) for i in range(nbr_cities)]
    print(coordinates_cities)
    return coordinates_cities
'''
def random_cities() -> dict[list[int]]:
    coordinates_cities = {i : [random.randint(-grid_size, grid_size), random.randint(
        -grid_size, grid_size)] for i in range(1,nbr_cities)}
    coordinates_cities_base = {0 : [0,0]}
    coordinates_cities_base.update(coordinates_cities)
    return coordinates_cities_base


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

def length_trip(solution, num_traject: int) -> float:
    '''
    Calculate the travel distance.

    :param solution: Solution of the problem.
    :param num_traject: Number of the trajectory.
    :return distance: Distance of the trajectory.
    '''
    lenght: float = 0
    last_item: int = 0
    for point in solution[num_traject]:
        lenght += distance_between_coord(coord_city[last_item], coord_city[point])
        last_item = point
    lenght += distance_between_coord(coord_city[last_item], coord_city[0])
    
    return lenght

def length_trip_array(solution) -> float:
    '''
    Calculate the travel distance.

    :param solution: Solution of the problem.
    :param num_traject: Number of the trajectory.
    :return distance: Distance of the trajectory.
    '''
    lenght: float = 0
    last_item: int = 0
    for point in solution:
        lenght += distance_between_coord(coord_city[last_item], coord_city[point])
        last_item = point
    lenght += distance_between_coord(coord_city[last_item], coord_city[0])
    
    return lenght

def total_distance(solution) -> float:
    '''
    Calculate the total distance of the solution.

    :param solution: Solution of the problem.
    :return distance: Total distance of the solution.
    '''
    total_lenght = 0
    for i in solution:
        total_lenght += length_trip(solution, i)
    return total_lenght

def test_pos(tableau, element):
    table = []
    for i in range(len(tableau)):
        copy_table = tableau.copy()
        copy_table.insert(i, element)
        table.append(copy_table.copy())
    tableau.append(element)
    table.append(tableau.copy())
    return table

def neighbourhood(solution: list[list[int]]) -> list[list[int]]:
    '''
    Get the list of the neighbours.

    :param solution: List of elements.
    :param p_nbr_truck: truck number
    :return list_neighbours: List of the neighbours.

    TODO : modifier et adapter avec le dictionnaire de camion avec les coordonnées

    '''
    #print(f"solution initial is : {solution}")
    #print(f"solution 1 is : {solution[1]}")
    list_neighbours = []
    for camion in solution:
        for i in solution[camion]:
            copy_solution = copy.deepcopy(solution)
            #print(f"solution is : {solution}")
            #print(f"copy_solution is : {copy_solution}")
            copy_solution[camion].remove(i)
            #print(f"solution is : {solution}")
            #print(f"value sent and remove is : {i}")
            if camion == nbr_truck:
                
                for combo in test_pos(copy_solution[1].copy(),i):
                    copy_solution[1] = list(combo)
                    #print(copy_solution[1])
                    #print(f"copy_solution nbr_truck : {copy_solution}")
                    list_neighbours.append(copy_solution.copy())
                    
            else:
                
                for combo in test_pos(copy_solution[camion+1].copy(),i):
                    copy_solution[camion+1] = list(combo)
                    #print(f"copy_solution {copy_solution}")
                    list_neighbours.append(copy_solution.copy())

            copy_solution = []
    #print("neighbours are : ", list_neighbours)               
    return list_neighbours
    # for k in range(len(solution)):
        
    #     if (solution[k][2] == p_nbr_truck):
    #         if solution[k][2] == nbr_truck:
    #             new_val = 1
    #         else:
    #             new_val = solution[k][2] + 1
    #         sol_val = ([solution[k][0], solution[k][1], new_val, last_element(solution, p_nbr_truck)+1])
    #     else:
    #         new_val = p_nbr_truck
    #         sol_val = ([solution[k][0], solution[k][1], new_val,
    #                    last_element(solution, p_nbr_truck)+1])

    #     neighbour = solution[:k] + [sol_val] + solution[k+1:]
    #     list_neighbours.append(neighbour)


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

    # analyse statistics de la recherche tabu
    courantes = []
    meilleures_courantes = []

    while (nbr_iter < iter_max):

        # look amoung all neighbours the current solution
        
        #print(neighbourhood(current_solution))
        for neighbour in neighbourhood(current_solution):
            
            value_neighbour = total_distance(neighbour)

            #print(value_neighbour)
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
        meilleures_courantes.append(value_best_overrall)
        courantes.append(value_best)
        # current_solution takes value of best solution not tabfound
        current_solution = best

        # update tabu list
        list_tabu.append(current_solution)

    return best_overrall, courantes , meilleures_courantes

def generate_random_solution(container_truck, cities):
    '''
    Generate a random solution.

    :param container_truck: List of the trucks.
    :param cities: List of the cities.
    :return solution: Solution of the problem.
    '''
  
    for i in cities : 
        if i != -1:
            container_truck[random.randint(1, nbr_truck)].append(i)
    return container_truck

def display_result(p_solution) -> None:
    '''
    Display the solution of the problem.

    :param solution: Solution of the problem.
    '''
    
    plt.title("Connected Scatterplot points with lines")

    # plot scatter plot with x and y data
    print(p_solution)
    for truck in p_solution:
        x = [0]
        y = [0]
        plt.scatter(x, y)
        print("Camion numéro : " + str(truck))
        print("(0, 0, 0, 0)" + " -> ", end='')
        for item in p_solution[truck]:
            x.append(coord_city[item][0])
            y.append(coord_city[item][1])
            print(str(item) + " -> ", end='')
        print("(0, 0, 0, 0)")
        x.append(0)
        y.append(0)
        plt.plot(x, y, label="label " + str(truck), color=list_color[truck])
        plt.legend()
        
    print(f" my solution : {p_solution}")
    print(f"test : {total_distance(p_solution)}")
    plt.show()

coord_city = random_cities() 

solution_initiale = generate_random_solution(truck_container(), coord_city)
new_coord_city = {-1 : [Infinity, Infinity]}
coord_city.update(new_coord_city)
val, courants, meilleurs_courants = tabu_search(solution_initiale, size_tabu, iter_max)
display_result(val)
#print(courants)
#print(meilleurs_courants)
plt.xlabel("nb itérations", fontsize=16)
plt.ylabel("valeur", fontsize=16)
plt.legend()
plt.plot(range(len(courants)), courants)
plt.plot(range(len(courants)), meilleurs_courants)
plt.show()

start = time.time()
random.seed(a=5)
nb_starts = 500
val_max: list[list[int]] = {1 : [-1]}
for iter in range(nb_starts):
    solution_initiale = generate_random_solution(truck_container(), coord_city)
    val, courants, meilleurs_courants = tabu_search(solution_initiale, size_tabu, iter_max)
    #print(total_distance(val))
    if total_distance(val) < total_distance(val_max):
        val_max = val
        #print(val_max)
    print(iter)
#print(total_distance(val_max))
display_result(val_max)
end = time.time()
elapsed = end - start
print(f'Temps d\'exécution : {elapsed} ms')


