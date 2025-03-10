import numpy as np
from scipy.interpolate import griddata

class steam():
    """
    The steam class is used to find thermodynamic properties of steam along an isobar.
    """
    def __init__(self, pressure, T=None, x=None, s=None, name=""):
        '''
        Constructor for steam properties
        '''
        self.p = pressure  # Pressure in kPa
        self.T = T  # Temperature in degrees C
        self.x = x  # Quality of steam
        self.s = s  # Entropy (kJ/(kg*K))
        self.name = name  # Identifier
        self.region = None  # 'superheated' or 'saturated'

        # Load tables
        self.sat_data = self.load_table("sat_water_table.txt", min_cols=8)
        self.superheat_data = self.load_table("superheated_water_table.txt", min_cols=4)

        # Calculate properties
        self.calc()

    def load_table(self, filename, min_cols):
        """ Load data safely from a file, handling errors. """
        try:
            data = np.genfromtxt(filename, delimiter="\t", skip_header=1, dtype=np.float64)
            if data.ndim == 1:  # If only one row, reshape
                data = data.reshape(1, -1)
            if data.shape[1] < min_cols:
                raise ValueError(f"{filename} has fewer than {min_cols} columns.")
            return data
        except Exception as e:
            raise ValueError(f"Error reading {filename}: {e}")

    def calc(self):
        '''
        Determine the thermodynamic state and interpolate properties.
        '''
        # Extract data columns
        ts, ps, hfs, hgs, sfs, sgs, vfs, vgs = self.sat_data.T
        tcol, hcol, scol, pcol = self.superheat_data[:, 0], self.superheat_data[:, 1], self.superheat_data[:, 2], self.superheat_data[:, 3]

        Pbar = self.p / 100  # Convert pressure to bar

        # Get saturated properties via interpolation
        Tsat = float(griddata(ps, ts, Pbar))
        hf = float(griddata(ps, hfs, Pbar))
        hg = float(griddata(ps, hgs, Pbar))
        sf = float(griddata(ps, sfs, Pbar))
        sg = float(griddata(ps, sgs, Pbar))
        vf = float(griddata(ps, vfs, Pbar))
        vg = float(griddata(ps, vgs, Pbar))

        self.hf = hf  # Store hf for reference

        # Determine region
        if self.T is not None:
            if self.T > Tsat:
                self.region = "Superheated"
                self.h = float(griddata((tcol, pcol), hcol, (self.T, self.p)))
                self.s = float(griddata((tcol, pcol), scol, (self.T, self.p)))
                self.x = 1.0
                self.v = 0.023507  # Approximation
            else:
                self.region = "Saturated"
                self.x = 1.0
                self.h = hg
                self.s = sg
                self.v = vg

        elif self.s is not None:  # Allow entropy as input
            self.region = "Saturated"
            self.T = Tsat
            self.h = float(griddata(ps, hfs, Pbar)) + (self.s - sf) * (hg - hf) / (sg - sf)
            self.x = (self.s - sf) / (sg - sf)
            self.v = vf + self.x * (vg - vf)

        elif self.x is not None:
            self.region = "Saturated"
            self.T = Tsat
            self.h = hf + self.x * (hg - hf)
            self.s = sf + self.x * (sg - sf)
            self.v = vf + self.x * (vg - vf)

    def print(self):
        """
        Prints a formatted report of steam properties.
        """
        print(f"Name:  {self.name}")
        print(f"Region:  {self.region}")
        print(f"{self.p:.2f} kPa")
        print(f"{self.T:.1f} degrees C")
        print(f"{self.h:.2f} kJ/kg")
        print(f"{self.s:.4f} kJ/(kg K)")
        print(f"{self.v:.6f} m^3/kg")
        print(f"{self.x:.4f}" if self.region == "Saturated" else "")
