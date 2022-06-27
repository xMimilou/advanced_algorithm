import random
from collections import deque
import math
from numpy import Infinity
from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt

grid_size = 10
nb_ville = 25
nb_camion = 4

taille_tabou = 500
iter_max = 10000
pile_chemin = [0 for i in range(nb_camion)]
random.seed(a=3)

list_color = {
    1 : "red",
    2 : "blue",
    3 : "green",
    4 : "orange"
}

# ajouter une matrice double dimentionnel pour simuler le trafic sur une route entre deux points et l'appliquer en coef au calcule de distance.


def random_city() -> list[list[int]]:
    '''
    Generate a random list of cities with coordinates.

    Return a list with the city coordinates.
    '''
    coordinates_cities = [(random.randint(-grid_size, grid_size), random.randint(
        -grid_size, grid_size), random.randint(1, nb_camion), i) for i in range(nb_ville)]

    print(coordinates_cities)
    return coordinates_cities


def alea_distance_bet_point(cities) -> list[list[int]]:
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


def distance_between_all_coord(coordinates_cities: list[list[int]]) -> list[list[float]]:
    '''
    Calculate the distance between 2 cities.

    Return a table of distance. The dimentions are the list of cities in order.
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

    Return the result square root of the addition of the 2 coordonnates.
    '''
    coord_x = (coord_1[0]-coord_2[0])
    coord_y = (coord_1[1]-coord_2[1])
    return math.sqrt(coord_x**2+coord_y**2)


def takethird(element: list):
    '''
    Return the 3rd element of a list.

    remplacer avec un dictionnaire?
    '''
    return element[3]


def longueur_trajet(solution: list[list[int]], num_traject: int) -> float:
    '''
    Calculate the travel distance.
    '''
    longueur: float = 0
    last_item = (0, 0, 0, 0)
    val = sorted(solution, key=takethird)

    for item in val:
        if item[2] == num_traject or (item[0] == 0 and item[1] == 0):
            longueur += distance_between_coord(last_item, item)
            last_item = item
    longueur += distance_between_coord(last_item, (0, 0))
    return longueur


def total_distance(solution):
    total_lenght = 0
    for i in range(1, nb_camion+1):
        total_lenght += longueur_trajet(solution, i)
    return total_lenght


def last_element(sol, num):
    val = sorted(sol, key=takethird)
    higher = 0
    for element in val:
        if element[2] == num:
            if element[3] > higher:
                higher = element[3]
    return higher


"""
def voisinage(solution):
    matrixe_voisin = []
    for j in range(1,nb_camion+1):
        list_voisin = []
        for k in range(len(solution)):
            #print(type(solution[k]))
            # un indice : on veut les états des k-1 premiers objets et des k+1 derniers objets
            # et l'état inverse de l'objet k (attention aux bornes du slicing)
            if (solution[k][2] == j):
                if solution[k][2] == nb_camion+1:
                    new_val =  1
                else:
                    new_val = solution[k][2] + 1 
                sol_val = ([solution[k][0],solution[k][1],new_val,0])
            else:
                new_val = j
                sol_val = ([solution[k][0],solution[k][1],new_val,last_element(solution,j)+1])
        
            voisin = solution[:k] + [sol_val] + solution[k+1:] #SOLUTION
            list_voisin.append(voisin)
        matrixe_voisin.append(list_voisin)
    return matrixe_voisin
"""


def voisinage2(solution, num_cam):
    list_voisin = []
    for k in range(len(solution)):
        # print(type(solution[k]))
        # un indice : on veut les états des k-1 premiers objets et des k+1 derniers objets
        # et l'état inverse de l'objet k (attention aux bornes du slicing)
        if (solution[k][2] == num_cam):
            if solution[k][2] == nb_camion:
                new_val = 1
            else:
                new_val = solution[k][2] + 1
            sol_val = ([solution[k][0], solution[k][1], new_val, 0])
        else:
            new_val = num_cam
            sol_val = ([solution[k][0], solution[k][1], new_val,
                       last_element(solution, num_cam)+1])

        voisin = solution[:k] + [sol_val] + solution[k+1:]  # SOLUTION
        list_voisin.append(voisin)
    return list_voisin


def tabou_search(solution_initiale, taille_tabou: int, iter_max: int):
    '''
    Calculate the tabou search with max length and interation.

    Return the best result for a tabou search
    '''
    nb_iter: int = 0
    liste_tabou = deque((), maxlen=taille_tabou)

    # variables solutions pour la recherche du voisin optimal non tabou
    solution_courante = solution_initiale
    meilleure = solution_initiale
    meilleure_globale = solution_initiale

    # variables valeurs pour la recherche du voisin optimal non tabou
    valeur_meilleure = total_distance(solution_initiale)
    valeur_meilleure_globale = valeur_meilleure

    while (nb_iter < iter_max):
        valeur_meilleure = Infinity

        # on parcourt tous les voisins de la solution courante
        for i in range(1, nb_camion):
            for voisin in voisinage2(solution_courante, i):
                # print(voisin)
                # print(solution_courante)
                valeur_voisin = total_distance(voisin)
                # print(valeur_voisin)
                # print(valeur_meilleure)
                # MaJ meilleure solution non taboue trouvée
                if valeur_voisin < valeur_meilleure and voisin not in liste_tabou:
                    valeur_meilleure = valeur_voisin
                    meilleure = voisin

        # on met à jour la meilleure solution rencontrée depuis le début
        if valeur_meilleure < valeur_meilleure_globale:
            meilleure_globale = meilleure
            valeur_meilleure_globale = valeur_meilleure
            nb_iter = 0
        else:
            nb_iter += 1

        # on passe au meilleur voisin non tabou trouvé
        solution_courante = meilleure

        # on met à jour la liste tabou
        liste_tabou.append(solution_courante)

    return meilleure_globale

# print(alea_distance_bet_point(random_city()))


def display_result(solution):
    val = sorted(solution, key=takethird)
    plt.title("Connected Scatterplot points with lines")
  
    # plot scatter plot with x and y data
    
    for camion in range(1,nb_camion+1):
        x = [0]
        y = [0]
        plt.scatter(x, y)
        print("Camion numéro : "+ str(camion))
        print("(0, 0, 0, 0)"+ " -> ", end='')
        for item in val:
            if (item[2] == camion):
                x.append(item[0])
                y.append(item[1])
                print(str(item) + " -> ", end='')
        print("(0, 0, 0, 0)")
        x.append(0)
        y.append(0)
        plt.plot(x, y, label= "label "+ str(camion), color=list_color[camion])
        plt.legend()
        print(longueur_trajet(val,camion))
    print(total_distance(val))  
    plt.show()  
    return x,y



val = tabou_search(random_city(), taille_tabou, iter_max)
x,y = display_result(val)

  
