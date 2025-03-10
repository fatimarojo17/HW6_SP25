from ResistorNetwork import ResistorNetwork, ResistorNetwork_2

def main():
    resistor_network_file = "ResistorNetwork.txt"

    print("Network 1:")
    Net = ResistorNetwork()
    Net.BuildNetworkFromFile(resistor_network_file)
    Net.AnalyzeCircuit()

    print("\nNetwork 2:")
    Net_2 = ResistorNetwork_2()
    Net_2.BuildNetworkFromFile(resistor_network_file)
    Net_2.AnalyzeCircuit()

if __name__ == "__main__":
    main()
