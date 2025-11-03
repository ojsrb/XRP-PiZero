class vec3:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other):
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return vec3(self.x - float(other.x), self.y - float(other.y), self.z - float(other.z))

    def __repr__(self):
        return f"vec3({self.x}, {self.y}, {self.z})"

    def mul(self, scalar):
        return vec3(self.x * scalar, self.y * scalar, self.z * scalar)

class vec3rotation:
    def __init__(self, x, y, z, roll, pitch, yaw):
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def __add__(self, other):
        return vec3rotation(self.x + other.x, self.y + other.y, self.z + other.z, self.roll + other.roll, self.pitch + other.pitch, self.yaw + other.yaw)

    def __sub__(self, other):
        return vec3rotation(self.x - other.x, self.y - other.y, self.z - other.z, self.roll - other.roll, self.pitch - other.pitch, self.yaw - other.yaw)

    def __repr__(self):
        return f"vec3rotation({self.x}, {self.y}, {self.z}, {self.roll}, {self.pitch}, {self.yaw})"

    def to_vec3(self):
        return vec3(self.x, self.y, self.z)

class quat:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w