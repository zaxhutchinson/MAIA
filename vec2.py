import math

class Vec2:
    def __init__(self,_x,_y):
        self.x = int(_x)
        self.y = int(_y)
    def __eq__(self,other):
        if isinstance(other,Vec2):
            return self.x==other.x and self.y==other.y
        else:
            return False
    def __str__(self):
        return str(self.x) + "," + str(self.y)

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self,_x):
        self.x = _x
    def setY(self,_y):
        self.y = _y


    def intersectsLineSeg(self,lineseg):
        return lineseg.intersectsPoint(self)


    def distanceToPoint(self,otherVec):
        return math.sqrt(
            math.pow(otherVec.getX()-x,2.0) +
            math.pow(otherVec.getY()-y,2.0)
        )

    # Borrowed from:
    #   https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
    def distanceToLineSeg(self,lseg):
    #    return abs(
    #        l[0]*self.x + self.y + l[1]
    #    ) / math.sqrt(
    #        l[0]**2 + 1
    #    )
        A = x - lseg.v1.getX()
        B = y - lseg.v1.getY()
        C = lseg.v2.getX() - lseg.v1.getX()
        D = lseg.v2.getY() - lseg.v1.getY()

        DOT = A * C + B * D
        LEN_SQ = C*C + D*D
        PARAM = -1

        if LEN_SQ != 0:
            PARAM = DOT / LEN_SQ

        XX = 0
        YY = 0
        if PARAM < 0:
            XX = lseg.v1.getX()
            YY = lseg.v1.getY()
        elif PARAM > 1:
            XX = lseg.v2.getX()
            YY = lseg.v2.getY()
        else:
            XX = lseg.v1.getX() + PARAM * C
            YY = lseg.v1.getY() + PARAM * D

        DX = x - XX
        DY = y - YY

        return math.sqrt(DX*DX + DY*DY)

    def lineEqFromAngle(self,angle):
        m = math.tan(angle)
        n = y - m * x
        return (m,n)

    def move(self,angle,distance):
        self.x = self.x + distance * math.cos(angle)
        self.y = self.y + distance * math.sin(angle)

    # Borrowed from:
    #   https://stackoverflow.com/questions/2259476/rotating-a-point-about-another-point-2d
    #   
    def rotateAroundPoint(self,angle,point):
        S = math.sin(angle)
        C = math.cos(angle)

        x=x-point.x
        y=y-point.y
        xnew = x * C - y * S
        ynew = x * S + y * C

        x = xnew + point.x
        y = ynew + point.y
        

