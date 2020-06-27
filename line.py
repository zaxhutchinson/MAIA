from vec2 import Vec2

class LineSeg:
    def __init__(self,v1,v2):
        self.v1 = v1
        self.v2 = v2

    def intersectsLineSeg(self,ls):
        a = ( \
            (ls.v2.getX()-ls.v1.getX()) * (self.v1.getY()-ls.v1.getY()) - \
            (ls.v2.getY()-ls.v1.getY()) * (self.v1.getX()-ls.v1.getX()) \
        ) / ( \
            (ls.v2.getY()-ls.v1.getY()) * (self.v2.getX()-self.v1.getX()) - \
            (ls.v2.getX()-ls.v1.getX()) * (self.v2.getY()-self.v1.getY()) \
        )

        b = ( \
            (self.v2.getX()-self.v1.getX()) * (self.v1.getY()-ls.v1.getY()) - \
            (self.v2.getY()-self.v1.getY()) * (self.v1.getX()-ls.v1.getX()) \
        ) / ( \
            (ls.v2.getY()-ls.v1.getY()) * (self.v2.getX()-self.v1.getX()) - \
            (ls.v2.getX()-ls.v1.getX()) * (self.v2.getY()-self.v1.getY()) \
        )

        return (a >= 0 and a <= 1 and b >= 0 and b <= 1)