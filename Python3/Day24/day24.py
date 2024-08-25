from dataclasses import dataclass
from typing import *

import numpy as np
import sympy


@dataclass
class Point2:
    x: Union[int, float]
    y: Union[int, float]


@dataclass
class Point3:
    x: Union[int, float]
    y: Union[int, float]
    z: Union[int, float]

    @property
    def position(self) -> Tuple[float, float, float]:
        return self.x, self.y, self.z


@dataclass
class Hailstone:
    start_point: Point3
    speed: Point3

    @property
    def a2(self) -> float:
        return self.speed.y / self.speed.x

    @property
    def b2(self) -> float:
        return self.start_point.y - self.a2*self.start_point.x

    def get_future_intersection_2d(self, other: 'Hailstone') -> Optional[Point2]:
        """Solve equations for intersection."""
        if self.a2 == other.a2:
            return None

        int_x: float = (other.b2 - self.b2) / (self.a2 - other.a2)
        int_y: float = self.a2 * int_x + self.b2
        intersection_point: Point2 = Point2(int_x, int_y)

        # Is in self's future ?
        dx: float = (intersection_point.x - self.start_point.x) / self.speed.x
        dy: float = (intersection_point.x - self.start_point.x) / self.speed.x
        if dx < 0 or dy < 0:
            return None

        # Is in other's future ?
        dx = (intersection_point.x - other.start_point.x) / other.speed.x
        dy = (intersection_point.x - other.start_point.x) / other.speed.x
        if dx < 0 or dy < 0:
            return None

        return intersection_point


def part_one() -> int:
    MIN_VALUE: int = 200000000000000
    MAX_VALUE: int = 400000000000000

    result: int = 0
    stones: List[Hailstone] = []

    with open("input.txt", mode='r') as f_input:
        for line in f_input.readlines():
            line = line.strip()
            pos, _sep, vel = line.partition(" @ ")
            start_point: Point3 = Point3(*[int(x) for x in pos.split(", ")])
            velocity: Point3 = Point3(*[int(x) for x in vel.split(", ")])

            stones.append(Hailstone(start_point, velocity))

    # Compute intersection points
    for idx1, stone1 in enumerate(stones):
        for idx2, stone2 in enumerate(stones):
            if idx2 <= idx1:
                continue
            intersection_point: Optional[Point2] = stone1.get_future_intersection_2d(stone2)
            if intersection_point is None:
                continue
            if MIN_VALUE <= intersection_point.x <= MAX_VALUE and MIN_VALUE <= intersection_point.y <= MAX_VALUE:
                result += 1

    return result

# Part 2

def build_matrixes(
    hailstone1: Hailstone,
    hailstone2: Hailstone,
    hailstone3: Hailstone,
    hailstone4: Hailstone,
    hailstone5: Hailstone,
    hailstone6: Hailstone,
) -> Tuple[np.ndarray, np.ndarray]:
    """Create matrixes representing a 6-hailstone sub-problem.

    The Bareiss algorithm used later requires no zeros on the diagonal.
    So lines were re-ordered, which does not change anything at all.

    """
    # Shortcuts for each value
    x01, y01, z01 = hailstone1.start_point.position
    vx1, vy1, vz1 = hailstone1.speed.position
    x02, y02, z02 = hailstone2.start_point.position
    vx2, vy2, vz2 = hailstone2.speed.position
    x03, y03, z03 = hailstone3.start_point.position
    vx3, vy3, vz3 = hailstone3.speed.position
    x04, y04, z04 = hailstone4.start_point.position
    vx4, vy4, vz4 = hailstone4.speed.position
    x05, y05, z05 = hailstone5.start_point.position
    vx5, vy5, vz5 = hailstone5.speed.position
    x06, y06, z06 = hailstone6.start_point.position
    vx6, vy6, vz6 = hailstone6.speed.position

    A = np.array([
        # 1-2-3
        [vz1-vz3,       0, vx3-vx1, z03-z01,       0, x01-x03],  # 2
        [vy1-vy2, vx2-vx1,       0, y02-y01, x01-x02,       0],  # 1
        [      0, vz2-vz3, vy3-vy2,       0, z03-z02, y02-y03],  # 3
        # 4-5-6    
        [vz4-vz6,       0, vx6-vx4, z06-z04,       0, x04-x06],  # 5
        [vy4-vy5, vx5-vx4,       0, y05-y04, x04-x05,       0],  # 4
        [      0, vz5-vz6, vy6-vy5,       0, z06-z05, y05-y06],  # 6
    ],
    dtype=np.longlong
    )

    B = np.array([
        # 1-2-3
        x01*vz1 - vx1*z01 + z03*vx3 - vz3*x03,  # 2
        x01*vy1 - vx1*y01 + y02*vx2 - vy2*x02,  # 1
        y02*vz2 - vy2*z02 + z03*vy3 - vz3*y03,  # 3
        # 4-5-6
        x04*vz4 - vx4*z04 + z06*vx6 - vz6*x06,  # 5
        x04*vy4 - vx4*y04 + y05*vx5 - vy5*x05,  # 4
        y05*vz5 - vy5*z05 + z06*vy6 - vz6*y06,  # 6
    ],
    dtype=np.longlong
    )

    # Print system
    '''
    equations: List[str] = []
    for i in range(len(A)):
        tmp = "{"
        tmp += ", ".join(str(x) for x in A[i])
        tmp += ", " + str(B[i])
        tmp+= "}"
        equations.append(tmp)
    system: str = ", ".join(equations)
    system = "{" + system + "}"
    print(system)
    '''

    return A, B

def bareiss_determinant(input_matrix: np.ndarray) -> int:
    """Compute a matrix's determinant using Bareiss algorithm.
    
    https://en.wikipedia.org/wiki/Bareiss_algorithm
    """
    n: int = len(input_matrix)

    # Algorithm is done in place, and require to extend the matrix
    # So it is copied in a bigger one
    tmp_matrix: np.ndarray = np.zeros((n+1, n+1), dtype=np.longlong)
    for i in range(n):
        for j in range(n):
            tmp_matrix[i+1, j+1] = input_matrix[i, j]

    # Using sympy for arbitrary precision
    matrix = sympy.matrices.Matrix(tmp_matrix)

    # === Algorithm ===

    matrix[0, 0] = 1

    for k in range(1, n-1+1):
        for i in range(k+1, n+1):
            for j in range(k+1, n+1):
                mij = matrix[i,j]
                mkk = matrix[k,k]
                mik = matrix[i,k]
                mkj = matrix[k,j]
                mkk1 = matrix[k-1,k-1]

                matrix[i, j] = (mij*mkk - mik*mkj) / mkk1

    return matrix[n, n]

def solve(A_matrix: np.ndarray, B_matrix: np.ndarray) -> List[int]:
    """Solve a linear system using Cramer's rule.
    
    https://en.wikipedia.org/wiki/Cramer%27s_rule
    """
    n: int = len(A_matrix)
    A = A_matrix.copy()
    B = B_matrix.copy()

    # Compute det(A) once and for all
    det_A = bareiss_determinant(A.copy())
    # print("det(A):", det_A)

    result: List[int] = []
    for index in range(n):
        # Compute the matrix
        Ai: np.ndarray = A.copy()
        Ai[:, index] = B.copy()

        # print("===", index + 1)
        # print(np.array_repr(Ai).replace("\n", "").replace("],", "],\n"))

        det_Ai = bareiss_determinant(Ai)
        # print(det_Ai)

        result.append(det_Ai / det_A)

    return result

def part_two() -> int:
    """This solution was found by hand.

    Predicate
    ---------
    It is very unlikely to find a solution to a sub-problem (with less hailstones)
    that is not the solution of the full size problem.

    So this solution tries to find a solution to a minimal problem.

    Mathematics
    -----------
    I attempted to find a solution by hand, writing equations and solving a system.

    Long story short:
    - we can rewrite the problem so that a sub-problem of it is finding 6 values
      - start position (3D) + speed (3D)
    - we can rewrite this sub-problem to have a sub-sub-problem with is linear !
    - when trying to solve with a system of (linear!) equations, at least 6 hailstones must be used,
      - note that the hailstones trajectories must be linearly independent

    I could have transformed the system matrix in its echelon form by hand, but it would
    be such a pain.
    That's where I gave the rest of the solving to my computer.

    (See the maths in part2.pdf)

    Programming
    -----------
    Values of the input are rather big and asking numpy of scipy to solve the linear
    system of equation just does not work.
    Note: input values are only integers and that is a huge condition to do what is explain below.

    I had to implement my own solving algorithm.
    Taking into account that float imprecision is my enemy here.

    I first went for finding the echelon form of the system when I found out about the
    Bareiss_algorithm (https://en.wikipedia.org/wiki/Bareiss_algorithm).
    The article tells about getting the echelon form but I could not find it.

    However it gives me the determinant of the matrix, with no float issue.

    Combined with Cramer's rule (https://en.wikipedia.org/wiki/Cramer%27s_rule) which
    allows to solve a system only using determinants, I had all I needed.

    """
    stones: List[Hailstone] = []

    with open("input.txt", mode='r') as f_input:
        for line in f_input.readlines():
            line = line.strip()
            pos, _sep, vel = line.partition(" @ ")
            start_point: Point3 = Point3(*[int(x) for x in pos.split(", ")])
            velocity: Point3 = Point3(*[int(x) for x in vel.split(", ")])

            stones.append(Hailstone(start_point, velocity))

    # Solve for the first 6 hailstones
    A, B = build_matrixes(*stones[:6])
    res: List[int] = solve(A, B)

    # print("Result =", res)
    return sum(res[:3])  # Sum of x0s, y0s & z0s


print("Part one:", part_one())
print("Part two:", part_two())
