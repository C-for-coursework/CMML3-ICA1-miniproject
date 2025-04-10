import numpy as np

def angle_theta(a, b):
    '''Calculate the angle between two vectors'''
    a = np.array(a)
    b = np.array(b)
    
    # Dot product
    dot_product = np.dot(a, b)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    cos_theta = dot_product / (norm_a * norm_b)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)  # Float error
    return np.degrees(np.arccos(cos_theta))
