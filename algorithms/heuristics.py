from typing import Tuple
from algorithms import utils
import math
from algorithms.problems import SystemRepairProblem


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(state, problem):
    """
    The Manhattan distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    """
    Esta es mi versión de código inicial
    
    position=state[0]
        if state[1]==False and state[2]:
            kposition=problem.kitPosition
            d=abs(position[0]-kposition[0])+abs(position[1]-kposition[1])
        elif state[1]==True and state[2]:
            tposition=problem.systemPositions[0]
            d=abs(position[0]-tposition[0])+abs(position[1]-tposition[1])
            
        elif not state[2]:
            cposition=problem.controlPosition
            d=abs(position[0]-cposition[0])+abs(position[1]-cposition[1])
        return d
    
    se la mandé a ChatGPT y le pregunté como hacer para saber si el sistema que estaba revisando era en efecto el más cercano
    y me dijo que tenía que:
        
    1.Recorrer state[2], porque ahí están los sistemas que todavía faltan.
    2.Calcular la distancia Manhattan desde position hasta cada uno.
    3.Quedarte con la menor distancia.
    
    Por ejemplo, la idea sería:

    distancias = []

    for sistema in state[2]:
        distancia = abs(position[0] - sistema[0]) + abs(position[1] - sistema[1])
        distancias.append(distancia)

    d = min(distancias)
    
    Y ojo con algo importante: problem.systemPositions contiene todos los sistemas originales, mientras que state[2] contiene únicamente los pendientes. Por eso para saber cuál falta y cuál es el más cercano debes usar:

    state[2]

    no:

    problem.systemPositions
    
    Ya con eso cambié mi código a la versión final y se la volví a mandar para comprobar que estuviera bien.
    """
    position = state[0]

    if not state[1]:
        kposition = problem.kitPosition
        d = abs(position[0] - kposition[0]) + abs(position[1] - kposition[1])

    elif state[2]:
        distanciaMinima = float("inf")
        for tposition in state[2]:
            dT = abs(position[0] - tposition[0]) + abs(position[1] - tposition[1])
            if dT < distanciaMinima:
                distanciaMinima = dT
        d = distanciaMinima

    else:
        cposition = problem.controlPosition
        d = abs(position[0] - cposition[0]) + abs(position[1] - cposition[1])

    return d    
        
    utils.raiseNotDefined()


def euclideanHeuristic(state, problem):
    """
    The Euclidean distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    """
    Esta es mi versión de código inicial
    
    position=state[0]
        if state[1]==False and state[2]:
            kposition=problem.kitPosition
            d=math.sqrt((position[0]-kposition[0])**2+(position[1]-kposition[1])**2)
        elif state[1]==True and state[2]:
            tposition=problem.systemPositions[0]
            d=math.sqrt((position[0]-tposition[0])**2+(position[1]-tposition[1])**2)
        elif not state[2]:
            cposition=problem.controlPosition
            d=math.sqrt((position[0]-cposition[0])**2+(position[1]-cposition[1])**2)
        return d
        
    Implementé los mismo cambios que me había dicho para manhattanHeuristic y le volví a mandar el código para comprobar 
    que estuviera bien.
    
    """
    position = state[0]

    if not state[1]:
        kposition = problem.kitPosition
        d = math.sqrt((position[0] - kposition[0]) ** 2 + (position[1] - kposition[1]) ** 2)

    elif state[2]:
        distanciaMinima = float("inf")
        for tposition in state[2]:
            dT = math.sqrt((position[0] - tposition[0]) ** 2 + (position[1] - tposition[1]) ** 2)
            if dT < distanciaMinima:
                distanciaMinima = dT
        d = distanciaMinima

    else:
        cposition = problem.controlPosition
        d = math.sqrt((position[0] - cposition[0]) ** 2 + (position[1] - cposition[1]) ** 2)

    return d
    
            
    utils.raiseNotDefined()

def _manhattanDistance(pos1, pos2):
    return (abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]))

def _mstCost(positions):
    """
    Calcula el MST usando la distancia Manhattan entre las posiciones.
    """

    if len(positions) <= 1:
        return 0

    visitados = {positions[0]}
    costo = 0

    while len(visitados) < len(positions):
        distanciaMinima = float("inf")
        puntoElegido = None
        for punto in visitados:
            for otro in positions:
                if otro not in visitados:
                    distancia = _manhattanDistance(punto,otro)
                    if distancia < distanciaMinima:
                        distanciaMinima = distancia
                        puntoElegido = otro
        costo += distanciaMinima
        visitados.add(puntoElegido)

    return costo

def systemRepairHeuristic(
    state: Tuple[Tuple, bool, Tuple], problem: SystemRepairProblem
):
    """
    Your heuristic for the SystemRepairProblem.

    state: (position, hasKit, pendingSystems)
    problem: SystemRepairProblem instance

    This must be admissible and preferably consistent.

    Hints:
    - Use problem.heuristicInfo to cache expensive computations
    - Go with some simple heuristics first, then build up to more complex ones
    - Consider the kit, pending systems, and the final return to control center
    - Balance heuristic strength vs. computation time (do experiments!)
    """
    position, hasKit, pendingSystems = state

    if problem.isGoalState(state):
        return 0
    
    key = (position, hasKit, pendingSystems)

    if key in problem.heuristicInfo:
        return problem.heuristicInfo[key]
    
    if not hasKit:
        distanciaAlKit = _manhattanDistance(position,problem.kitPosition)
        puntos = [problem.kitPosition]
        for sistema in pendingSystems:
            puntos.append(sistema)
        puntos.append(problem.controlPosition)
        costoMST = _mstCost(puntos)
        resultado= distanciaAlKit + costoMST

    elif pendingSystems:
        puntos = [position]
        for sistema in pendingSystems:
            puntos.append(sistema)
        puntos.append(problem.controlPosition)
        resultado= _mstCost(puntos)
    else:
        resultado= _manhattanDistance(position,problem.controlPosition)
    resultado= problem.heuristicInfo[key]
    
    return resultado
    utils.raiseNotDefined()
