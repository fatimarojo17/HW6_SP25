#region imports
from scipy.optimize import fsolve
import numpy as np
from Fluid import Fluid  # ✅ Import Fluid class before using it
from Node import Node
#endregion

# region class definitions

class PipeNetwork():
    def __init__(self, Pipes=[], Loops=[], Nodes=[], fluid=Fluid()):
        self.loops = Loops
        self.nodes = Nodes
        self.Fluid = fluid
        self.pipes = Pipes

    def findFlowRates(self):
        '''
        Finds flow rates in the pipe network using fsolve.
        '''
        N = len(self.pipes)  # Ensure Q0 matches the number of pipes
        Q0 = np.full(N, 10)  #  Initial guess for all pipes

        def fn(q):
            for i in range(len(self.pipes)):
                self.pipes[i].Q = q[i]  # Ensure this index is always valid

            L = self.getNodeFlowRates()  #  Ensure this returns exactly len(self.nodes) elements
            L += self.getLoopHeadLosses()  #  Ensure this returns exactly len(self.loops) elements
            return L

        return fsolve(fn, Q0)  #  Ensure Q0 size matches L size

    #region methods
    def buildNodes(self):
        '''
        Automatically builds nodes based on the pipes.
        Ensures each node is created only once.
        '''
        node_names = set()  # Keep track of node names

        for pipe in self.pipes:
            if pipe.startNode not in node_names:
                self.nodes.append(Node(pipe.startNode, self.getNodePipes(pipe.startNode)))
                node_names.add(pipe.startNode)
            if pipe.endNode not in node_names:
                self.nodes.append(Node(pipe.endNode, self.getNodePipes(pipe.endNode)))
                node_names.add(pipe.endNode)

    def getNodePipes(self, node):
        '''
        Returns a list of pipes connected to a node.
        '''
        return [p for p in self.pipes if p.oContainsNode(node)]

    def getNode(self, name):
        '''
        Returns a node object by its name.
        '''
        for n in self.nodes:
            if n.name == name:
                return n
        return None

    def getPipe(self, name):
        for p in self.pipes:
            if p.Name() == name:
                return p
        return None

    def getNodeFlowRates(self):
        qNet = [n.getNetFlowRate() for n in self.nodes]
        print(f" Node Flow Rates = {qNet}")  # ✅ Debugging output
        return qNet

    def getLoopHeadLosses(self):
        lhl = [l.getLoopHeadLoss() for l in self.loops]
        print(f" Loop Head Losses = {lhl}")  # ✅ Debugging output
        return lhl
