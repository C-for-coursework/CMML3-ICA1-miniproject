import numpy as np
import math

def cell_migration(Ncell, target):
    prop = 0.65  # Assume only 70% of the cells will migrate at each time step
    new_Ncell = Ncell.copy()

    Nseg = 40
    seg_map = [{} for _ in range(Nseg)]
    connections = {
        0: (None, [1]),
        4: ([3], [5, 15]),
        14: ([13], [35]),
        35: ([14, 35], [36]),
        39: ([38], None)
    }

    for seg in range(Nseg):
        if seg in connections:
            upstream, downstream = connections[seg]
        else:
            upstream = [seg - 1]
            downstream = [seg + 1]

        seg_map[seg] = {
            'upstream': upstream,
            'downstream': downstream
        }

    if target == 14:
        migrate = np.zeros(20)
        rest = list(range(15)) + list(range(35, 40))
        for seg in range(15, 35):
            if Ncell[seg] != 0:
                current_num = Ncell[seg]
                migrated = math.ceil(current_num * prop)
                new_Ncell[seg] -= migrated
                new_Ncell[seg_map[seg]['upstream'][0]] += migrated
                migrate[seg-15] += migrated
        for s in rest:
            new_Ncell[s] = Ncell[s] + migrate[0] / 20

    elif target == 34:
        migrate = np.zeros(10)
        rest = list(range(5)) + list(range(15, 40))
        for seg in range(5, 15):
            if Ncell[seg] != 0:
                if Ncell[seg] != 0:
                    current_num = Ncell[seg]
                    migrated = math.ceil(current_num * prop)
                    new_Ncell[seg] -= migrated
                    new_Ncell[seg_map[seg]['upstream'][0]] += migrated
                    migrate[seg - 5] += migrated
        for s in rest:
            new_Ncell[s] = Ncell[s] + migrate[0] / 30

    return new_Ncell