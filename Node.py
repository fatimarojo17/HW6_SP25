class Node():
    def __init__(self, Name='a', Pipes=[], ExtFlow=0):
        self.name = Name
        self.pipes = Pipes
        self.extFlow = ExtFlow

    def getNetFlowRate(self):
        Qtot = self.extFlow  # Count the external flow first
        for p in self.pipes:
            Qtot += p.getFlowIntoNode(self.name)  # Retrieve pipe flow rate
        return Qtot
