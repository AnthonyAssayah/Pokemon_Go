
class Edge:

    # Initialize a new edge
    def __init__(self, source=0, destination=0, weight=0.0):

        self.source = source
        self.destination = destination
        self.weight = weight

    # Return the source of the edge
    def get_source(self) -> int:
        return self.source

    # Change the source of the edge as new_source
    def set_source(self, new_source) -> None:
        self.source = new_source

    # Return the destination of the edge
    def get_destination(self) -> int:
        return self.destination

    # Change the destination of the edge as new_destination
    def set_destination(self, new_destination) -> None:
        self.destination = new_destination

    # Return the weight of the edge
    def get_weight(self) -> float:
        return self.weight

    # Change the weight of the edge as new_weight
    def set_weight(self, new_weight) -> None:
        self.weight = new_weight

    def __repr__(self) -> str:

        return str(self.weight)
