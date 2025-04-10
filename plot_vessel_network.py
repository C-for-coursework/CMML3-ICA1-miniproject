import numpy as np
import matplotlib.pyplot as plt

def plot_vessel_network(segments, Q, Ncell, t, branch_rule):
    plt.figure(figsize=(12, 6))
    if branch_rule != None:
        plt.title('Flow and Diameter of Network at t = {} using BR{}'.format(t, branch_rule))
    else:
        plt.title('Flow and Diameter of Network at t = {}'.format(t))

    cell_size = 5e-6

    d = np.zeros(40)
    for seg in range(40):
        d[seg] = (Ncell[seg] * cell_size) / np.pi

    # Plot all segments
    for seg in range(len(segments)):
        # Colored by flow direction
        color = "red" if Q[seg] > 0 else "blue"
        lwidth = d[seg] * 1e6 / 2  # Line width determined by diameter

        if seg == 15:
            start = segments[seg - 11]
            end = segments[seg + 1]
        elif seg == 35:
            start = segments[seg - 20]
            end = segments[seg]
        elif 36 <= seg < 40:
            start = segments[seg - 1]
            end = segments[seg]
        else:
            start = segments[seg]
            end = segments[seg + 1]
        plt.plot([start[0], end[0]], [start[1], end[1]], color=color, linewidth=lwidth)

    
    plt.grid()
    
    plt.show()
