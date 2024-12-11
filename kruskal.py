# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 20:56:19 2024

@author: SamuelBrambila
"""

import networkx as nx
import matplotlib.pyplot as plt

class algoritmoKruskal:
    def __init__(self, grafo):
        self.grafo = grafo
        self.aristas_mst = []
        self.pos = self.ordenamientoVertices()
    
    def ordenamientoVertices(self):
        # Crear posiciones para que los nodos se vean ordenados
        pos = {
            'A': (0, 3),      
            'B': (-1, 2),     
            'C': (1, 2),
            'D': (-1.5, 1),   
            'E': (1.5, 1),
            'F': (-1.5, 0),   
            'G': (1.5, 0),
            'H': (0, -1)      
        }
        return pos

    def kruskal(self):
        # Obtener todas las aristas del grafo y ordenarlas por peso
        aristas = sorted(self.grafo.edges(data=True), key=lambda x: x[2]['weight'])
        vertices = {nodo: nodo for nodo in self.grafo.nodes()}
        
        def findSet(u):
            if vertices[u] != u:
                vertices[u] = findSet(vertices[u])
            return vertices[u]
        
        def Union(u1, u2):
            f1 = findSet(u1)
            f2 = findSet(u2)
            if f1 != f2:
                vertices[f1] = f2
                self.aristas_mst.append((u1, u2))

        # Construir el Árbol de Expansión Mínima (MST)
        for u, v, data in aristas:
            Union(u, v)

    def dibujar_arbol_minimo(self):
        # Dibujar el grafo original con el árbol de expansión mínima resaltado
        plt.figure(figsize=(10, 7))
        nx.draw(self.grafo, self.pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
        etiquetas_aristas = nx.get_edge_attributes(self.grafo, 'weight')
        nx.draw_networkx_edge_labels(self.grafo, self.pos, edge_labels=etiquetas_aristas)
    
        # Resaltar las aristas del árbol de expansión mínima en rojo
        nx.draw_networkx_edges(self.grafo, self.pos, edgelist=self.aristas_mst, edge_color='red', width=2)
    
        plt.title("Árbol de Expansión Mínima con algoritmo Kruskal")
        plt.tight_layout()
    
        # Guardar el grafo en formato eps
        plt.savefig('kruskal.eps', format='eps', bbox_inches='tight')
    
        # Mostrar el grafo
        plt.show()


# Crear un grafo vacío
G = nx.Graph()

# Añadir nodos
nodos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
G.add_nodes_from(nodos)

# Definir las aristas
aristas = [
    ('A', 'B', 4),   
    ('B', 'D', 5),   
    ('D', 'F', 3),   
    ('F', 'H', 2),   
    ('G', 'H', 6),   
    ('G', 'E', 10),  
    ('C', 'E', 5),   
    ('C', 'A', 5),    
    ('A', 'F', 9),   
    ('A', 'G', 7),   
    ('B', 'C', 6),   
    ('B', 'G', 7),   
    ('C', 'F', 6),   
    ('D', 'H', 10),  
    ('E', 'H', 8),   
    ('F', 'G', 10),   
    ('B', 'H', 5),  
    ('D', 'G', 6),   
    ('A', 'H', 8),   
    ('C', 'H', 9)    
]

# Añadir las aristas con sus pesos al grafo
G.add_weighted_edges_from(aristas)

# Crear una instancia de la clase y ejecutar el algoritmo
arbol_kruskal = algoritmoKruskal(G)
arbol_kruskal.kruskal()

# Mostrar el grafo con el árbol de expansión mínima resaltado
arbol_kruskal.dibujar_arbol_minimo()