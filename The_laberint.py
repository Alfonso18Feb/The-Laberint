'''
Importamos los siguientes módulos:
networkx lo importamos como nx(para facilidad en escribir codigo) para crear gráficos
matplotlib.pyplot lo importamos como plt(para facilidad en escribir codigo) y nos dibujan los gráficos creados
random nos ayuda para mezclar los nodos
collection cojemos deque para ayudarnos para utilizar plotleft
'''

import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import deque
'''
Aquí están los input del algoritmo:
Que son las filas y columnas que queremos que tenga el laberinto
'''
filas = int(input('Número de filas: '))
columnas = int(input('Número de columnas: '))


'''
Este metodo crear_laberinto nos dibuja el laberinto y tambien la solution marcado en azul
Se utiliza el algoritmo Prim y el BFS que es para crea y solucionar respectivamente
'''
def crear_laberinto(m, n):#m son las dilas y n las columnas

    G = nx.Graph()  #creamos un grafo vacio

    pos = {}#creamos dictionario para poner las posiciones de los nodos
    '''
    Estos bucles for crean los nudos teniendo coordenadas de cada nodo que se añadiranal grafo G
    También, lo añadimos al dictionario con el valor en coordenadas y sus coordenas en un plano
    O(n^2) y omega(n^2) y theta(n^2)
    '''
    for i in range(m):
        for j in range(n):
            node = (i, j)
            G.add_node(node)
            pos[node] = (j, -i)#-i es para que el (0,0) este arriba a la izquierda


    edges = []#creamos una lista edges donde pondremos todos las posibles aristas
    '''
    Hacemos un bucle for para recorer los nodos como una matriz 
    esto nos sirve para añadir todas las posibles aristas que pueden esta conectado al nodo
    Que están restringidos porque sólo queremos caminos que no sean cíclicos
    Esta complejidad es 
    O(n^2) y omega(n^2) y theta(n^2)
    '''
    for i in range(m):
        for j in range(n):
            if j < n - 1:  #tenemos que ver que para cada j menor a n-1(columnas) podemos movernos a la derecha
                edges.append(((i, j), (i, j + 1)))#añadimos una tupla con los dos nodos que esta conectando la arista
            if i < m - 1:  #Aqui lo que hacemos es ver que la i cuando es menor a m-1(filas) podemos conectar con el nodo de abajo
                edges.append(((i, j), (i + 1, j)))#añadimos una tupla con los dos nodos que esta conectando la arista
 
    start_node = (0, 0)# el nodo donde empezamos estara en coordenadas (0,0)
   
    visited = set([start_node])#creamos un conjunto visited donde añadimos start_node ya que el mismo ya esta visitado
    edges = random.sample(edges, len(edges)) #mezclamos los las aristas para que cambien los caminos 
    maze_edges = []#creamos una lista maze_edge donde pondremos los caminos del laberinto
    '''
    Este bucle while nos repite el bucle hasta que hayamos visitado todos los nodos
    Luego dentro hay un bucle for que recorre cada tupla de la lista de edges(que son todo los tipo de vértices creados anteriormente)
    cada tupla tiene dos nodos que los llamamos u y v
    En el If vemos si el nodo u esta visitado y tambien que el nodo v no este en el conjunto de visitados
    SI esto es cierto entonces añadimos la arista(u,v) a maze_edge
    También, añadimos la v (que no estaba visitado al conjunto de visitados).
    Entonces se rompe el bucle for y comprobamos si ya hemos recorido todos los nodos
    SI lo hemos recorrido todo los nodos entonces al grafo G le añadimos todo los vertices que están en nuestra lista de maze_edges
    
    La complejidad de este Algoritmo sería:
    O(n^2) y omega(n^2)y theta(n^2)
    '''
    while len(visited) < m * n:
        for edge in edges:
            u, v = edge
            if u in visited and v not in visited:
                maze_edges.append(edge)
                visited.add(v)
                break
    G.add_edges_from(maze_edges)

    entrada = (0, 0)#entrada de laberinto
    salida = (m-1, n-1)#salida de laberinto
    '''
    Ahora dibujamos utilizando el metodo plt y nx.draw para crear el laberinto
    '''
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, with_labels=False, node_size=100, node_color='skyblue', font_size=10)#los puntos del camino
    nx.draw_networkx_nodes(G, pos, nodelist=[entrada], node_color='red')  #la entrada esta en rojo
    nx.draw_networkx_nodes(G, pos, nodelist=[salida], node_color='green') #la salida esta en verde
    plt.show()

    ''''
    Aquí empezamos a crear el algoritmo BFS que Solucion el Laberinto
    '''
    queue = deque([entrada]) #creamos una lista de los nodos que vamos cojiendo
    visited = {entrada: None} #creamos un dictionario visited donde se pondran gurdar los vecinos de cada nodo

    while queue:# cuando a queue este llena
        current_node = queue.popleft() #llamamos a current_node el primer nodo de la lista queue
        '''
        Este bucle for recorre todas las vecindades (neighbors) para cada neighbour:
        luego vemos si NO esta vecindad(hijo de current_node) está en el dictionario visited
        Entonces si no esta en visited añadimos a visited un dictionario:
        ((el nodo del vecino), (el nodo que estamos))
        El nodo del vecino lo añadimos a la lista queue
        
        '''
        for neighbor in G.neighbors(current_node):
            if neighbor not in visited:
                visited[neighbor] = current_node  
                queue.append(neighbor) 

        if current_node == salida:#si coencide que el current nodo estamos en el nodo salida
           
            camino = []#una lista vacia donde pondremos el camino mas corto para resolver el laberinto
            '''
            En otras palabras, el bucle while va ha retroceder del dicionario visited hasta llegar al Key NONE
            Primer añadimos el current_node que sería la salida
            luego cojemos el key de la salida para ver que nodo está conectado a la salida
            Que estos están escritos en el dictionario visited
            Entonces vemos si esta llave Key es NONO Si not NONE
            repetimos el bucle hasta llegar a la salida
            '''
            while current_node is not None:# haces este bucle hasta llgar a la key NONE que seria la entrada.
                camino.append(current_node)#añadimos el nodo a los caminos
                current_node = visited[current_node]
            camino.reverse()  # Invertir el camino para que sea de entrada a salida
            
            '''
            Ahora dibujamos el mismo grafo pero esta vez tenemos un path_edges que 
            es la solución más corta del laberinto.
            En el grafo lo dibujaremos en azul
            '''
            plt.figure(figsize=(8, 8))
            nx.draw(G, pos, with_labels=False, node_size=100, node_color='skyblue', font_size=10)
            nx.draw_networkx_nodes(G, pos, nodelist=[entrada], node_color='red')  # Nodo entrada
            nx.draw_networkx_nodes(G, pos, nodelist=[salida], node_color='green')  # Nodo salida
            path_edges = [(camino[i], camino[i + 1]) for i in range(len(camino) - 1)]# Aqui hacemos un for que recorre la lista de caminos y hacemos una lista de los dos nodos conectados que seran (camino[i], camino[i + 1])
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color='blue')#dibujamos el camino en azul con grosor 4
            plt.show()
            return


crear_laberinto(filas, columnas)
