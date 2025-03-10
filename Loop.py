class Loop():
    def __init__(self, Name, Pipes):  #  Make sure only two arguments are required
        '''
        Defines a loop in a pipe network.
        :param Name: name of the loop (string)
        :param Pipes: a list of Pipe objects that form the loop
        '''
        self.name = Name
        self.pipes = Pipes  #  Store the list of pipes correctly

    def getLoopHeadLoss(self):
        '''
        Calculates the net head loss as I traverse around the loop, in meters of fluid.
        :return: Total head loss in the loop.
        '''
        deltaP = 0  # Initialize head loss
        startNode = self.pipes[0].startNode  # Start at the first pipe's start node

        for p in self.pipes:
            phl = p.getFlowHeadLoss(startNode)
            deltaP += phl
            startNode = p.endNode if startNode != p.endNode else p.startNode  # Move to the next node

        return deltaP

