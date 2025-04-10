import numpy as np

def solve_for_flow(G, Ncell, Pin, Pout):
    """Solve for flow in the bifurcating vessel network."""
    Nseg = 40
    Nn = 40
    L = np.ones(Nseg) * 10e-6
    cell_size = 5e-6
    mu = 3.5e-3

    # Set very small values for zero conductance to avoid singular matrix errors
    G[G == 0] = 1e-25

    # Initialize matrices
    Q = np.zeros(Nseg)  # Segment flow array (m^3/s)
    C = np.zeros((Nn, Nn))  # Conductance matrix
    B = np.zeros(Nn)  # Solution vector

    node_map = [{} for _ in range(Nn)]
    for node in range(Nn):
        if node == 0:
            node_map[node] = {'upstream': None, 'downstream': [1]}
        elif node == 5:
            node_map[node] = {'upstream': [4], 'downstream': [6, 16]}
        elif node == 15:
            node_map[node] = {'upstream': [14, 34], 'downstream': [35]}
        elif node == 16:
            node_map[node] = {'upstream': [5], 'downstream': [17]}
        elif node == 34:
            node_map[node] = {'upstream': [33], 'downstream': [15]}
        elif node == 39:
            node_map[node] = {'upstream': [38], 'downstream': None}
        else:
            node_map[node] = {'upstream': [node - 1], 'downstream': [node + 1]}

    node_neighbor = [[] for _ in range(Nn)]
    for node in range(Nn):
        node_neighbor[node] = [node-1, node+1]
    node_neighbor[0] = [1]
    node_neighbor[39] = [38]
    node_neighbor[5] = [4,6,16]
    node_neighbor[15] = [14,34,35]

    seg_to_node = [[n, n + 1] for n in range(Nn)]
    seg_to_node[15] = [5, 16]
    seg_to_node[34] = [34, 15]

    # Set boundary conditions
    C[0, 0] = G[0] * 1
    B[0] = G[0] * Pin

    # Set equations for internal nodes
    for node in range(1, 39):
        upstream_nodes = node_map[node]['upstream']
        downstream_nodes = node_map[node]['downstream']
        neighboring_nodes = upstream_nodes + downstream_nodes
        for up_node in upstream_nodes:
            C[node, up_node] = - G[up_node]
        for down_node in downstream_nodes:
            C[node, down_node] = - G[node]
        C[node, node] = sum(G[n] for n in neighboring_nodes)

    # Set equation for last node
    C[39, 39] = G[38] * 1
    B[39] = G[38] * Pout

    # Solve for pressure
    P = np.linalg.solve(C, B)  # Nodal pressure array (Pa)

    # Compute segment flow rates
    for seg in range(Nseg):
        if seg == 0:
            Q[seg] = -G[seg] * (P[1] - Pin)
        elif seg == 39:
            Q[seg] = -G[seg] * (Pout - P[38])
        else:
            upstream_node = seg_to_node[seg][0]
            downstream_node = seg_to_node[seg][1]
            Q[seg] = -G[seg] * (P[downstream_node] - P[upstream_node])

    tau = np.zeros(Nseg)
    for seg in range(Nseg):
        if seg < len(L):   # Prevent out-range of index
            D_seg = (Ncell[seg] * cell_size) / np.pi
            if D_seg != 0:
                tau[seg] = (4 * mu * abs(Q[seg])) / (np.pi * (D_seg / 2) ** 3)
    return P, Q, tau
