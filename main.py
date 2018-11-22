import GirvanNewman as gn 
import NxToMongo as nm
import networkx as nx

#############################
########## Graphs demos #####
#############################

grafo_tarea = nx.Graph([
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

grafo_libro = nx.Graph([
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

random_graph = nx.random_geometric_graph(200, 0.125)

def main():
    db_client = nm.GetMongoDBClient('mongodb://localhost:27017')
    db = db_client.test
    json_data = db.red_social.find()
    result = nm.ParseFromJsonToGraph(json_data, 'id', 'friends')
    gn.girvan_newman(result, 2)

if __name__ == "__main__":
    main()

