import math


def translate_point(x, y, angle, dist):
    """Translates the x and y along an angle and distance

    Angle is expected in degrees since they will come from the player
    """
    rad_angle = math.radians(angle)
    new_x = x + dist * math.cos(rad_angle)
    new_y = y + dist * math.sin(rad_angle)
    return new_x, new_y


def sign(_n):
    """Returns the sign of n"""
    return (_n > 0) - (_n < 0)


def distance(x0, y0, x1, y1):
    """Calculates distance between two points"""
    return math.sqrt((x1 - x0) ** 2.0 + (y1 - y0) ** 2.0)


def get_cells_along_trajectory(x, y, angle, dist):
    """Gets cells along trajectory given a start point, angle, and distance

    Z note: I am pretty sure this came from some internet source. It has been
    passed down through several of my projects and I've lost the
    original citation. Hats off to whomever wrote it.
    """
    ix = int(x)
    iy = int(y)
    path = [(ix, iy)]
    ex, ey = translate_point(x, y, angle, dist)
    while distance(x, y, ex, ey) > 0.001:
        x, y = translate_point(x, y, angle, 0.001)
        ix = int(x)
        iy = int(y)
        if (ix, iy) != path[-1]:
            path.append((ix, iy))

    return path
    # dx = int(ex) - int(x)
    # dy = int(ey) - int(y)
    # sx = sign(dx)
    # sy = sign(dy)
    # S = math.floor(x), math.floor(y)
    # E = math.floor(ex), math.floor(ey)
    # G = math.floor(x), math.floor(y)
    #
    # traversed = [G[:]]
    #
    # tx = dy * (G[0] + sx - S[0])
    # ty = dx * (G[1] + sy - S[1])
    #
    # if dx == 0:
    #     tx = float("+inf")
    # if dy == 0:
    #     ty = float("+inf")
    #
    # while G[0] != E[0] or G[1] != E[1]:
    #     mvx = abs(tx) <= abs(ty)
    #     mvy = abs(ty) <= abs(tx)
    #
    #     if mvx:
    #         G = (G[0] + sx, G[1])
    #         tx = dy * (G[0] + sx - x)
    #     if mvy:
    #         G = (G[0], G[1] + sy)
    #         ty = dx * (G[1] + sy - y)
    #
    #     if G != traversed[-1]:
    #         traversed.append(G[:])
    #
    # return traversed


def get_vector_to(x0, y0, x1, y1):
    """Get vector to"""
    bearing = math.degrees(math.atan2(y1 - y0, x1 - x0))
    if bearing < 0:
        bearing += 360
    return bearing
