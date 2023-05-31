
class Node:
    def __init__(self, name):
        self.name = name
        self.links = {}

    def connect(self, other_node):
        link = Link(self, other_node)
        self.links[other_node.name] = link
        other_node.links[self.name] = link

    def send_data(self, to_node, data):
        if to_node.name in self.links:
            link = self.links[to_node.name]
            link.send_data(self.name, to_node.name, data)
        else:
            print(f"No link to {to_node.name} exists")

    def receive_data(self, data):
        print(f"Node {self.name} received data: {data}")

 # Path: link.py

class Link:
    def __init__(self, node1, node2):
        self.nodes = {node1.name: node1, node2.name: node2}
        self.capacity = 100  # for example

    def send_data(self, from_node, to_node, data):
        if self.capacity > len(data):
            self.nodes[to_node].receive_data(data)
            self.capacity -= len(data)
        else:
            print("Link capacity exceeded")

    def reset_capacity(self):
        self.capacity = 100

def main():
    # Creating nodes >> A and B
    node_A = Node('A')
    node_B = Node('B')

    # Establishing a connection between both nodes!
    node_A.connect(node_B)

    # Sending data here
    node_A.send_data(node_B, 'Hello from A')

    # Resetting link capacity back to normal
    node_A.links[node_B.name].reset_capacity()

if __name__ == "__main__":
    main()
