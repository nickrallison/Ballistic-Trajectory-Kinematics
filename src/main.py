# main.py

import math
from kinematics import forward_kinematics, solve_theta_time

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
        print(f"  theta (deg) = {math.degrees(theta):f}")
        print(f"  time        = {t:f} s")
        print(f"  → Δx = {dx_calc:f} (target {dx:f})")
        print(f"  → Δy = {dy_calc:f} (target {dy:f})")
        print()

if __name__ == "__main__":
    # Example parameters
    Vm_input = 90.0      # muzzle velocity in m/s
    dx_target = 50.0     # horizontal displacement in m
    dy_target =  2.0     # vertical displacement in m
    g_const   =  9.81    # gravity in m/s^2

    print("Forward‐solve and verify for:")
    print(f"  Vm = {Vm_input} m/s, Δx = {dx_target} m, Δy = {dy_target} m\n")
    verify(dx_target, dy_target, Vm_input, g_const)