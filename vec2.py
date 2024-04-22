import math


class Vec2:
    """This class is currently depreciated and is not in use"""

    def __init__(self, _x, _y):
        """Initializes x and y from associated parameters"""
        self.x = int(_x)
        self.y = int(_y)

    def __eq__(self, other):
        """Determines if two vectors are equivalent"""
        if isinstance(other, Vec2):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __str__(self):
        """Converts x and y to string format"""
        return str(self.x) + "," + str(self.y)

    def get_x(self):
        """Gets x"""
        return self.x

    def get_y(self):
        """Gets y"""
        return self.y

    def set_x(self, _x):
        """Sets x"""
        self.x = _x

    def set_y(self, _y):
        """Sets y"""
        self.y = _y

    def intersects_line_seg(self, lineseg):
        """Determines if vector intersects a line"""
        return lineseg.intersects_point(self)

    def distance_to_point(self, other_vec):
        """Calculates shortest distance to point from vector"""
        return math.sqrt(
            math.pow(other_vec.get_x() - self.x, 2.0)
            + math.pow(other_vec.get_y() - self.y, 2.0)
        )

    # Borrowed from:
    #   https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
    def distance_to_line_seg(self, lseg):
        """Calculates shortest distance to line from vector"""
        #    return abs(
        #        l[0]*self.x + self.y + l[1]
        #    ) / math.sqrt(
        #        l[0]**2 + 1
        #    )
        A = self.x - lseg.v1.get_x()
        B = self.y - lseg.v1.get_y()
        C = lseg.v2.get_x() - lseg.v1.get_x()
        D = lseg.v2.get_y() - lseg.v1.get_y()

        DOT = A * C + B * D
        LEN_SQ = C * C + D * D
        PARAM = -1

        if LEN_SQ != 0:
            PARAM = DOT / LEN_SQ

        XX = 0
        YY = 0
        if PARAM < 0:
            XX = lseg.v1.get_x()
            YY = lseg.v1.get_y()
        elif PARAM > 1:
            XX = lseg.v2.get_x()
            YY = lseg.v2.get_y()
        else:
            XX = lseg.v1.get_x() + PARAM * C
            YY = lseg.v1.get_y() + PARAM * D

        DX = self.x - XX
        DY = self.y - YY

        return math.sqrt(DX * DX + DY * DY)

    def line_eq_from_angle(self, angle):
        """Calculates line equation from angle"""
        m = math.tan(angle)
        n = self.y - m * self.x
        return (m, n)

    def get_point_at_distance_and_angle(self, angle, distance):
        """Gets point at distance and angle"""
        self.x = self.x + distance * math.cos(angle)
        self.y = self.y + distance * math.sin(angle)

    def move(self, angle, distance):
        """Moves vector given angle and distance"""
        self.x = self.x + distance * math.cos(angle)
        self.y = self.y + distance * math.sin(angle)

    # Borrowed from:
    #   https://stackoverflow.com/questions/2259476/rotating-a-point-about-another-point-2d
    #
    def rotate_around_point(self, angle, point):
        """Rotates vector around point"""
        S = math.sin(angle)
        C = math.cos(angle)

        self.x = self.x - point.x
        self.y = self.y - point.y
        x_new = self.x * C - self.y * S
        y_new = self.x * S + self.y * C

        self.x = x_new + point.x
        self.y = y_new + point.y
