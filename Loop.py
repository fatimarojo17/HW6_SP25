class Loop():
    def __init__(self, name=""):
        """
        Defines a loop with a name and a list of node names.
        """
        self.Name = name
        self.Nodes = []

    def __str__(self):
        """
        Returns a string representation of the loop.
        """
        return f"Loop {self.Name}: Nodes {self.Nodes}"

    def contains_node(self, node):
        """
        Checks if a given node is in this loop.
        :param node: (string) Node name to check.
        :return: (bool) True if node is in the loop, False otherwise.
        """
        return node in self.Nodes
