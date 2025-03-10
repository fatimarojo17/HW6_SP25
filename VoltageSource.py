class VoltageSource():
    def __init__(self, V=12.0, name='ab'):
        """
        Defines a voltage source in terms of self.Voltage and self.Name.
        """
        self.Voltage = V
        self.Name = name
