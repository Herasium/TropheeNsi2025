import math

class Vec3:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)): 
            return Vec3(self.x * other, self.y * other, self.z * other)
        if isinstance(other, Vec3): 
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        return NotImplemented

    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def normalize(self):
        magnitude = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        if magnitude == 0:
            return self
        return Vec3(self.x / magnitude, self.y / magnitude, self.z / magnitude)


    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return f"Vec3(x:{self.x}, y:{self.y}, z:{self.z})"
    