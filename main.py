import numpy as np
import sys

if len(sys.argv) == 8:
    semilla = int(sys.argv[1])
    nodos = str(sys.argv[2])
    numero_hormigas = int(sys.argv[3])
    numero_iteraciones = int(sys.argv[4])
    evaporacion_feromona = float(sys.argv[5])
    valor_heuristica = float(sys.argv[6])
    probabilidad_limite = float(sys.argv[7])
    print("Semilla: ", semilla, "Matriz de nodos y coordenadas: ", nodos, "Numero de hormigas: ", numero_hormigas, "Numero de iteraciones maximas: ", numero_iteraciones, "factor de evaporacion de la feromona: ", evaporacion_feromona, "Peso del valor de la heuristica: ", valor_heuristica, "Valor de la probabilidad limite: ", probabilidad_limite, sep='\n')
else:
    print("Error en la entrada de los parametros", "Los paramentros a ingresar son: semilla, Matriz de nodos y coordenadas, Tamaño de la poblacion, Numero de iteraciones maximas, factor de evaporacion de la feromona, peso del valor de la heuristica, Valor de la probabilidad limite", sep='\n')
    sys.exit(0)

np.random.seed(semilla)



def crear_solucion_inicial():   # Creamos un arreglo mezclado con los valores de 0 hasta numero_nodos - 1 sin repetir 
    solucion_inicial = np.arange(numero_nodos)
    np.random.shuffle(solucion_inicial)
    return solucion_inicial

def crear_matriz_distancias():  # Creamos una matriz de numero_nodos x numero_nodos con 0s y 1s en la diagonal, luego reemplazamos la diagonal superior con las distancias de los nodos i, j y para hacerla simetrica le sumamos la transpuesta
    matriz_distancias = np.full((numero_nodos,numero_nodos),0, dtype=float) + np.eye(numero_nodos, dtype=int)
    for i in range(numero_nodos):
        for j in range(i + 1, numero_nodos):
            distancia = np.sqrt(np.sum(np.square(nodos[i]-nodos[j])))
            matriz_distancias[i][j] = distancia
    matriz_distancias = matriz_distancias + matriz_distancias.T
    return matriz_distancias

def calcular_distancia_hormiga(arr):    # Sumamos en una variable auxiliar las distancias de los valores del arreglo en la matriz de distancia
    aux = 0
    for i in range(arr.shape[0] - 1):
        aux += matriz_distancias[arr[i]][arr[i + 1]]
    aux += matriz_distancias[arr[0]][arr[arr.shape[0] - 1]]
    return aux

def crear_colonia_de_hormigas():    # Inicializamos la colonia con un nodo al azar en la primera columna y la memoria se inicializa con un 1 en la posicion del nodo
    colonia = np.full((numero_hormigas, numero_nodos), -1, dtype=int)
    memoria = np.full((numero_hormigas, numero_nodos), -1, dtype=int)
    for i in range(numero_hormigas):
        colonia[i][0] = np.random.randint(numero_nodos)
        memoria[i][colonia[i][0]] = 1
    return colonia, memoria

def crear_matriz_de_feromonas():    # La feromona de tamaÃ±o numero_nodos x numero_nodos se inicializa con la formula 1/NumVariables*Costo(Solucion_inicial), donde solucion_inicial = valor_mejor_solucion en la primera iteracion
    feromona = np.full((numero_nodos,numero_nodos),1/(numero_hormigas*valor_mejor_solucion))
    return feromona, 1/(numero_hormigas*valor_mejor_solucion)

def crear_matriz_distancias():  # Creamos una matriz de numero_nodos x numero_nodos con 0s y 1s en la diagonal, luego reemplazamos la diagonal superior con las distancias de los nodos i, j y para hacerla simetrica le sumamos la transpuesta
    matriz_distancias = np.full((numero_nodos,numero_nodos),0, dtype=float) + np.eye(numero_nodos, dtype=int)
    for i in range(numero_nodos):
        for j in range(i + 1, numero_nodos):
            distancia = np.sqrt(np.sum(np.square(nodos[i]-nodos[j])))
            matriz_distancias[i][j] = distancia
    matriz_distancias = matriz_distancias + matriz_distancias.T
    return matriz_distancias

def crear_matriz_heuristica():  # La matriz de heuristica es 1 dividido la matriz de distancias
    matriz_heuristica = 1/matriz_distancias
    return matriz_heuristica

def avanzar_hormiga(i): # Hacemos que una hormiga avance por todos los nodos, para ello buscamos sus nodos por visitar
    nodos_por_visitar = np.where(memoria[i] == -1)[0]
    for k in range(numero_nodos - 1):
        if np.random.rand() < probabilidad_limite:  # Con probabilidad q0 buscamos el nodo que tenga mejor Tij*Nij^b
            max = 0
            max_posicion = -1
            for j in nodos_por_visitar:
                if feromona[colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 1]][j]*(matriz_heuristica[colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 1]][j]**valor_heuristica) > max:
                    max = feromona[colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 1]][j]*(matriz_heuristica[colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 1]][j]**valor_heuristica)
                    max_posicion = j
            colonia[i][numero_nodos - nodos_por_visitar.shape[0]] = max_posicion
            memoria[i][max_posicion] = 1
            nodos_por_visitar = np.delete(nodos_por_visitar, np.where(nodos_por_visitar == max_posicion))
        else:                                       # Con probabilidad (1-q0) buscamos un nodo por metodo de la ruleta
            ruleta = np.array([])
            for j in nodos_por_visitar:
                ruleta = np.append(ruleta, feromona[colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 1]][j]*(matriz_heuristica[colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 1]][j]**valor_heuristica))
            ruleta /= np.sum(ruleta)
            seleccionado = np.random.choice(nodos_por_visitar, 1, p=ruleta)
            colonia[i][numero_nodos - nodos_por_visitar.shape[0]] = seleccionado
            memoria[i][seleccionado] = 1
            nodos_por_visitar = np.delete(nodos_por_visitar, np.where(nodos_por_visitar == seleccionado))
            # Las actualizaciones de la feromona local se resuelven a continuacion
        feromona[colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 2] ][colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 1] ] = (1-evaporacion_feromona)*feromona[colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 2] ][colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 1] ] + evaporacion_feromona*valor_inicial_feromona
        feromona[colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 1] ][colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 2] ] = feromona[colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 2] ][colonia[i][numero_nodos - nodos_por_visitar.shape[0] - 1] ]
    feromona[colonia[i][0]][colonia[i][numero_nodos - 1] ] = (1-evaporacion_feromona)*feromona[colonia[i][0]][colonia[i][numero_nodos - 1] ] + evaporacion_feromona*valor_inicial_feromona
    feromona[colonia[i][numero_nodos - 1]][colonia[i][0] ] = feromona[colonia[i][0]][colonia[i][numero_nodos - 1]]

nodos = np.genfromtxt(nodos, dtype = float, delimiter=' ', skip_header = 6, skip_footer=1, usecols=(1,2))
numero_nodos = nodos.shape[0]
matriz_distancias = crear_matriz_distancias()
arreglo_mejor_solucion = crear_solucion_inicial()
valor_mejor_solucion = calcular_distancia_hormiga(arreglo_mejor_solucion)
feromona, valor_inicial_feromona = crear_matriz_de_feromonas()
matriz_heuristica = crear_matriz_heuristica()
while numero_iteraciones > 0 and np.round(valor_mejor_solucion, decimals=4) != 7544.3659:
    colonia, memoria = crear_colonia_de_hormigas()
    
if np.round(valor_mejor_solucion, decimals=4) == 7544.3659:
    print("Se encontro la solucion")
    print("Solucion: ", arreglo_mejor_solucion)
else:
    print("Solucion no encontrada, mejor solucion: ", valor_mejor_solucion)
    print("con el arreglo: ", arreglo_mejor_solucion)


