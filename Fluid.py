class Fluid():
    def __init__(self, mu=0.00089, rho=1000):
        '''
        Default properties are for water
        :param mu: dynamic viscosity in Pa*s
        :param rho: density in kg/m^3
        '''
        self.mu = mu  # Simply make a copy of the value in the argument as a class property
        self.rho = rho  # Simply make a copy of the value in the argument as a class property
        self.nu = mu / rho  # Calculate the kinematic viscosity in units of m^2/s
