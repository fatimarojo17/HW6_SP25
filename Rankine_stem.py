from Steam_stem import steam

class Rankine:
    def __init__(self, p_low=8, p_high=7350, x_high=0.9, name='Rankine Cycle'):
        self.p_low = p_low
        self.p_high = p_high
        self.x_high = x_high
        self.name = name
        self.efficiency = None
        self.turbine_work = 0
        self.pump_work = 0
        self.heat_added = 0

    def calc_efficiency(self):
        # State 1: Turbine inlet
        self.state1 = steam(self.p_high, x=self.x_high, name="Turbine Inlet")

        # State 2: Turbine exit (Now correctly handles entropy `s`)
        self.state2 = steam(self.p_low, s=self.state1.s, name="Turbine Exit")

        # State 3: Pump inlet (Saturated liquid)
        self.state3 = steam(self.p_low, x=0, name="Pump Inlet")

        # State 4: Pump exit
        self.state4 = steam(self.p_high, s=self.state3.s, name="Pump Exit")
        self.state4.h = self.state3.h + self.state3.v * (self.p_high - self.p_low)

        # Work and efficiency calculations
        self.turbine_work = self.state1.h - self.state2.h
        self.pump_work = self.state4.h - self.state3.h
        self.heat_added = self.state1.h - self.state4.h
        self.efficiency = 100.0 * (self.turbine_work - self.pump_work) / self.heat_added

        return self.efficiency

    def print_summary(self):
        print(f"Cycle: {self.name}, Efficiency: {self.efficiency:.2f}%")
