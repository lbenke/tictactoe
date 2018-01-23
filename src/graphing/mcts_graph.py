"""
This module contains tools for visualising MCTS trees using Graphviz.
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
        root_node (TreeNode): the root node of the tree
        layout (string): graph layout to use when drawing, e.g. dot, neato,
            twopi, circo, fdp, sfdp
        node_scores: when true, an extra line is added to each node label with
            the score for that move
        edge_scores: when true, a label is added to each edge with the score for
            that move
        highlight_moves (bool): when true, a character in each node label is
            highlighted to show the move represented by that node
        highlights_coloured (bool): when true highlighted characters are red,
            when false they are bold
        fill_colours (bool): sets whether nodes are coloured by score
        edge_colours (bool): sets whether edges are coloured by score
        border_colours (bool): sets whether borders are coloured by score
        sort_nodes (bool): when true the nodes in each rank are sorted by score
        verbose_score (bool): when true scores are displayed in the form 
            wins/visits
        transparent (bool): when true the background is set to transparent
    """

    def __init__(self, root_node=None, layout='dot', node_scores=True,
            edge_scores=False, highlight_moves=True, highlights_coloured=False,
            fill_colours=True, edge_colours=True, border_colours=True,
            sort_nodes=True, verbose_score=True, transparent=False):
        """
        Constructor.
        
        Args:
            root_node (TreeNode): the root node of the tree; if a root node is 
                provided a new graph will be generated for it automatically, 
                otherwise generate_graph must be called separately
            layout (string): graph layout to use when drawing, e.g. dot, neato,
                twopi, circo, fdp, sfdp
            node_scores: when true, an extra line is added to each node label 
                with the score for that move
            edge_scores: when true, a label is added to each edge with the score
                for that move
            highlight_moves (bool): when true, a character in each node label is
                highlighted to show the move represented by that node
            highlights_coloured (bool): when true highlighted characters are 
                red, when false they are bold
            fill_colours (bool): sets whether nodes are coloured by score
            edge_colours (bool): sets whether edges are coloured by score
            border_colours (bool): sets whether borders are coloured by score
            sort_nodes (bool): when true the nodes in each rank are sorted by 
                wins
            verbose_score (bool): when true scores are displayed in the form 
                wins/visits
            transparent (bool): when true the background is set to transparent            
        """
        self.root_node = root_node
        self.layout = layout
        self.node_scores = node_scores
        self.edge_scores = edge_scores
        self.highlight_moves = highlight_moves
        self.highlights_coloured = highlights_coloured
        self.fill_colours = fill_colours
        self.edge_colours = edge_colours
        self.border_colours = border_colours
        self.sort_nodes = sort_nodes
        self.verbose_score = verbose_score
        self.transparent = transparent

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
            score_label = ('{0:.3f}'.format(round(tree_node.score(), 3)) if
                    self.edge_scores else '')
            self.agraph.add_edge(u=tree_node.parent.id, v=tree_node.id,
                    label=score_label)

        # Set the node and edge attributes
        self.__set_attrs(tree_node)

        # Sort the children of this node so they are rendered in order of score
        child_nodes = tree_node.child_nodes.values()
        if self.sort_nodes:
            child_nodes = sorted(child_nodes, key=lambda x: x.score())

        # Add any child nodes to the graph
        for child_node in child_nodes:
            self.__build_graph(child_node)

    def __set_general_attrs(self):
        """
        Set general graph display attributes.        
        See https://www.graphviz.org/doc/info/attrs.html
        """
        if self.transparent:
            self.agraph.graph_attr['bgcolor'] = 'transparent'
        self.agraph.node_attr['fixedsize'] = 'true'
        if self.verbose_score and self.node_scores:
            self.agraph.node_attr['width'] = '1.35'
            self.agraph.node_attr['height'] = '1.35'
        else:
            self.agraph.node_attr['width'] = '1'
            self.agraph.node_attr['height'] = '1'
            self.agraph.graph_attr['outputorder'] = 'edgesfirst'
        self.agraph.node_attr['shape'] = 'square'
        self.agraph.node_attr['fontname'] = 'Courier New'
        self.agraph.node_attr['style'] = 'filled'
        self.agraph.node_attr['fillcolor'] = 'white'
        self.agraph.edge_attr['fontname'] = 'Courier New'
        self.agraph.edge_attr['fontsize'] = '10'

    def __set_attrs(self, tree_node):
        """Set individual node and edge display attributes based on user 
        preferences."""
        if self.fill_colours:
            node = self.agraph.get_node(tree_node.id)
            if tree_node.parent:
                # Map score to hue between green and red
                h = str(tree_node.score() / 3.0)
                s = 0.5 if self.edge_colours and not \
                        self.border_colours else 0.25
                node.attr['fillcolor'] = '{} {} {}'.format(h, s, 1.0)
            else:
                node.attr['fillcolor'] = 'white'

        if self.border_colours:
            node = self.agraph.get_node(tree_node.id)
            if tree_node.parent:
                # Map score to hue between green and red
                h = str(tree_node.score() / 3.0)
                node.attr['color'] = '{} {} {}'.format(h, 1.0, 1.0)
            else:
                node.attr['color'] = 'grey'

        if self.edge_colours:
            if tree_node.parent:
                # Map score to hue between green and red
                h = str(tree_node.score() / 3.0)
                edge = self.agraph.get_edge(tree_node.parent.id, tree_node.id)
                edge.attr['color'] = '{} {} {}'.format(h, 1.0, 1.0)
                if not self.border_colours:
                    edge.attr['penwidth'] = '3.0'

    def __create_label(self, tree_node):
        """Creates a label for the tree node, optionally including score details
        and highlighting the new move represented by the node."""
        graph_node_label = '<'

        # Add the node state to the label with highlighting if required
        tree_node_str = str(tree_node).replace('\n', '<br/>')
        if self.highlight_moves and tree_node.parent:
            parent_node_str = str(tree_node.parent).replace('\n', '<br/>')
            graph_node_label += self.__highlight_differences(
                    tree_node_str, parent_node_str)
        else:
            graph_node_label += tree_node_str

        # Add scores to the label if required
        if self.node_scores and tree_node.parent:
            score = '{0:.3f}'.format(round(tree_node.score(), 3))
            if self.verbose_score:
                graph_node_label += '<br/><font point-size="10">Wins: {}' \
                        '<br/>Visits: {}<br/>Score: {}'.format(
                        float(tree_node.wins), tree_node.visits, score)
                if (hasattr(tree_node, 'ucb1_score') and
                        tree_node.ucb1_score is not None):
                    ucb1 = '{0:.3f}'.format(round(tree_node.ucb1_score, 3))
                    graph_node_label += '<br/>UCB1: {}'.format(ucb1)
                graph_node_label += '</font>'
            else:
                graph_node_label += '<br/>{}'.format(score)

        graph_node_label += '>'

        return graph_node_label

    def __highlight_differences(self, string1, string2):
        """Highlights any characters that differ between two strings."""
        highlighted_str = ""
        for i in range(len(string1)):
            if string1[i] != string2[i]:
                # Character does not match parent so highlight it
                if self.highlights_coloured:
                    highlighted = '<font color="red">{}</font>'
                else:
                    highlighted = '<b>{}</b>'
                highlighted_str += highlighted.format(string1[i])
            else:
                highlighted_str += string1[i]
        return highlighted_str
