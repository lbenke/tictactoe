"""
This module contains tools for visualising MCTS graphs using networkx.
"""

import pygraphviz as pgv
import datetime


def graph_mcts_tree(root_node, output_path=None, layout='dot',
        label_ratios=True, edge_ratios=False, highlight_moves=True,
        monochrome=True, fill_colours=True, edge_colours=True,
        border_colours=True, filetype='png'):
    """
    Generates a png file with a visualisation of the tree starting from the 
    given root node.
    
    Args:
        root_node (TreeNode): the root node of the tree
        output_path (string): optional path to output file, default is current 
            directory
        layout (string): graph layout to use when drawing, e.g. dot, neato, 
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
    # Create a pygraphviz graph and add the nodes
    agraph = pgv.AGraph()
    build_graph(agraph, root_node, highlight_moves, monochrome,
        label_ratios, edge_ratios, fill_colours, edge_colours, border_colours)

    # Set general display attributes
    agraph.graph_attr['outputorder'] = 'edgesfirst'
    agraph.node_attr['fixedsize'] = 'true'
    agraph.node_attr['width'] = '1'
    agraph.node_attr['height'] = '1'
    agraph.node_attr['shape'] = 'square'
    agraph.node_attr['fontname'] = 'Courier New'
    agraph.node_attr['style'] = 'filled'
    agraph.node_attr['fillcolor'] = 'white'
    # agraph.node_attr['fillcolor'] = '0.0 0.0 0.96'
    # agraph.graph_attr['bgcolor'] = '0.0 0.0 0.96'
    # agraph.edge_attr['fontname'] = 'Courier New'
    # agraph.graph_attr['bgcolor'] = 'transparent'
    # agraph.graph_attr['splines'] = 'line'
    agraph.layout(prog=layout)

    # Create the output file
    if output_path is None:
        st = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
        output_path = "tree_graph_{}_{}.{}".format(st, layout, filetype)
    agraph.draw(output_path)


def build_graph(graph, tree_node, highlight_moves, monochrome,
        label_ratios, edge_ratios, fill_colours, edge_colours, border_colours):
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

    if fill_colours:
        node = graph.get_node(tree_node.id)
        if tree_node.parent:
            if edge_colours and not border_colours:
                node.attr['fillcolor'] = str(
                    tree_node.ratio() / 3.0) + ' 0.5 1.0'
            else:
                node.attr['fillcolor'] = str(
                    tree_node.ratio() / 3.0) + ' 0.25 1.0'
        else:
            node.attr['fillcolor'] = 'white'

    if border_colours:
        if tree_node.parent:
            node = graph.get_node(tree_node.id)
            node.attr['color'] = str(tree_node.ratio() / 3.0) + ' 1.0 1.0'
        else:
            node.attr['color'] = '0.0 0.0 0.5'

    if edge_colours:
        if tree_node.parent:
            edge = graph.get_edge(tree_node.parent.id, tree_node.id)
            edge.attr['color'] = str(tree_node.ratio() / 3.0) + ' 1.0 1.0'
            if not border_colours:
                edge.attr['penwidth'] = '3.0'

    # Sort the child nodes so they are rendered in LR order on the graph
    child_nodes = tree_node.child_nodes.values()
    child_nodes.sort(key=lambda x: x.ratio(), reverse=True)

    # Recursively add child nodes to the graph
    for child_node in child_nodes:
        build_graph(graph, child_node, highlight_moves, monochrome,
                label_ratios, edge_ratios, fill_colours, edge_colours,
                border_colours)


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
        if tree_node_string[i] != parent_node_string[i]:
            if monochrome:
                graph_node_label += '<b>' + tree_node_string[i] + '</b>'
            else:
                graph_node_label += '<font color="red">' + tree_node_string[i] \
                        + '</font>'
        elif tree_node_string[i] == '\n':
            # Replace '\n' with '<br/>' since we are using HTML-like labels
            graph_node_label += '<br/>'
        else:
            graph_node_label += tree_node_string[i]
    if label_ratios:
        ratio = str('<br/>%.3f' % round(tree_node.ratio(), 3))
        graph_node_label += ratio
    graph_node_label += '>'
    return graph_node_label
