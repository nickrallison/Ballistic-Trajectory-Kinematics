import math
from typing import List, Tuple

def forward_kinematics(Vm: float, theta: float, t: float, g: float = 9.81) -> Tuple[float, float]:
    """
    Given muzzle velocity Vm, launch angle theta (rad), time t and gravity g,
    compute horizontal and vertical displacements Δx and Δy.
    """
    dx = Vm * math.cos(theta) * t
    dy = Vm * math.sin(theta) * t - 0.5 * g * t * t
    return dx, dy

def solve_theta_time(dx: float, dy: float, Vm: float, g: float = 9.81
                    ) -> List[Tuple[float, float]]:
    """
    Solve for the two possible (theta, t) pairs that satisfy:
      dx = Vm*cos(theta)*t
      dy = Vm*sin(theta)*t - 0.5*g*t^2

    Returns a list of (theta, t) in radians and seconds. If no real solution
    exists, returns an empty list.
    """
    # Discriminant under the radical
    disc = Vm**4 - 2*Vm**2*dy*g - (dx * g)**2
    if disc < 0:
        return []  # no real solutions

    sqrt_disc = math.sqrt(disc)

    # low‐arc solution
    theta1 = math.atan((Vm**2 - sqrt_disc) / (dx * g))
    t1 = math.sqrt(2) * math.sqrt(Vm**2 - dy*g - sqrt_disc) / g

    # high‐arc solution
    theta2 = math.atan((Vm**2 + sqrt_disc) / (dx * g))
    t2 = math.sqrt(2) * math.sqrt(Vm**2 - dy*g + sqrt_disc) / g

    return [(theta1, t1), (theta2, t2)]

def verify(dx: float, dy: float, Vm: float, g: float = 9.81) -> None:
    """
    Solve for theta & t, then plug back into forward kinematics to verify
    that we recover (dx, dy).
    """
    solutions = solve_theta_time(dx, dy, Vm, g)
    if not solutions:
        print("No real solutions for the given parameters.")
        return

    for i, (theta, t) in enumerate(solutions, start=1):
        dx_calc, dy_calc = forward_kinematics(Vm, theta, t, g)
        print(f"Solution #{i}:")
        print(f"  theta (deg) = {math.degrees(theta):.4f}")
        print(f"  time        = {t:.4f} s")
        print(f"  → Δx = {dx_calc:.4f} (target {dx:.4f})")
        print(f"  → Δy = {dy_calc:.4f} (target {dy:.4f})")
        print()

if __name__ == "__main__":
    # Example parameters
    Vm_input = 90.0      # muzzle velocity in m/s
    dx_target = 50.0    # horizontal displacement in m
    dy_target =  20.0    # vertical displacement in m
    g_const   =  9.81    # gravity in m/s^2

    print("Forward‐solve and verify for:")
    print(f"  Vm = {Vm_input} m/s, Δx = {dx_target} m, Δy = {dy_target} m\n")
    verify(dx_target, dy_target, Vm_input, g_const)