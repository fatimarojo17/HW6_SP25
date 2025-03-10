# region imports
from Fluid import Fluid
from Pipe import Pipe
from Loop import Loop
from PipeNetwork import PipeNetwork
import importlib
import Loop
importlib.reload(Loop)
from Loop import Loop

# endregion

def main():
    water = Fluid()  # Instantiate a Fluid object (water)
    roughness = 0.00025  # Pipe roughness in meters

    PN = PipeNetwork([], [], [], water)  # Instantiate PipeNetwork object

    # Define pipe segments
    PN.pipes = [
        Pipe('a', 'b', 250, 300, roughness, water),
        Pipe('a', 'c', 100, 200, roughness, water),
        Pipe('b', 'e', 100, 200, roughness, water),
        Pipe('c', 'd', 125, 200, roughness, water),
        Pipe('c', 'f', 100, 150, roughness, water),
        Pipe('d', 'e', 125, 200, roughness, water),
        Pipe('d', 'g', 100, 150, roughness, water),
        Pipe('e', 'h', 100, 150, roughness, water),
        Pipe('f', 'g', 125, 250, roughness, water),
        Pipe('g', 'h', 125, 250, roughness, water)
    ]

    # Add Node objects to the pipe network
    PN.buildNodes()

    # Set external flow values for certain nodes
    PN.getNode('a').extFlow = 60
    PN.getNode('d').extFlow = -30
    PN.getNode('f').extFlow = -15
    PN.getNode('h').extFlow = -15

    # Ensure all pipes exist before adding to loops
    for name in ['a-b', 'b-e', 'd-e', 'c-d', 'a-c']:
        pipe = PN.getPipe(name)
        print(f"Retrieved pipe {name}: {pipe}")  # ✅ Should print valid Pipe objects
    # Define loops in the pipe network
    loop_pipes = [
        PN.getPipe('a-b'),
        PN.getPipe('b-e'),
        PN.getPipe('d-e'),
        PN.getPipe('c-d'),
        PN.getPipe('a-c')
    ]
    print("Loop A is being created with pipes:", loop_pipes)
    PN.loops.append(Loop('A', loop_pipes))

    # Compute flow rates
    PN.findFlowRates()

    # Output results
    PN.printPipeFlowRates()
    print("\nCheck node flows:")
    PN.printNetNodeFlows()
    print("\nCheck loop head loss:")
    PN.printLoopHeadLoss()
print(f"Loop class definition: {Loop.__init__.__code__.co_varnames}")


if __name__ == "__main__":
    main()
