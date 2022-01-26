"""
------
Contains basic classes for geometry
------
@includes:
1. Point
2. Line

Useless functions:
1. intPrint()
"""

from math import atan2, degrees, floor, pi, sqrt, atan, copysign
import numpy as np

def intPrint(num) -> int:
    # Just as a small utility function
    """
    -------------------------------------
    Returning an int if the float has no decimal values
    -------------------------------------
    Requires math library (ceil)
    Good for the kids, easy to implement
    """
    if num - floor(num) == float(0):
        num = int(num)
    return num

class Point:
    """
    -------------------------------------
    Point Class
    -------------------------------------
    Stores informations about a point and methods that can be executed at your disposal

    You can:
    1. Measure distance from another point using `.distance()`
    2. Use it as the basis of creating Line objects
    3. Use it as a general purpose Point data class

    NB: You are free to let me know of any important changes I cna bring upon this class
    """
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        pass
    def distance(self, point:tuple):
        """
        -------------------------------------
        Returns the distance between another point and this one
        -------------------------------------
        Returns an `int` if possible, generally set to return `float`
        Best Use:
        ```python
        >>> A = Point(0,0)
        >>> B = Pont(3,4)
        >>> print(A.distance(B())) #yes, you have to 'call' the object there
        ```
        Output:
        ```
        5
        ```
        You're free to pass in a tuple of coordinates, although more than 3 values won't be rejected, only the first two values count in the end
        """
        x1 = point[0]
        y1 = point[1]
        dSquared = (y1-self.y)**2 + (x1-self.x)**2 #I heard ** is bad and slow, might change this thing in future
        return intPrint(sqrt(dSquared))
    def __call__(self) -> np.array:
        """
        -------------------------------------
        Returns the [x,y] values as a np.array or numpy.ndarray
        -------------------------------------
        Example:
        ```python
        >>> A = Point(3,4)() #yes, you can call an object when __call__ is declared!
        >>> print(A)
        ```
        Output:
        ```
        (3,4)
        ```
        """
        return np.array([self.x, self.y])
    def __repr__(self):
        """
        Returns a tuple, readable atleast
        """
        return (self.x, self.y)


class Line:
    def __init__(self, points:list[Point]) -> None:
        """
        Only the first two Points will be counted. Currently I don't know how to stop 
        the user from adding more than 2 points.

        Equation format is thought to be:
        ```python
        (self.dY)*x - (self.dX)*y + self.k = 0
        ```
        """
        self.points:list[Point] = points
        point0:float = points[0]
        point1:float = points[1]
        #Coefficients of equation
        self.dY:float = (point1.y - point0.y)
        self.dX:float = (point1.x - point0.x)
        self.k:float = -(self.dY*point0.x) + (self.dX*point0.y)
        #Slope calculation because it's important!
        self.sign:float = copysign(1.0,self.dY) # only for angles
        if (self.dX == 0):
            self.slope:float = float('inf') * (self.sign)
        else:
            # I should have added an elseif with y1-y2 == 0 condition but what the heck!
            self.slope:float = self.dY / self.dX
        pass
    
    @property
    def X(self):
        return np.array([self.points[0].x, self.points[1].x])
        
    @property
    def Y(self):
        return np.array([self.points[0].y, self.points[1].y])

    def __call__(self):
        ArrayX = np.array([self.points[0].x, self.points[1].x])
        ArrayY = np.array([self.points[0].y, self.points[1].y])
        return ArrayX, ArrayY

    @property
    def radian(self) -> float:
        """
        Returns the angle made against the x axis in radians
        """
        if self.slope == float('inf') * self.sign:
            return pi/2 * self.sign
        else:
            return atan(self.slope)

    @property
    def degree(self) -> float:
        """
        Returns the angle made against the x axis in degrees
        """
        if self.slope == float('inf') * self.sign:
            return intPrint(90 * self.sign)
        else:
            return intPrint((atan(self.slope)*180)/pi)
    
    @property
    def length(self):
        return self.points[0].distance(self.points[1])

    def intersect(self, line): # returns the point of intrsection
        """
        -------------------------------------
        Returns the intersection point of two lines
        -------------------------------------

        if lines are parallel: returns `None`

        if lines overlap one another: returns `float('inf')`

        if lines intersect: returns `tuple(solutionX,solutionY)`
        """
        if abs(self.slope) == abs(line.slope): # without the abs it won't check if the dY values are negatives of each other
            if self.k == line.k:
                # Lines are same!
                return float('inf')
            # Lines are parallel
            return None
        # solve for both line
        a1 = self.dY
        a2 = line.dY
        b1 = -1*self.dX
        b2 = -1*line.dX
        c1 = self.k
        c2 = line.k
        solutionX = ( (b1*c2) - (b2*c1) )/( (b2*a1) - (b1*a2) )
        solutionY = ( (c1*a2) - (c2*a1) )/( (b2*a1) - (b1*a2) )
        # remove last decimal point values if they are zeros
        return (intPrint(solutionX), intPrint(solutionY))

    def angleBetween(self, line, degrees = True):
        """
        ------
        Returns the angle between twon intersection lines
        ------
        if they overlap or are parallels: returns 0
        else: returns a float, maybe int too

        returns degree by default, set false for radian
        """
        # If one of them is vertical lines
        if self.slope == float('inf'):
            if not degrees:
                return intPrint((pi/2) - abs(line.radian))
            return intPrint((90 - abs(line.degree)))
        if line.slope == float('inf'):
            if not degrees:
                return intPrint((pi/2) - abs(self.radian))
            return intPrint((90 - abs(self.degree)))
        # if none of them are vertical lines
        if abs(self.slope) == abs(line.slope): # without the abs it won't check if the dY values are negatives of each other
            # Lines are parallel
            return 0
        else:
            if degrees:
                return intPrint(abs(atan((self.slope - line.slope)/(1 - (self.slope*line.slope)))*180/pi))
            else:
                return intPrint(abs(atan((self.slope - line.slope)/(1 - (self.slope*line.slope)))))

    def hasPoint(self, point:Point) -> bool:
        """
        -------------------------------------
        Checks if the point exists in the line
        -------------------------------------

        Give a `Point` object and it will return if the point exists in the linw
        """
        if ((self.dY*point.x) - (self.dX*point.y) - (self.k)) == 0:
            return True
        else:
            return False
    
    def __repr__(self) -> str:
        """
        ----------------------------------------------
        Returns the equation form of the line in text
        ----------------------------------------------

        NB: I want ot be able to print multiple paradigms of equations
        """
        kVal = intPrint(self.k)
        printdX = self.dX
        if self.k == float(0):
            sign = ""
            kVal = ""
        elif copysign(1.0,self.k) == 1.0:
            sign = "+"
            kVal = abs(kVal)
        elif copysign(1.0,self.k) == -1.0:
            sign = "-"
            kVal = abs(kVal)
        if self.dX > 0:
            printdX = "+"+str(intPrint(self.dX))
        
        return f"{intPrint(self.dY)}y{printdX}x{sign}{kVal}=0"

    
if __name__ == "__main__":
    #Declariong Points
    A = Point(0,0)
    B = Point(0,6)
    C = Point(0,9)
    D = Point(5,7)
    E = Point(1,5)
    F = Point(1,9)
    G = Point(0,15)
    H = Point(0,13)
    I = Point(100,0)
    J = Point(400,400)
    #Declaring Lines
    AB = Line([A,B])
    CD = Line([C,D])
    EF = Line([E,F])
    GH = Line([G,H])
    #Utilities
    print(A.distance((3,4))) # Should return an int
    print(AB) #printing equation form
    print(AB.degree) # angle against the x axis
    print(AB.hasPoint(C)) # Checks if the point exists in the line at all
    print(AB.intersect(CD)) # checks if the lines intersect ever
    print(AB.intersect(EF)) # Should return None
    print(AB.intersect(AB)) # Should return float('inf')
    print(AB.intersect(GH)) # Should return float('inf')
    print(AB.angleBetween(CD)) # Measures the acute angle between two intersecting line
    print(AB.angleBetween(GH)) # Should return 180
    print(AB.k) # Should return an int
    print(EF.k) # Should return an int
    print(EF)
    print(I.distance(J())) # Should return an int