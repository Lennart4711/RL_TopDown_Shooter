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


def line_line_intersection(line1, line2):
    x1, y1 = line1[0]  # Endpoint 1 of line 1
    x2, y2 = line1[1]  # Endpoint 2 of line 1
    x3, y3 = line2[0]  # Endpoint 1 of line 2
    x4, y4 = line2[1]  # Endpoint 2 of line 2

    # Calculate the denominator
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    # If the denominator is zero, the lines are parallel or coincident
    if denominator == 0:
        return None

    # Calculate the intersection point coordinates
    intersection_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
    intersection_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

    # Check if the intersection point lies within the line segments
    if (min(x1, x2) <= intersection_x <= max(x1, x2) and min(y1, y2) <= intersection_y <= max(y1, y2) and
            min(x3, x4) <= intersection_x <= max(x3, x4) and min(y3, y4) <= intersection_y <= max(y3, y4)):
        return intersection_x, intersection_y
    else:
        return None