import yaml

class Map:
    def __init__(self, map_filename):
        with open(map_filename, 'r') as stream:
            self.data_loaded = yaml.load(stream)

        self.nodes = self.data_loaded['nodes']
        for node in self.nodes:
            print(node)

        self.adjacency_list = []
        self.edges = self.data_loaded['edges']
        for label in self.edges:
            edge = []
            for child in label['children']:
                edge.append(child['label'])
                print("Node", label['label'], "is connected to node", child['label'])
            self.adjacency_list.append(edge)
        print(self.adjacency_list)

