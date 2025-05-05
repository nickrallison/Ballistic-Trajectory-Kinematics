from sympy import symbols, tan, atan, sqrt, simplify, solve

# 1) symbols
Vm, dx, dy, g, theta = symbols('Vm dx dy g theta', real=True, positive=True)

# 2) t in terms of theta:  t = dx/(Vm*cos(theta))
#    cos(theta) = 1/sqrt(1+tan(theta)**2)
t_expr = dx / (Vm * (1/sqrt(1 + tan(theta)**2)))

# 3) Δy‐equation:  dy = Vm*sin(theta)*t - (g/2)*t**2
#    sin(theta) = tan(theta)/sqrt(1+tan(theta)**2)
expr = (Vm * (tan(theta)/sqrt(1 + tan(theta)**2)) * t_expr
        - (g/2)*t_expr**2
        - dy)

# 4) Turn that into a polynomial in u=tan(theta)
u = symbols('u', real=True)
expr_u = expr.subs(tan(theta), u)
poly   = simplify(expr_u * (1 + u**2))  # clear the sqrt‐denominator → quadratic

# 5) Solve quadratic for u
sol_u = solve(poly, u)  # two roots: high‐arc and low‐arc

# 6) Back out theta = atan(u) and t
solutions = []
for uval in sol_u:
    th = simplify(atan(uval))              # use atan(), not .atan()
    tm = simplify(t_expr.subs(theta, th))
    solutions.append((th, tm))

# 7) Display
for i, (th, tm) in enumerate(solutions, start=1):
    print(f"Solution #{i}:")
    print("  theta =", th)
    print("  time  =", tm)
    print()