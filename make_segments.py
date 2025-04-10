import numpy as np

def make_segments(L):
    # Feeding vessel
    feeding = np.zeros((6, 2))

    for seg in range(5):
        feeding[seg + 1, 0] = 0
        feeding[seg + 1, 1] = np.sum(L[:seg + 1]) * 1e6

    # Proximal bifurcation
    proximal = np.zeros((11, 2))
    proximal[0, :] = feeding[5, :]

    for seg in range(6, 16):
        proximal[seg - 5, 0] = np.sum(L[5:seg]) * 1e6
        proximal[seg - 5, 1] = 50

    # Draining vessel
    draining = np.zeros((6, 2))  # Increased size to 6 rows
    draining[0, :] = proximal[10, :]

    for seg in range(35, 40):  # Adjusted range
        draining[seg - 34, 0] = 100
        draining[seg - 34, 1] = 50 - np.sum(L[34:seg]) * 1e6

    # Distal bifurcation
    dist1 = np.zeros((6, 2))
    dist1[0, :] = feeding[5, :]

    for seg in range(16, 21):
        dist1[seg - 15, 0] = 0
        dist1[seg - 15, 1] = 50 + np.sum(L[15:seg]) * 1e6

    dist2 = np.zeros((11, 2))
    dist2[0, :] = dist1[5, :]

    for seg in range(21, 31):
        dist2[seg - 20, 0] = np.sum(L[20:seg]) * 1e6
        dist2[seg - 20, 1] = 100

    dist3 = np.zeros((6, 2))  # Increased size to 6 rows
    dist3[0, :] = dist2[10, :]

    for seg in range(31, 36):  # Adjusted range
        dist3[seg - 30, 0] = 100
        dist3[seg - 30, 1] = 100 - np.sum(L[30:seg]) * 1e6

    distal = np.vstack((dist1, dist2[1:], dist3[1:]))

    segments = np.vstack((feeding, proximal[1:], distal[1:-1], draining[1:]))

    return segments