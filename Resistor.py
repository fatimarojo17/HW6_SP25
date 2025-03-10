class Resistor():
    def __init__(self, R=1.0, i=0.0, name='ab'):
        """
        Defines a resistor to have a self.Resistance, self.Current, and self.Name.
        :param R: Resistance in Ohm (float)
        :param i: Current in Amps (float)
        :param name: Name of resistor by alphabetically ordered pair of node names
        """
        self.Resistance = R
        self.Current = i
        self.Name = name

    def DeltaV(self):
        """
        Calculates voltage change across resistor.
        :return: Voltage drop across resistor as a float
        """
        return self.Current * self.Resistance
