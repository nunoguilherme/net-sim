import time
import logging
import tkinter as tk
from tkinter import messagebox

class Node:
    def __init__(self, name):
        self.name = name
        self.links = {}

    def connect(self, other_node, speed=1.0, latency=0.0):
        link = Link(self, other_node, speed, latency)
        self.links[other_node.name] = link
        other_node.links[self.name] = link

    def send_data(self, to_node, data, from_node=None):
        if to_node.name in self.links:
            link = self.links[to_node.name]
            link.send_data(self.name, to_node.name, data)
        else:
            for name, link in self.links.items():
                if from_node is None or name != from_node.name:
                    print(f"Node {self.name} forwarding data to {name}")
                    link.send_data(self.name, name, data)
                    break
                else:
                    print(f"No link to {to_node.name} exists")

    def receive_data(self, from_node, data):
        print(f"Node {self.name} received data: {data}")
        if data['dest'] != self.name:
            self.send_data(self.links[data['dest']].nodes[data['dest']], data, from_node=self)


class Link:
    def __init__(self, node1, node2, speed=1.0, latency=0.0):
        self.nodes = {node1.name: node1, node2.name: node2}
        self.capacity = 100
        self.speed = speed
        self.latency = latency

    def send_data(self, from_node, to_node, data):
        time.sleep(self.latency)  # Simulate latency
        if self.capacity > len(data):
            time.sleep(len(data) / self.speed)  # Simulate transmission time
            self.nodes[to_node].receive_data(from_node, data)
            self.capacity -= len(data)
        else:
            print("Link capacity exceeded")

    def reset_capacity(self):
        self.capacity = 100


def create_network():
    node_A = Node('A')
    node_B = Node('B')
    node_C = Node('C')

    node_A.connect(node_B, speed=2.0, latency=0.1)
    node_B.connect(node_C, speed=1.5, latency=0.05)

    data = {'source': 'A', 'dest': 'C', 'message': 'Hello from A'}
    node_A.send_data(node_C, data)

    node_A.links[node_B.name].reset_capacity()

    messagebox.showinfo("Network", "Network created successfully!")


logging.basicConfig(level=logging.INFO)


def main():
    root = tk.Tk()
    root.geometry("300x200")
    root.title("Network Simulator")

    button = tk.Button(root, text="Create Network", command=create_network)
    button.pack(fill='x', padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
