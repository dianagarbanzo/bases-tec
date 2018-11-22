from pymongo import MongoClient
import networkx as nx

def GetMongoDBClient(client_url):
    client = MongoClient(client_url)
    return client

def ParseFromJsonToGraph(json_structure, id_name, connected_nodes_property_name):
    resultant_graph = nx.Graph()
    current_id = 0
    list_of_nodes = []
    list_of_edges = []
    list_of_connected_nodes = []
    edge = ()

    for node in json_structure:
        current_id =  str(node[id_name])

        list_of_nodes.append(current_id )
        list_of_connected_nodes = node[connected_nodes_property_name]
        
        for connected_node in list_of_connected_nodes:
            edge = (current_id, str(connected_node))
            list_of_edges.append(edge)

    resultant_graph.add_nodes_from(list_of_nodes)
    resultant_graph.add_edges_from(list_of_edges)

    return resultant_graph


def NxToMongoJSON(graph, filename):
    file = open(filename, "a")
    with open(filename, 'w') as file: 
        for node in graph.nodes:
            person = {'id':node}
            friends = [f for f in graph.neighbors(node)]
            person['friends'] = friends
            person_json = json.dumps(person)
            file.write(person_json + '\n') 
