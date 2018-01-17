"""
This module contains tools for visualising MCTS graphs using networkx.
"""

import pygraphviz as pgv
import datetime


class MCTSGraph(object):
    """
    This class generates a pygraphviz AGraph from a tree, and outputs the graph
    in a number of formats.
    
    Example use:
    >> g = graphing.MCTSGraph(root_node=tree.root_node)
    >> g.draw_graph('output.png')

    Attributes:
        layout (string): graph layout to use when drawing, e.g. dot, neato,
            twopi, circo, fdp, sfdp
        node_ratios: when true, an extra line is added to each node label with
            the score/visits ratio for that move
        edge_ratios: when true, a label is added to each edge with the
            score/visits ratio for that move
        highlight_moves (bool): when true, a character in each node label is
            highlighted to show the move represented by that node
        highlights_coloured (bool): when true highlighted characters are red,
            when false they are bold
        sort_nodes (bool): when true the nodes in each rank are sorted by score
    """

    def __init__(self, root_node=None, layout='dot', node_ratios=True,
            edge_ratios=False, highlight_moves=True, highlights_coloured=False,
            fill_colours=True, edge_colours=True, border_colours=True,
            sort_nodes=True):
        """
        Constructor.
        
        Args:
            root_node (TreeNode): the root node of the tree; if a root node is 
                provided a new graph will be generated for it automatically, 
                otherwise generate_graph must be called separately
            output_path (string): optional path to output file, default is 
                current directory
            layout (string): graph layout to use when drawing, e.g. dot, neato,
                twopi, circo, fdp, sfdp
            node_ratios: when true, an extra line is added to each node label 
                with the score/visits ratio for that move
            edge_ratios: when true, a label is added to each edge with the
                score/visits ratio for that move
            highlight_moves (bool): when true, a character in each node label is
                highlighted to show the move represented by that node
            highlights_coloured (bool): when true highlighted characters are 
                red, when false they are bold
            sort_nodes (bool): when true the nodes in each rank are sorted by 
                score
        """
        self.layout = layout
        self.node_ratios = node_ratios
        self.edge_ratios = edge_ratios
        self.highlight_moves = highlight_moves
        self.highlights_coloured = highlights_coloured
        self.fill_colours = fill_colours
        self.edge_colours = edge_colours
        self.border_colours = border_colours
        self.sort_nodes = sort_nodes

        # Generate the AGraph if a tree node was provided
        self.agraph = self.generate_graph(root_node) if root_node else None

    def generate_graph(self, root_node):
        """
        Generates a pygraphviz AGraph from the tree defined by the given root 
        node.
        
        Args:
            root_node (TreeNode): the root node of the tree
                
        Returns:
            AGraph: the new AGraph of the tree
        """
        # Create a pygraphviz graph and add the nodes
        self.agraph = pgv.AGraph()
        self.__set_general_attrs()
        self.__build_graph(root_node)
        return self.agraph

    def draw_graph(self, path=None, format='png'):
        """
        Writes a representation of the graph to an output file in a specified
        format, e.g. png, jpg, fig, gv, pdf, svg, gif, ps.

        Args:
            path (string): the path to the output file; the format will 
                be guessed from the extension, otherwise the format argument 
                will be used
            format (string): the format of the output file, used only if the 
                format cannot be guessed from the extension of the output path
                
        Returns:
            str: the graph representation as raw data if no path was 
                specified, otherwise None
        """
        return self.agraph.draw(path=path, format=format, prog=self.layout)

    def __build_graph(self, tree_node):
        """Builds the AGraph by adding the tree node and any child nodes 
        recursively until terminal nodes are reached."""
        # Create a new graph node from the tree node and add it to the graph
        graph_node_label = self.__create_label(tree_node)
        self.agraph.add_node(tree_node.id, label=graph_node_label)

        # Add the edge from this node to its parent to the graph
        if tree_node.parent:
            ratio_label = ('%.3f' % round(tree_node.ratio(), 3) if
                    self.edge_ratios else '')
            self.agraph.add_edge(u=tree_node.parent.id, v=tree_node.id,
                    label=ratio_label)

        # Set the node and edge attributes
        self.__set_attrs(tree_node)

        # Sort the child nodes so they are rendered in order on the graph
        child_nodes = tree_node.child_nodes.values()
        if self.sort_nodes:
            child_nodes = sorted(child_nodes, key=lambda x: x.ratio())

        # Add any child nodes to the graph
        for child_node in child_nodes:
            self.__build_graph(child_node)

    def __set_general_attrs(self):
        """
        Set general graph display attributes.        
        See https://www.graphviz.org/doc/info/attrs.html
        """
        self.agraph.graph_attr['outputorder'] = 'edgesfirst'
        self.agraph.node_attr['fixedsize'] = 'true'
        self.agraph.node_attr['width'] = '1'
        self.agraph.node_attr['height'] = '1'
        self.agraph.node_attr['shape'] = 'square'
        self.agraph.node_attr['fontname'] = 'Courier New'
        self.agraph.node_attr['style'] = 'filled'
        self.agraph.node_attr['fillcolor'] = 'white'
        # self.agraph.node_attr['fillcolor'] = '0.0 0.0 0.96'
        # self.agraph.graph_attr['bgcolor'] = '0.0 0.0 0.96'
        # self.agraph.edge_attr['fontname'] = 'Courier New'
        # self.agraph.graph_attr['bgcolor'] = 'transparent'
        # self.agraph.graph_attr['splines'] = 'line'

    def __set_attrs(self, tree_node):
        """
        Set node and edge display attributes based on user preferences.
        See https://www.graphviz.org/doc/info/attrs.html
        """
        if self.fill_colours:
            node = self.agraph.get_node(tree_node.id)
            if tree_node.parent:
                # Map ratio to hue between green and red
                h = str(tree_node.ratio() / 3.0)
                s = 0.5 if self.edge_colours and not \
                        self.border_colours else 0.25
                node.attr['fillcolor'] = '{} {} {}'.format(h, s, 1.0)
            else:
                node.attr['fillcolor'] = 'white'

        if self.border_colours:
            node = self.agraph.get_node(tree_node.id)
            if tree_node.parent:
                # Map ratio to hue between green and red
                h = str(tree_node.ratio() / 3.0)
                node.attr['color'] = '{} {} {}'.format(h, 1.0, 1.0)
            else:
                node.attr['color'] = 'grey'

        if self.edge_colours:
            if tree_node.parent:
                # Map ratio to hue between green and red
                h = str(tree_node.ratio() / 3.0)
                edge = self.agraph.get_edge(tree_node.parent.id, tree_node.id)
                edge.attr['color'] = '{} {} {}'.format(h, 1.0, 1.0)
                if not self.border_colours:
                    edge.attr['penwidth'] = '3.0'

    def __create_label(self, tree_node):
        """Creates a label for the tree node, optionally including a ratio and 
        HTML-like syntax to highlight the new move."""
        if tree_node.parent is None:
            # Plain-text label for the root node
            return tree_node.to_string()

        if not self.highlight_moves:
            # Plain-text label with optional ratio
            ratio = ('\n%.3f' % round(tree_node.ratio(), 3) if
                    self.node_ratios else '')
            return tree_node.to_string() + ratio

        # HTML-like label highlighting the new move
        graph_node_label = '<'
        tree_node_string = tree_node.to_string()
        parent_node_string = tree_node.parent.to_string()
        for i in range(len(tree_node_string)):
            if tree_node_string[i] != parent_node_string[i]:
                # Character does not match parent so highlight it
                highlighted = ('<font color="red">{}</font>' if
                        self.highlights_coloured else '<b>{}</b>')
                graph_node_label += highlighted.format(tree_node_string[i])
            elif tree_node_string[i] == '\n':
                # Replace '\n' with '<br/>' since we are using HTML-like labels
                graph_node_label += '<br/>'
            else:
                graph_node_label += tree_node_string[i]
        if self.node_ratios:
            ratio = '<br/>%.3f' % round(tree_node.ratio(), 3)
            graph_node_label += ratio
        graph_node_label += '>'
        return graph_node_label
