import sys
sys.path.append('../DATA_Manager')
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

# http://pycallgraph.slowchop.com/en/master/
# usage: pycallgraph graphviz -- graph_example.py
graphviz = GraphvizOutput()
graphviz.output_file = 'basic.png'
with PyCallGraph(output=GraphvizOutput()):
    import DATA_Manager
    DATA_Manager.main()