from random import seed, random

from classes.Edge import Edge


class Node:

    # Initialize a new node
    def __init__(self, key, location):
        if location is None:
            seed()
            x = random() + 35  # as we got in the x values input
            y = random() + 32  # as we got in the y values input
            z = 0.0
            self.location = (x, y, z)
        else:
            self.location = location

        self.key = key
        self.info = ""
        self.tag = 0

        self._in = {}
        self._out = {}

    def __lt__(self, other):
        return self.tag < other.get_tag()

    def __gt__(self, other):
        return self.tag > other.get_tag()

    def __str__(self):
        return str(self.key)

    # Return the key of the node
    def get_key(self) -> int:
        return self.key

    # Change the key of the node to new_key
    def set_key(self, new_key) -> None:
        self.key = new_key

    # Return the info of the node
    def get_info(self) -> str:
        return self.info

    # Change the info of the node to new_key
    def set_info(self, new_info) -> None:
        self.info = new_info

    # Return the tag of the node
    def get_tag(self) -> int:
        return self.tag

    # Change the tag of the node to new_key
    def set_tag(self, new_tag) -> None:
        self.tag = new_tag

    # Return a dictionary of incoming edges of the node
    def get_in(self) -> dict:
        return self._in

    # Return a dictionary of outgoing edges of the node
    def get_out(self) -> dict:
        return self._out

    # Add a new node as the destination of a new edge
    def add_in(self, new_key, weight) -> None:
        self._in[new_key] = Edge(new_key, self.key, weight)

    # Add a new node as the source of a new edge
    def add_out(self, new_key, weight) -> None:
        self._out[new_key] = Edge(self.key, new_key, weight)

    # Return true iff,succeed to remove the node_data from the _in
    def remove_in(self, node_data: int) -> bool:
        if self._in.__contains__(node_data):
            self._in.pop(node_data)
            return True
        else:
            return False

    # Return true iff,succeed to remove the node_data from the _out
    def remove_out(self, node_data: int) -> bool:
        if self._out.__contains__(node_data):
            self._out.pop(node_data)
            return True
        else:
            return False

    # def __repr__(self) -> str:
    #
    #     return str(self.key) + ": |edges out| " + str(self._out.__len__()) + " |edges in| " + str(self._in.__len__())

    def __repr__(self) -> str:
        return str(self.key)
