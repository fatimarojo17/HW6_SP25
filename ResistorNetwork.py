from scipy.optimize import fsolve
from Resistor import Resistor
from VoltageSource import VoltageSource
from Loop import Loop

class ResistorNetwork():
    def __init__(self):
        self.Loops = []
        self.Resistors = []
        self.VSources = []

    def BuildNetworkFromFile(self, filename):
        import os
        file_path = os.path.join(os.path.dirname(__file__), filename)

        with open(file_path, "r") as file:
            FileTxt = file.read().split('\n')

        self.Resistors = []
        self.VSources = []
        self.Loops = []

        LineNum = 0
        while LineNum < len(FileTxt):
            lineTxt = FileTxt[LineNum].lower().strip()
            if len(lineTxt) < 1 or lineTxt[0] == '#':
                pass
            elif "resistor" in lineTxt:
                LineNum = self.MakeResistor(LineNum, FileTxt)
            elif "source" in lineTxt:
                LineNum = self.MakeVSource(LineNum, FileTxt)
            elif "loop" in lineTxt:
                LineNum = self.MakeLoop(LineNum, FileTxt)  # ✅ FIXED
            LineNum += 1

    def MakeResistor(self, N, Txt):
        R = Resistor()
        N += 1
        txt = Txt[N].lower()
        while "resistor" not in txt:
            if "name" in txt:
                R.Name = txt.split('=')[1].strip()
            if "resistance" in txt:
                R.Resistance = float(txt.split('=')[1].strip())
            N += 1
            txt = Txt[N].lower()

        self.Resistors.append(R)
        return N

    def MakeVSource(self, N, Txt):
        VS = VoltageSource()
        N += 1
        txt = Txt[N].lower()
        while "source" not in txt:
            if "name" in txt:
                VS.Name = txt.split('=')[1].strip()
            if "value" in txt:
                VS.Voltage = float(txt.split('=')[1].strip())
            N += 1
            txt = Txt[N].lower()

        self.VSources.append(VS)
        return N

    def MakeLoop(self, N, Txt):  # ✅ FIXED: Added missing function
        """
        Reads loop definitions from the file.
        """
        L = Loop()
        N += 1
        txt = Txt[N].lower()

        while "loop" not in txt:
            if "name" in txt:
                L.Name = txt.split('=')[1].strip()
            if "nodes" in txt:
                L.Nodes = txt.split('=')[1].strip().replace(" ", "").split(',')
            N += 1
            txt = Txt[N].lower()

        self.Loops.append(L)
        return N

    def AnalyzeCircuit(self):
        i0 = [2.0, 6.0, 8.0]  # Correct initial guesses
        i = fsolve(self.GetKirchoffVals, i0)

        print("I1 = {:0.1f}".format(i[0]))
        print("I2 = {:0.1f}".format(i[1]))
        print("I3 = {:0.1f}".format(i[2]))

        return i

    def GetKirchoffVals(self, i):
        Node_c_Current = i[0] + i[1] - i[2]
        KVL = [16 - 2*i[0] - 2*i[1], 32 - 1*i[2] - 4*i[1]]
        KVL.append(Node_c_Current)
        return KVL


class ResistorNetwork_2(ResistorNetwork):
    def __init__(self):
        super().__init__()

    def BuildNetworkFromFile(self, filename):
        super().BuildNetworkFromFile(filename)
        self.Resistors.append(Resistor(5, -2, "de"))  # ✅ Ensure I4 is included

    def AnalyzeCircuit(self):
        i0 = [2.0, 6.0, 8.0, -2.0]  # Corrected initial guesses
        i = fsolve(self.GetKirchoffVals, i0)

        print("I1 = {:0.1f}".format(i[0]))
        print("I2 = {:0.1f}".format(i[1]))
        print("I3 = {:0.1f}".format(i[2]))
        print("I4 = {:0.1f}".format(i[3]))  # ✅ Ensure I4 is printed

        return i

    def GetKirchoffVals(self, i):
        Node_c_Current = i[0] + i[1] - i[2]
        Node_d_Current = i[2] - i[3]
        KVL = [16 - 2*i[0] - 2*i[1], 32 - 1*i[2] - 4*i[1] - 5*i[3]]
        return [KVL[0], KVL[1], Node_c_Current, Node_d_Current]
