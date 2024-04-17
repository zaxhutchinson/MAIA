from vec2 import Vec2


class LineSeg:
    def __init__(self, v1, v2):
        """Sets start and end points"""
        self.v1 = v1
        self.v2 = v2

    def itersects_point(self, point):
        """Determines if line intersects a point"""
        if self.v1.get_x() == self.v2.get_x():
            return self.v1.get_x() == point.get_x()
        elif self.v1.get_y() == self.v2.get_y():
            return self.v1.get_y() == point.get_y()
        else:
            return (point.get_y() - self.v1.get_y()) / (
                self.v2.get_y() - self.v1.get_y()
            ) == (point.get_x() - self.v1.get_x()) / (self.v2.get_x() - self.v1.get_x())

    def intersects_line_seg(self, ls):
        """Determines if line intersects another line"""
        a = (
            (ls.v2.get_x() - ls.v1.get_x()) * (self.v1.get_y() - ls.v1.get_y())
            - (ls.v2.get_y() - ls.v1.get_y()) * (self.v1.get_x() - ls.v1.get_x())
        ) / (
            (ls.v2.get_y() - ls.v1.get_y()) * (self.v2.get_x() - self.v1.get_x())
            - (ls.v2.get_x() - ls.v1.get_x()) * (self.v2.get_y() - self.v1.get_y())
        )

        b = (
            (self.v2.get_x() - self.v1.get_x()) * (self.v1.get_y() - ls.v1.get_y())
            - (self.v2.get_y() - self.v1.get_y()) * (self.v1.get_x() - ls.v1.get_x())
        ) / (
            (ls.v2.get_y() - ls.v1.get_y()) * (self.v2.get_x() - self.v1.get_x())
            - (ls.v2.get_x() - ls.v1.get_x()) * (self.v2.get_y() - self.v1.get_y())
        )

        return a >= 0 and a <= 1 and b >= 0 and b <= 1
