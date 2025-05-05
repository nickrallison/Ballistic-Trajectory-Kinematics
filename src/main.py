import numpy as np

def solve_theta(Vm, dx, dy, g=9.81):
    # Implements the full 4-branch solution for θ
    Vm2 = Vm**2
    dx2 = dx**2
    A = -dx2 * g**2 - 2 * dy * Vm2 * g + Vm2**2

    thetas = []
    if A < 0:
        # No real solutions for sqrt(A)
        return thetas

    sqrtA = np.sqrt(A)
    denom = dx2 * g + 2 * dy * Vm2

    # ± for sqrtA
    for sign1 in [+1, -1]:
        inner = Vm2 + sign1 * sqrtA
        # ± for outer sqrt
        B = dx2 * inner**2 + (dx2 * g + 2 * dy * Vm2)**2
        if B < 0:
            continue
        sqrtB = np.sqrt(B)
        for sign2 in [+1, -1]:
            num = dx * inner + sign2 * sqrtB
            # Avoid division by zero
            if denom == 0:
                continue
            theta = -2 * np.arctan(num / denom)
            theta_deg = np.degrees(theta)
            # Only keep real, physical angles (0 < θ < 90)
            if 0 < theta_deg < 90:
                thetas.append(theta_deg)
    # Remove duplicates (can happen due to symmetry)
    thetas = list(sorted(set([round(t, 8) for t in thetas])))
    return thetas

def check_solution(Vm, dx, dy, theta_deg, g=9.81):
    # Plug θ back into the original equations to check
    theta = np.radians(theta_deg)
    Vx = Vm * np.cos(theta)
    Vy = Vm * np.sin(theta)
    # Quadratic formula for t: y = Vy*t - 0.5*g*t^2 = dy
    # 0.5*g*t^2 - Vy*t + dy = 0
    a = 0.5 * g
    b = -Vy
    c = dy
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        print(f"No real time solution for θ = {theta_deg:.2f}°")
        return None
    t1 = (-b + np.sqrt(discriminant)) / (2*a)
    t2 = (-b - np.sqrt(discriminant)) / (2*a)
    t = t1 if t1 > 0 else t2
    x_check = Vx * t
    return x_check

if __name__ == "__main__":
    # Example values
    Vm = 90.0      # m/s
    dx = 50.0      # meters
    dy = 3.0       # meters (target is 2m above muzzle)
    g = 9.81

    thetas = solve_theta(Vm, dx, dy, g)
    if not thetas:
        print("No real θ solutions for these parameters.")
    else:
        print(f"Possible θ (degrees): {', '.join(f'{t:.4f}' for t in thetas)}")
        # Check the solution by plugging back
        tol = 1e-2  # 1 cm tolerance
        for theta_deg in thetas:
            x_check = check_solution(Vm, dx, dy, theta_deg, g)
            if x_check is not None and abs(x_check - dx) < tol:
                print(f"VALID: θ = {theta_deg:.4f}°, x_check = {x_check:.4f} m")
            else:
                print(f"INVALID: θ = {theta_deg:.4f}°, x_check = {x_check:.4f} m")