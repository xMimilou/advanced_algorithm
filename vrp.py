import random
from collections import deque
import math
grid_size = 10
nb_ville = 2
nb_camion = 4


def random_city() -> list[list[int]]:
    '''
    Generate a random list of cities with coordinates.

    Return a list with the city coordinates.
    '''
    coordinates_cities = [(random.randint(1, grid_size), random.randint(
        1, grid_size), 0, 0) for i in range(nb_ville)]
    base_coordinate = (0, 0)
    coordinates_cities.insert(0, base_coordinate)
    return coordinates_cities


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
            print(item)
            longueur += distance_between_coord(last_item, item)
            print(longueur)
            last_item = item
    longueur += distance_between_coord(last_item, (0, 0))
    return longueur


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
    valeur_meilleure = valeur_contenu(solution_initiale)
    valeur_meilleure_globale = valeur_meilleure

    while (nb_iter < iter_max):
        valeur_meilleure = -1

        # on parcourt tous les voisins de la solution courante
        for voisin in voisinage(solution_courante):
            valeur_voisin = valeur_contenu(voisin)

            # MaJ meilleure solution non taboue trouvée
            if valeur_voisin > valeur_meilleure and voisin not in liste_tabou:
                valeur_meilleure = valeur_voisin
                meilleure = voisin

        # on met à jour la meilleure solution rencontrée depuis le début
        if valeur_meilleure > valeur_meilleure_globale:
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


print(longueur_trajet(
    [(0, 0, 1, 0), (1, 2, 1, 1), (2, 5, 1, 2), (5, 1, 1, 3)], 1))
