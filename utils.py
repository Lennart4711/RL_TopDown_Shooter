import numpy as np


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def crossed_wall(wall: np.ndarray, trajectory: np.ndarray):
    # Return true if pos->pos+dx,dy crosses wall
    A = wall[0]
    B = wall[1]

    C = trajectory[0]
    D = trajectory[1]

    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
