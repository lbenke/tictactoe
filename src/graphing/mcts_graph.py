import networkx as nx
import pygraphviz as pgv
import networkx.drawing.nx_agraph as nxpgv
import rules
import datetime


def graph_mcts_tree(root_node):
    # Create a networkx graph and add the nodes
    g = nx.DiGraph()
    root_state = rules.board_str(root_node.state)
    g.add_node(root_state)
    for child in root_node.child_nodes.values():
        child_state = rules.board_str(child.state) + "\n" + str('%.3f' % round(child.ratio(), 3))
        g.add_edge(root_state, child_state)

    # Create a graphviz graph and set display attributes
    a = nxpgv.to_agraph(g)
    # a.graph_attr['bgcolor'] = 'transparent'
    a.node_attr['fontname'] = 'Courier New'
    a.node_attr['style'] = 'filled'
    a.node_attr['fillcolor'] = 'white'
    a.node_attr['fixedsize'] = 'true'
    a.node_attr['width'] = '1'
    a.node_attr['height'] = '1'
    a.node_attr['shape'] = 'square'
    a.layout(prog='dot')
    # a.layout(prog='circo')
    # a.layout()

    st = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    a.draw("tree_dot_{}.png".format(st))

    # print a.string()
