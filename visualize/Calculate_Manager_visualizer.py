import sys
sys.path.append('../Calculate_Manager')
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

# http://pycallgraph.slowchop.com/en/master/
# usage: pycallgraph graphviz -- graph_example.py
with PyCallGraph(output=GraphvizOutput()):
    import Calculate_Manager
    Calculate_Manager.main()