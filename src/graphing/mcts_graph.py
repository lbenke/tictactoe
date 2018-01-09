"""
This module contains tools for visualising MCTS graphs using networkx.
"""

import networkx as nx
import networkx.drawing.nx_agraph as nxpgv
import datetime


def graph_mcts_tree(root_node, output_path=None, graph_type='dot',
        label_ratios=True, edge_ratios=False,
        highlight_moves=True, monochrome=False):
    """
    Generates a png file with a visualisation of the tree starting from the 
    given root node.
    
    Args:
        root_node (TreeNode): the root node of the tree
        output_path (string): optional path to output file, default is current 
            directory
        graph_type (string): graph layout to use when drawing, e.g. neato, dot, 
            twopi, circo, fdp, sfdp
        label_ratios: when true, an extra line is added to each node label with
            the score/visits ratio for that move
        edge_ratios: when true, a label is added to each edge with the 
            score/visits ratio for that move
        highlight_moves (bool): when true, a character in each node label is 
            highlighted to show the move represented by that node
        monochrome (bool): when true highlighted characters are bold, when false
            they are red                
    """
    # Create a networkx graph and add the nodes
    g = nx.DiGraph()
    build_graph(g, root_node, highlight_moves, monochrome,
            label_ratios, edge_ratios)

    # Create graphviz graph and set display attributes
    a = nxpgv.to_agraph(g)
    a.node_attr['fixedsize'] = 'true'
    a.node_attr['width'] = '1'
    a.node_attr['height'] = '1'
    a.node_attr['shape'] = 'square'
    a.node_attr['fontname'] = 'Courier New'
    a.node_attr['style'] = 'filled'
    a.node_attr['fillcolor'] = 'white'
    # a.graph_attr['bgcolor'] = 'transparent'
    # a.edge_attr['fontname'] = 'Courier New'
    a.layout(prog=graph_type)

    # Create the output file
    if output_path is None:
        st = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
        output_path = "tree_graph_{}_{}.png".format(st, graph_type)
    a.draw(output_path)


def build_graph(graph, tree_node, highlight_moves, monochrome,
        label_ratios, edge_ratios):
    """Recursively adds child nodes to the graph until terminal nodes are 
    reached."""
    # Create a new graph node from the tree node
    graph_node_label = create_label(tree_node, highlight_moves, monochrome,
            label_ratios)
    graph.add_node(tree_node.id, label=graph_node_label)

    # Add an edge from this node to its parent
    if tree_node.parent:
        ratio = str('%.3f' % round(tree_node.ratio(), 3)) if edge_ratios else ''
        graph.add_edge(tree_node.parent.id, tree_node.id, label=ratio)

    # Recursively add child nodes to the graph
    for child_node in tree_node.child_nodes.values():
        build_graph(graph, child_node, highlight_moves, monochrome,
                label_ratios, edge_ratios)


def create_label(tree_node, highlight_moves, monochrome, label_ratios):
    """Creates a label for the tree node, optionally including a ratio and using 
    HTML-like syntax to highlight the new move."""
    if tree_node.parent is None:
        # Plain-text label for the root node
        return tree_node.to_string()

    if not highlight_moves:
        # Plain-text label with optional ratio
        ratio = str('\n%.3f' % round(tree_node.ratio(), 3)) if label_ratios else ''
        return tree_node.to_string() + ratio

    # HTML-like label highlighting the new move
    graph_node_label = '<'
    # Compare the current node to its parent to identify and highlight the move
    tree_node_string = tree_node.to_string()
    parent_node_string = tree_node.parent.to_string()
    for i in range(len(tree_node_string)):
        if tree_node_string[i] == '\n':
            # Replace '\n' with '<br/>' since we are using HTML-like labels
            graph_node_label += '<br/>'
        elif tree_node_string[i] != parent_node_string[i]:
            if monochrome:
                graph_node_label += '<b>' + tree_node_string[i] + '</b>'
            else:
                graph_node_label += '<font color="red">' + tree_node_string[
                    i] + '</font>'
        else:
            graph_node_label += tree_node_string[i]
    if label_ratios:
        ratio = str('<br/>%.3f' % round(tree_node.ratio(), 3))
        graph_node_label += ratio
    graph_node_label += '>'
    return graph_node_label
