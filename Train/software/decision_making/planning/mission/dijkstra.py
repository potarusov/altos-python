
class Node(object):
    def __init__(self, id, distance):
        self.id = id
        self.distance = distance
        self.parent = 1000

    def set_parent(self, parent):
        self.parent = parent

    def print_info(self):
        print(self.distance)
        print(self.parent)

class DijkstraPlanner:
    def __init__(self, adjacency_list):
        self.graph = []
        for i in range(len(adjacency_list)):
            self.graph.append(Node(i, 100000))
        self.adjacency_list = adjacency_list

    def plan(self, start_node_index):
        list = []
        start = self.graph[start_node_index]
        start.distance = 0
        list.append(start)

        while list:
            node_w_the_smallest_distance = 0
            current = list[node_w_the_smallest_distance].id
            for i in range(1, len(list)):
                if list[i].distance < list[node_w_the_smallest_distance].distance:
                    current = list[i].id
                    node_w_the_smallest_distance = i

            list.pop(node_w_the_smallest_distance)

            for i in range(0, len(self.adjacency_list[current])):
                child_index = self.adjacency_list[current][i]
                if self.graph[child_index].distance > self.graph[current].distance + 1:
                    self.graph[child_index].distance = self.graph[current].distance + 1
                    self.graph[child_index].parent = current
                    list.append(self.graph[child_index])

    def find_path(self, destination_node_index, origin_node_index):
        path = []
        node = self.graph[destination_node_index]
        while node.id != origin_node_index:
            path.append(node.id)
            node = self.graph[node.parent]

        #path.append(node.id)
        print(path)
        return path
