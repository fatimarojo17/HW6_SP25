# region imports
import math
import numpy as np
import random as rnd
from scipy.optimize import fsolve
from Fluid import Fluid  # ✅ Ensure Fluid is imported before use


# endregion
class Pipe():
    def __init__(self, Start='A', End='B', L=100, D=200, r=0.00025, fluid=None):
        if fluid is None:
            fluid = Fluid()

        self.startNode = min(Start, End)  # Ensure alphabetical order
        self.endNode = max(Start, End)
        self.length = L
        self.d = D / 1000.0  # Convert diameter from mm to meters
        self.r = r
        self.relrough = self.r / self.d
        self.A = math.pi / 4.0 * self.d**2
        self.Q = 10  # Initial guess in L/s
        self.fluid = fluid

    def oContainsNode(self, node):
        '''
        Checks if this pipe connects to a given node.
        :param node: The node name to check
        :return: True if this pipe is connected to the node, False otherwise.
        '''
        return self.startNode == node or self.endNode == node
    def Name(self):
        '''
        Returns the pipe name in "startNode-endNode" format.
        :return: A string representing the pipe name.
        '''
        return f"{self.startNode}-{self.endNode}"

    def findFlowRates(self):
        '''
        Finds flow rates in the pipe network using fsolve.
        '''
        N = len(self.pipes)  # ✅ Ensure it matches the number of pipes
        Q0 = np.full(N, 10)  # ✅ Create an array with exactly N elements

        def fn(q):
            for i in range(len(self.pipes)):
                self.pipes[i].Q = q[i]  # ✅ Ensure this index is always valid

            L = self.getNodeFlowRates()  # ✅ Ensure this returns exactly len(self.nodes) elements
            L += self.getLoopHeadLosses()  # ✅ Ensure this returns exactly len(self.loops) elements
            return L

        return fsolve(fn, Q0)  # ✅ Ensure Q0 size matches L size

    def getFlowIntoNode(self, node):
        '''
        Determines the flow rate into a given node.
        :param node: The node name to check
        :return: Flow rate (+) if entering the node, (-) if exiting
        '''
        if node == self.startNode:
            return -self.Q  # Flow exits the start node
        elif node == self.endNode:
            return self.Q  # Flow enters the end node
        return 0  # This shouldn't happen if the node is part of this pipe

