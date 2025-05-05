# kinematics.py

import math
from typing import List, Tuple

def forward_kinematics(Vm: float, theta: float, t: float, g: float = 9.81
                      ) -> Tuple[float, float]:
    """
    Given muzzle velocity Vm, launch angle theta (rad), time t and gravity g,
    compute horizontal and vertical displacements Δx and Δy.
    """
    dx = Vm * math.cos(theta) * t
    dy = Vm * math.sin(theta) * t - 0.5 * g * t * t
    return dx, dy

def solve_theta_time(dx: float, dy: float, Vm: float, g: float = 9.81
                    ) -> Tuple[Tuple[float, float], Tuple[float, float]] | None:
    """
    Solve for the two possible (theta, t) pairs that satisfy:
      dx = Vm*cos(theta)*t
      dy = Vm*sin(theta)*t - 0.5*g*t^2

    Returns a list of (theta, t) in radians and seconds.
    If no real solution exists, returns an empty list.
    """
    # Discriminant under the radical
    disc = Vm**4 - 2 * Vm**2 * dy * g - (dx * g)**2
    if disc < 0:
        return None  # no real solutions

    sqrt_disc = math.sqrt(disc)

    # low‐arc solution
    theta1 = math.atan((Vm**2 - sqrt_disc) / (dx * g))
    t1 = dx / (Vm * math.cos(theta1))

    # high‐arc solution
    theta2 = math.atan((Vm**2 + sqrt_disc) / (dx * g))
    t2 = dx / (Vm * math.cos(theta2))

    return ((theta1, t1), (theta2, t2))