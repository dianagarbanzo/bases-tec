import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt 

def get_levels(graph, root):
    levels = {}
    level = 0
    current_level_nodes = [root]
    successors_by_node = dict(nx.bfs_successors(graph, root)) 

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
            if(predecessors_of_node):            
                predecessors[node] = predecessors_of_node
                
    return predecessors

def get_successors(graph, levels):
    successors = {}

    for level, nodes in levels.items():
        for node in nodes:
            neighbors_of_node = graph.neighbors(node)
            successors_of_node = []
            for neighbor in neighbors_of_node:
                down_level_nodes = levels.get(level + 1,[])
                if(neighbor in down_level_nodes):
                    successors_of_node.append(neighbor)
            if(successors_of_node):            
                successors[node] = successors_of_node
                
    return successors

def get_nodes_label(graph, root, levels, predecessors):
    nodes_credits = {root:1}

    for values in levels.values():
        for node in values:
            if(node != root):
                shortest_paths = 0
                for pre in predecessors[node]:
                    shortest_paths += nodes_credits[pre]
                nodes_credits[node] = shortest_paths    

    return nodes_credits

def is_leaf(node, successors):
    is_leaf = node not in successors
    return is_leaf

def get_parents_labels_sum(parents, labels):
    sum_parents_labels = 0 
    for parent in parents:
        sum_parents_labels += labels[parent] 
    return sum_parents_labels

def get_credits(levels, labels, successors, predecessors):
    nodes_credit = {}
    edges_credit = {}
    levels_from_buttom = reversed(list(levels.keys()))

    for level in levels_from_buttom:
        nodes = levels[level]
        for node in nodes:
            if(is_leaf(node, successors)):
                nodes_credit[node] = 1
                parents = predecessors.get(node,[])
                sum_parents_labels = 0
                sum_parents_labels = get_parents_labels_sum(parents, labels) 

                for parent in parents:
                    edge = tuple(sorted((parent,node)))
                    edges_credit[edge] = nodes_credit[node]*labels[parent]/sum_parents_labels

            else:
                credit = 1
                childs = successors.get(node,[])
                for child in childs:
                    edge = tuple(sorted((node,child)))
                    credit += edges_credit[edge] 
                nodes_credit[node] = credit

                parents = predecessors.get(node,[])
                sum_parents_labels = 0
                sum_parents_labels = get_parents_labels_sum(parents, labels) 

                for parent in parents:
                    edge = tuple(sorted((parent,node)))
                    edges_credit[edge] = nodes_credit[node]*labels[parent]/sum_parents_labels

    return nodes_credit, edges_credit

def find_keys_of_element(dictionary, search_element):
    result = []
    for key, value in dictionary.items():   
        if value == search_element:
            result.append(key)
    return result

G = nx.Graph([
    ('A','B'),
    ('A','C'),
    ('B','C'),
    ('B','H'),
    ('C','D'),
    ('H','I'),
    ('H','G'),
    ('D','E'),
    ('D','F'),
    ('G','E'),
    ('I','G'),
    ('E','F')
])

G1 = nx.Graph([
    ('A','B'),
    ('B','C'),
    ('A','C'),
    ('B','D'),
    ('D','E'),
    ('D','F'),
    ('D','G'),
    ('F','G'),
    ('F','E')
])


def calculate_betweeness(graph):
    betweeness = {}

    for root in graph.nodes:
        levels = get_levels(graph, root)
        predecessors_by_node = get_predecessors(graph, levels)
        successors_by_node = get_successors(graph, levels)
        labels_by_node = get_nodes_label(graph, root, levels, predecessors_by_node)
        edges_credit = get_credits(levels, labels_by_node, successors_by_node, predecessors_by_node)[1]

        for edge, credit in edges_credit.items():
            if edge in betweeness:
                betweeness[edge] += credit
            else:
                betweeness[edge] = credit

    for edge in betweeness.keys():
        betweeness[edge] = betweeness[edge]/2    

    return betweeness

def find_communities(graph, betweeness):
    list_of_betweennesses = list(betweeness.values())
    list_of_unique_betweennesses = list(set(list_of_betweennesses))
    list_of_unique_betweennesses.sort(reverse=True)
    current_number_of_communities = 1 

    for element in list_of_unique_betweennesses:
        
        element_keys = find_keys_of_element(betweeness, element)

        for edge in element_keys:

            graph.remove_edge(edge[0],edge[1])
            connected_components = list(sorted(nx.connected_components(graph), key = len, reverse=True))
            new_number_of_communities = len(connected_components)

            if (new_number_of_communities > current_number_of_communities):
                current_number_of_communities = new_number_of_communities
                yield connected_components
           

graph = G
betweeness = calculate_betweeness(graph)
print(betweeness)
c = find_communities(graph, betweeness)
print(next(c))
print(next(c))
print(next(c))

# communities_generator = community.girvan_newman(G)
# top_level_communities = next(communities_generator)
# next_level_communities = next(communities_generator)
# next2= next(communities_generator)
# print(sorted(map(sorted, top_level_communities)))
# print(sorted(map(sorted, next_level_communities)))
# print(sorted(map(sorted, next2)))