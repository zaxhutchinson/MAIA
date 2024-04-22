import math


def translate_point(x, y, angle, distance):
    """Translates the x and y along an angle and distance

    Angle is expected in degrees since they will come from the player
    """
    rad_angle = math.radians(angle)
    new_x = x + distance * math.cos(rad_angle)
    new_y = y + distance * math.sin(rad_angle)
    return (new_x, new_y)


def sign(_n):
    """Returns the sign of n"""
    return (_n > 0) - (_n < 0)


def distance(x0, y0, x1, y1):
    """Calculates distance between two points"""
    return math.sqrt((x1 - x0) ** 2.0 + (y1 - y0) ** 2.0)


def get_cells_along_trajectory(x, y, angle, distance):
    """Gets cells along trajectory given a start point, angle, and distance

    Z note: I am pretty sure this came from some internet source. It has been
    passed down through several of my projects and I've lost the
    original citation. Hats off to whomever wrote it.
    """
    A = (x, y)
    B = translate_point(x, y, angle, distance)
    B = (int(B[0]), int(B[1]))

    D = (B[0] - A[0], B[1] - A[1])
    S = (sign(D[0]), sign(D[1]))
    GA = (math.floor(A[0]), math.floor(A[1]))
    GB = (math.floor(B[0]), math.floor(B[1]))
    (dx, dy) = GA

    traversed = [GA]

    tIx = D[1] * (dx + S[0] - A[0])
    tIy = D[0] * (dy + S[1] - A[1])

    if D[0] == 0:
        tIx = float("+inf")
    if D[1] == 0:
        tIy = float("+inf")

    while (dx, dy) != GB:
        movx = abs(tIx) <= abs(tIy)
        movy = abs(tIy) <= abs(tIx)

        if movx:
            dx += S[0]
            tIx = D[1] * (dx + S[0] - A[0])
        if movy:
            dy += S[1]
            tIy = D[0] * (dy + S[1] - A[1])

        traversed.append((dx, dy))

    return traversed


def get_vector_to(x0, y0, x1, y1):
    """Get vector to"""
    bearing = math.degrees(math.atan2(y1 - y0, x1 - x0))
    if bearing < 0:
        bearing += 360
    return bearing
