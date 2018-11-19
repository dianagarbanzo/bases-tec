import networkx as nx
import matplotlib.pyplot as plt 


def get_levels(graph, root):
    levels = {}
    level = 0
    current_level_nodes = [root] 
    successors_by_node = dict(nx.bfs_successors(graph,root))

    while current_level_nodes:
        next_level_nodes = []
        levels[level] = current_level_nodes

        for node in current_level_nodes:
            successors = successors_by_node.get(node,[])
            next_level_nodes += successors
        
        level += 1
        current_level_nodes = next_level_nodes
   
    return levels

def get_predecessors(graph, levels):
    predecessors = {}

    for level, nodes in levels.items():
        for node in nodes:
            neighbors_of_node = graph.neighbors(node)
            predecessors_of_node = []
            for neighbor in neighbors_of_node:
                if(level > 0):
                    upper_level_nodes = levels[level - 1]
                    if(neighbor in upper_level_nodes):
                        predecessors_of_node.append(neighbor)
                        
            predecessors[node] = predecessors_of_node
                
    return predecessors

def get_nodes_label(graph, root):
    levels = get_levels(graph,root)
    predecessors = get_predecessors(graph, levels)
    nodes_credits = {root:1}

    for values in levels.values():
        for node in values:
            if(node != root):
                shortest_paths = 0
                for pre in predecessors[node]:
                    shortest_paths += nodes_credits[pre]
                nodes_credits[node] = shortest_paths    

    return nodes_credits
                    
G = nx.Graph([
    (1,2),
    (1,3),
    (2,3),
    (2,4),
    (3,5),
    (4,6),
    (4,7),
    (5,8),
    (5,9),
    (7,8),
    (6,7),
    (8,9)
])

G1 = nx.Graph([
    ('A','B'),
    ('B','C'),
    ('A','C'),
    ('B','D'),
    ('D','E'),
    ('D','F'),
    ('D','G'),
    ('G','F'),
    ('F','E'),
])


print(get_nodes_label(G1,'E'))

#levels = get_levels(G1,'E')
#print(levels)

# credits = get_nodes_credits(G,1)
# print(credits)
#print(dict(nx.bfs_predecessors(G, source=2)))
print(dict(nx.bfs_successors(G1, source='E')))

#c = nx.edge_betweenness_centrality(G)
#print (c)

#print(G.nodes)
#print(G.edges)
#nx.draw(G1)
#plt.show()