import numpy as np

from solve_for_flow import solve_for_flow
from plot_vessel_network import plot_vessel_network
from make_segments import make_segments
from cell_migration import cell_migration
from angle_theta import angle_theta


# Set random seed for reproducibility
np.random.seed(123456789)

# Input parameters
Nt = 40  # Number of time steps
Pin = 4 * 98  # Inlet pressure (Pa)
Pout = 1 * 98  # Outlet pressure (Pa)

mu = 3.5e-3  # Dynamic viscosity of blood (Pa-s)
Nn = 40  # Number of nodes
Nseg = 40  # Number of segments
num_cell = 10  # Initial number of cells per segment
cell_size = 5e-6  # Size of each cell (m)

# Segment directions
v1 = [0, 1]
v2 = [1, 0]
v3 = [0, -1]

branch_rule = int(input())

# Initialize the network
L = np.ones(Nseg) * 10e-6
Ncell = np.ones(Nseg) * num_cell  # Segment cell number array
D = np.zeros(Nseg)  # Segment diameters (m)
G = np.zeros(Nseg)  # Segment conductance array (m^4/Pa-s-m)

segments = make_segments(L)

def compute_conductance(Nseg, Ncell, cell_size, mu, L):
    D = np.zeros(Nseg)
    G = np.zeros(Nseg)
    for seg in range(Nseg):
        D[seg] = Ncell[seg] * cell_size / np.pi
        G[seg] = (np.pi * D[seg] ** 4) / (128 * mu * L[seg])
    return D, G

D, G = compute_conductance(Nseg, Ncell, cell_size, mu, L)

P, Q, tau = solve_for_flow(G, Ncell, Pin, Pout)
plot_vessel_network(segments, Q, Ncell, 0, None)

target = 0
if branch_rule == 1:
    if tau[34] > tau[14]:
        target = 34
    elif tau[34] < tau[14]:
        target = 14
elif branch_rule == 2:
    vector_35 = -np.array(v3)
    vector_34 = -np.array(v3)
    vector_14 = -np.array(v2)
    if angle_theta(vector_35, vector_34) < angle_theta(vector_35, vector_14):
        target = 34
    elif angle_theta(vector_35, vector_34) > angle_theta(vector_35, vector_14):
        target = 14

# Time step
for t in range(Nt):
    print(f'Time step {t + 1}/{Nt}')

    Ncell = cell_migration(Ncell, target)

    P, Q, tau = solve_for_flow(G, Ncell, Pin, Pout)

    # Plot only every 20 time steps
    if (t + 1) % 10 == 0:
        plot_vessel_network(segments, Q, Ncell, t+1, branch_rule)
