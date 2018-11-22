from pymongo import MongoClient
import networkx as nx
import matplotlib.pyplot as plt 

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

db_client = GetMongoDBClient('mongodb://localhost:27017')
db = db_client.test
json_data = db.red_social.find()
result = ParseFromJsonToGraph(json_data, 'id', 'friends')

nx.draw(result)
plt.show()