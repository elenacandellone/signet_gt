import numpy as np
import graph_tool.all as gt

class SignedNetwork:
    def __init__(self):
        self.nodes = None
        self.edges = None
        self.graph = None

    def graph_construction(self, repre, repre_type='adj', is_directed=False, nodes_id=None, weights=None):
        """
        Constructs a signed network from the adjacency matrix or the edge list.

        Parameters:
            repre (numpy.ndarray or list of tuples): The input representation of the graph.
            repre_type (str): The type of representation ('adj' for adjacency matrix, 'edgelist' for edge list).
            is_directed (bool): True if the graph is directed, False otherwise.
            nodes_id (list or None): The IDs of nodes in the graph.
            weights (list or None): The weights of edges in the graph.

        Returns:
            gt.Graph: The graph constructed from the input representation.
        """
        if repre_type == 'adj':
            # UNDIRECTED
            if not is_directed:
                A = np.triu(repre)  # Convert the input adjacency matrix to upper triangular to avoid duplicate edges

            # DIRECTED    
            else:
                A = np.array(repre)

            edge_list = np.transpose(A.nonzero())  # Get the edgelist from the adjacency matrix
            weights = A[A.nonzero()]  # Get the non-zero elements as edge weights

        elif repre_type == 'edgelist':

            # UNDIRECTED
            if not is_directed:
                A = np.triu(repre)  # Convert the input adjacency matrix to upper triangular to avoid duplicate edges

            # DIRECTED    
            else:
                A = np.array(repre)
            edge_list = repre

            if weights is None:
                raise ValueError('Please provide edge weights')  # Raise an exception for missing edge weights

        else:
            raise ValueError('Please choose between adj and edgelist')  # Raise an exception for an invalid representation type

        self.edges = edge_list

        # Construct the graph
        self.graph = gt.Graph(directed=is_directed)
        self.graph.add_edge_list(edge_list)

        # Add weights and colours as an edge property map
        self.graph.ep['weight'] = self.graph.new_edge_property(value_type="double", vals=weights)
        self.graph.ep['color'] = self.graph.new_edge_property(value_type="string", vals=['#42BFDD' if w > 0 else '#F24333' for w in weights])

        if nodes_id:
            # Node IDs
            self.graph.vp["node_id"] = self.graph.new_vertex_property(value_type="string", vals=nodes_id)
            self.nodes = nodes_id
        else:
            print('warning: no node IDs assigned, default indexes are used')
            self.graph.vp["node_id"] = self.graph.new_vertex_property(value_type="string", vals=self.graph.get_vertices())
            self.nodes = self.graph.get_vertices()

        return self.graph