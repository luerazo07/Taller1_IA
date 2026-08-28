from algorithms.problems import SearchProblem
import algorithms.utils as utils
from world.game import Directions
from algorithms.heuristics import nullHeuristic


def tinyDiagnosticSearch(problem: SearchProblem):
    """
    Returns a hard-coded sequence of moves for the tinyDiagnostic layout.
    For any other station layout, the sequence of moves will be incorrect.
    """
    s = Directions.SOUTH
    e = Directions.EAST
    return [s, e, s, e, e, e, e, s, e, e, s, s, e, s, s, e, s, e, e, e, e, e, e, e]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    empezamo= problem.getStartState()
    if problem.isGoalState(empezamo):
        return []
    sino =utils.Stack()
    sino.push((empezamo, []))
    vecinos= []
    while not sino.isEmpty():
        actual, pepe = sino.pop()
        if actual in vecinos:
            continue
        vecinos.append(actual)
        if problem.isGoalState(actual):
            return pepe
        for a, b, c in problem.getSuccessors(actual):
            if a not in vecinos:
                guardar = [b]
                sino.push((a, guardar))
                
    return []
                
        


def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    """
    Version inicial del codigo
    def breadthFirstSearch(problem: SearchProblem):
    nodo = problem.getStartState()
    if problem.isGoalState(nodo): return nodo
    fromtera = utils.Queue()
    fromtera.push(nodo)
    alcanzados = set()
    alcanzados.add(nodo)
    while fromtera.isEmpty() == False:
        nodo = fromtera.pop()  
        for sucesor in problem.getSuccessors(nodo):
            s = sucesor.getState()
            if problem.isGoalState(s): return sucesor 
            if s not in alcanzados:
                alcanzados.add(s)
                fromtera.push(s, sucesor.getActions())  

    utils.raiseNotDefined()

    Mi version inicial del codigo esta basada en el pseudocodigo proporcionado en clase.


    """
def breadthFirstSearch(problem: SearchProblem):

    estadoInicial = problem.getStartState()
    if problem.isGoalState(estadoInicial):
        return []

    frontera = utils.Queue()
    frontera.push((estadoInicial, []))

    alcanzados = set()
    alcanzados.add(estadoInicial)

    while not frontera.isEmpty():
        nodo, acciones = frontera.pop()
        for sucesor in problem.getSuccessors(nodo):
            s, action, stepCost = sucesor
            if s not in alcanzados:
                nuevasAcciones = acciones + [action]
                if problem.isGoalState(s):
                    return nuevasAcciones
                alcanzados.add(s)
                frontera.push((s, nuevasAcciones))

    return []  # no se encontró solución


def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """
    """
    
    estado = problem.getStartState()
    acciones = []
    costo = 0
    nodo = (estado, acciones, costo)
    
    if  problem.isGoalState(nodo[0]) == True:
        return acciones
    frontera = utils.PriorityQueue()
    frontera.push(nodo,costo)
    alcanzados = set()
    alcanzados.add(nodo[0])
    while frontera.isEmpty() == False:
        siguientes = frontera.pop()
        sucesores = problem.getSuccessors(siguientes[0])
        for i in sucesores:
            if problem.isGoalState(i[0]) == True:
                return acciones
            if i[0] not in alcanzados:
                alcanzados.add(i[0])
                frontera.push(i)
    return acciones
    
    // Este de aqui es mi codigo inicial a partir del pseudocodigo que vimos en clase, hay una parte que me genera
    dudas y es la parte de como manejar las acciones y el costo acumulado de los sucesores que se van expandiendo.
    
    Es por esto que le solicite ayuda a Claude con el siguiente prom para poder identificar errores y realizar el manejo
    de acciones y costos:
    
    promt: mira este es mi codigo actualmente, podrias ayudarme a revisar posibles correcciones que le pueda realizar sin darme
    el codigo directo, tambien tengo dudas sobre como manejar el tema de las acciones y los costos acumulados, podrias guiarme 
    sin darme explicitamente codigo.
    
    La respuesta de CLaude fue esta:
    
    Dale, vamos a revisarlo por partes, señalando qué falta sin darte el bloque armado — así lo terminas de conectar tú.

    1. El chequeo de meta está en un lugar "arriesgado"
    python
    for i in sucesores:
        if problem.isGoalState(i[0]) == True:
            return acciones

    Dos cosas para pensar aquí:

    Recuerda: en UCS es más seguro chequear la meta al sacar un nodo de la frontera (justo después de frontera.pop()), no al generar cada sucesor dentro del for. ¿Por qué? Porque cuando generas un sucesor, todavía no sabes si ese es el camino más barato hasta ahí — podría haber otro camino más barato al mismo estado que todavía está esperando en la cola. Solo cuando la PriorityQueue te lo entrega vía pop() (que siempre da el de menor costo primero) puedes estar seguro de que si es meta, es la solución óptima.
    Pregúntate: ¿dónde deberías mover ese if isGoalState? Pista: justo después de la línea siguientes = frontera.pop(), antes incluso de calcular sucesores.
    2. return acciones — ¿qué acciones es esa?
    python
    return acciones

    Esta variable acciones es la que creaste una sola vez al inicio de la función y nunca la vuelves a tocar dentro del while. Entonces sin importar en qué parte del mapa encuentres la meta, siempre vas a retornar la lista vacía original ([]), porque nunca la actualizaste.

    Pregúntate: si vas a mover el chequeo de meta a justo después del pop() (punto 1), ¿qué variable deberías retornar ahí en su lugar? Pista: el nodo que acabas de sacar (siguientes) ya trae consigo el camino completo de acciones que lo trajo hasta acá — ¿en qué posición de esa tupla está guardado eso?

    3. Estas pusheando i (el triple crudo), no un nodo nuevo
    python
    frontera.push(i)

    Dos problemas:

    push en tu PriorityQueue necesita dos argumentos (item y prioridad) — acá solo le estás pasando uno.
    i es el triple (sucesor, accion, stepCost) tal como te lo dio getSuccessors. Pero lo que necesitas meter a la frontera es un nodo con la forma (estado, acciones, costo) — igual que como armaste el nodo inicial al principio de tu función.

    Piénsalo así: cada vez que expandes un nodo, por cada sucesor que generas necesitas construir uno nuevo con esa misma estructura de 3 elementos, no simplemente reenviar el triple tal cual te llegó.

    Preguntas para guiarte en esa construcción:

    Tienes siguientes (el nodo padre, con su propia lista de acciones y su propio costo) y i (el triple del sucesor, con su acción individual y su costo de un solo paso). ¿Cómo combinas la lista de acciones del padre con la acción individual del hijo para armar la lista de acciones completa del nuevo nodo? (repasa el patrón lista_vieja + [elemento_nuevo] que vimos antes)
    ¿Cómo combinas el costo acumulado del padre con el stepCost del triple para sacar el costo total del nuevo nodo?
    Una vez tengas esos dos valores nuevos (lista de acciones actualizada, costo actualizado), ¿cómo arman junto con el estado sucesor (i[0]) la tupla completa del nuevo nodo?
    Y finalmente, ¿qué le pasas como segundo argumento a push para que la cola sepa dónde ubicarlo?
    Resumen de lo que debes ajustar
    Mueve el chequeo de isGoalState a justo después de frontera.pop().
    Ahí, retorna las acciones que trae el nodo que sacaste (no la variable acciones original de la línea 2).
    Dentro del for, en vez de pushear i directamente, construye un nodo nuevo (estado_sucesor, acciones_actualizadas, costo_actualizado) y pushealo con su costo como prioridad.

    Intenta reescribirlo con estas tres correcciones en mente y me lo muestras
    
    // Ahi le pregunte que no entendia por que me decia lo de la verificacion luego del pop si ya estaba, incluso el ciclo for tambien estaba luego del pop, a lo que la ia me respondio:
    
    Sí, exacto — el pop() va antes del for, y de hecho ya lo tienes así en tu código actual. Vamos a mirar tu propio código línea por línea para que veas dónde está cada cosa:

    python
    while frontera.isEmpty() == False:
        siguientes = frontera.pop()              # <- 1. sacas el nodo de menor costo
        sucesores = problem.getSuccessors(siguientes[0])   # <- 2. lo expandes
        for i in sucesores:                       # <- 3. recorres sus sucesores
            ...

    Fíjate: siguientes = frontera.pop() ya está antes del for en tu código — eso está bien puesto. Lo que te decía es que el chequeo de meta (if problem.isGoalState(...)) actualmente está adentro del for, revisando cada sucesor i. Lo que te sugiero es que ese chequeo lo hagas apenas sacas siguientes del pop(), antes de siquiera calcular sucesores — o sea, entre la línea 1 y la línea 2 de arriba.

    Así quedaría la estructura (sin código, solo el orden de los pasos)
    while la frontera no esté vacía:
        1. sacar el nodo de la frontera (pop) → esto te da (estado, acciones, costo)
        2. CHEQUEAR AQUÍ: ¿ese estado es meta? 
        → si sí, retornas las acciones de ESE nodo, terminas la función
        3. si no es meta, ahí sí llamas getSuccessors sobre ese estado
        4. recorres cada sucesor con el for
        5. por cada sucesor, construyes un nodo nuevo y lo pusheas si no está visitado
    Por qué se mueve ahí y no se queda en el for

    Piénsalo así: el nodo que sacas con pop() es, por construcción de la PriorityQueue, el más barato de toda la frontera en ese momento. Si justo ese nodo resulta ser meta, ya sabes con certeza que no existe ningún camino más barato — porque si existiera, habría estado en la frontera con menor costo y el pop() te lo habría entregado a él primero. Por eso el chequeo va ahí, apenas lo sacas, y no cuando apenas lo estás generando como sucesor (en ese punto todavía no sabes si es el camino óptimo hasta ahí).

    ¿Con esto te queda más claro dónde reubicar esa condición? Intenta moverla y ajusta el return para que retorne las acciones de siguientes, no de la variable acciones original.
        
    //A partir de estas recomendaciones aplique cambios como sacar cada una de las partes en variables como sucesor, accion, ncosto e ir guardando progresivamente las acciones propias de cada ruta 
    junto con el costo acumulado de ese nodo en el momento dado, luego de algunas verificaciones y pruebas este fue mi codigo.
        
    """            
    
    estado = problem.getStartState()
    acciones = []
    costo = 0
    nodo = (estado, acciones, costo)
       
    if problem.isGoalState( nodo[0]) == True:
        return acciones
    
    frontera = utils.PriorityQueue()
    frontera.push(nodo,costo)
    alcanzados = set()
    alcanzados.add(nodo[0])
    while frontera.isEmpty() == False:
        siguientes = frontera.pop()
        if problem.isGoalState(siguientes[0]) == True:
                return siguientes[1]
        sucesores = problem.getSuccessors(siguientes[0])
        
        for i in sucesores:
            sucesor,accion, ncosto = i
            nuevasAcciones = siguientes[1] + [accion]
            nuevoCosto = siguientes[2] + ncosto
            nNodo = (sucesor, nuevasAcciones, nuevoCosto)
            if i[0] not in alcanzados:
                alcanzados.add(i[0])
                frontera.push(nNodo, nuevoCosto)
    return acciones
 


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    """
    Este era mi código inicial
    
    estado = problem.getStartState() 
    acciones = [] 
    costo = 0 
    nodo = (estado, acciones, costo) 
    
    if problem.isGoalState( nodo[0]) == True: 
        return acciones frontera = utils.PriorityQueue() 
        
    frontera.push(nodo,costo+heuristic) 
    alcanzados = {} 
    alcanzados[estado] = nodo 
    
    while not frontera.isEmpty(): 
        nodo=frontera.pop() 
        if problem.isGoalState( nodo.estado) == True: 
            return nodo problem.getSuccessors(nodo[0])
            
    ----------------
    estado = problem.getStartState() 
    acciones = [] 
    costo = 0 
    nodo = (estado, acciones, costo) 
    
    if problem.isGoalState( nodo[0]) == True: 
        return acciones 
        
    frontera = utils.PriorityQueue() 
    frontera.push(nodo,costo+heuristic) 
    alcanzados = {} 
    alcanzados[estado] = nodo
     
    while not frontera.isEmpty(): 
        nodo_frontera=frontera.pop() 
        if problem.isGoalState( nodo_frontera[0]) == True:
            return nodo_frontera[1] 
        siguientes=problem.getSuccessors(nodo_frontera[0]) 
        
        for i in siguientes: 
            sucesor,accion, ncosto = i 
            nuevasAcciones = nodo_frontera[1] + [accion] 
            nuevoCosto = nodo_frontera[2] + ncosto 
            hijo = (sucesor, nuevasAcciones, nuevoCosto) 
            
            if sucesor not in alcanzados or (sucesor in alcanzados and nuevoCosto<alcanzados[sucesor][costo]): 
                alcanzados[sucesor]=hijo 
                nuevah=heuristic(sucesor, problem) 
                frontera.push(hijo,costo+heuristic)
                
    Se lo mandé a ChatGPT para saber si estaba correcto y me respondió esto:
    1. Esta línea está mal
    frontera.push(nodo, costo + heuristic)

    Por qué: heuristic es una función, no un número
    Tienes:

    costo = 0
    heuristic = una función

    y no puedes hacer:

    número + función

    Necesitas ejecutar la heurística sobre el problema y el estado para obtener el valor h.

    Recuerda:

    f = g + h
    
    2. Esta parte está mal
    alcanzados[sucesor][costo]

    alcanzados[sucesor] te devuelve el nodo guardado:

    (estado, acciones, costo)

    Pero costo es una variable que vale 0, no el índice que quieres usar.

    Recuerda tu estructura:

    hijo = (sucesor, nuevasAcciones, nuevoCosto)
            [0]          [1]              [2]

    Por lo tanto, para obtener el costo del nodo que ya estaba guardado en alcanzados, tienes que usar la posición correspondiente al costo.

    Tu comparación conceptualmente debe ser:

    nuevoCosto < costo_del_nodo_que_ya_estaba_guardado
    
    3. Esta línea también está mal
    frontera.push(hijo,costo+h)

    Porque costo y h son los valores que calculaste para el nodo inicial.

    Para cada hijo tienes que calcular su propio:

    g = nuevoCosto
    h = heurística del estado del hijo
    f = g + h

    Es decir, no puedes reutilizar el costo y h del inicio.

    Piensa:

    nodo_frontera
       ↓
    nuevo hijo
        ↓
    nuevoCosto       ← g del hijo
    heuristic(...)   ← h del hijo
       ↓
    g + h             ← prioridad del hijo
    
    Ahí vi que partes de la estructura estaba pensando mal, porque y cual era la forma correcta de ver 
    el problema, entonces realicé los cambios que me dijo y le volví a mandar el código
    para comprobar que estuviera bien.
    """
    estado = problem.getStartState()
    acciones = []
    costo = 0
    nodo = (estado, acciones, costo)
        
    if problem.isGoalState( nodo[0]) == True:
        return acciones
    
    h=heuristic(nodo[0], problem)
    frontera = utils.PriorityQueue()
    frontera.push(nodo,costo+h)
    alcanzados = {}
    alcanzados[estado] = nodo
    
    while not frontera.isEmpty():
        nodo_frontera=frontera.pop()
        if problem.isGoalState( nodo_frontera[0]) == True:
            return nodo_frontera[1]
        siguientes=problem.getSuccessors(nodo_frontera[0])
        
        for i in siguientes:
            sucesor,accion, ncosto = i
            nuevasAcciones = nodo_frontera[1] + [accion]
            nuevoCosto = nodo_frontera[2] + ncosto
            hijo = (sucesor, nuevasAcciones, nuevoCosto)
            
            if sucesor not in alcanzados or (sucesor in alcanzados and nuevoCosto<alcanzados[sucesor][2]):
                alcanzados[sucesor]=hijo
                nuevah=heuristic(sucesor, problem)
                frontera.push(hijo,nuevoCosto+nuevah)
                
    return []
    utils.raiseNotDefined()


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
