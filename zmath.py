import math

###############################################################################
# Translate Point
#   Translates the x and y along an angle and distance
#   Angle is expected in degrees since they will come from the player
#   Returns a tuple with the new x and y
def translatePoint(x,y,angle,distance):
    rad_angle = math.radians(angle)
    new_x = x + distance * math.cos(rad_angle)
    new_y = y + distance * math.sin(rad_angle)
    return (new_x,new_y)

###############################################################################
# Sign
#   Returns the sign of n. Used by other functions.
def sign(_n):
        return (_n > 0) - (_n < 0)

###############################################################################
# Distance
def distance(x0,y0,x1,y1):
    return math.sqrt(
        (x1-x0)**2 + (y1-y0)**2
    )

###############################################################################
# Get Cells Along a Trajector
#   Returns a list of cells (x,y) through which a line passes
#   on its way from A to B
#   NOTE: I am pretty sure this came from some internet source. It has been
#       passed down through several of my projects and I've lost the
#       original citation. Hats off to whomever wrote it.
def getCellsAlongTrajectory(x,y,angle,distance):

    A=(x,y)
    B=translatePoint(x,y,angle,distance)
    B = (int(B[0]),int(B[1]))

    D = (B[0]-A[0],B[1]-A[1])
    S = (sign(D[0]),sign(D[1]))
    GA = (math.floor(A[0]),math.floor(A[1]))
    GB = (math.floor(B[0]),math.floor(B[1]))
    (dx,dy) = GA

    traversed = [GA]

    tIx = D[1] * (dx + S[0] - A[0])
    tIy = D[0] * (dy + S[1] - A[1])

    if(D[0]==0):
        tIx = float('+inf')
    if(D[1]==0):
        tIy = float('+inf')

    while (dx,dy) != GB:
        movx = abs(tIx) <= abs(tIy)
        movy = abs(tIy) <= abs(tIx)

        if movx:
            dx += S[0]
            tIx = D[1] * (dx + S[0] - A[0])
        if movy:
            dy += S[1]
            tIy = D[0] * (dy + S[1] - A[1])

        traversed.append((dx,dy))

    return traversed