# Ballistic Trajectory Kinematics

This small project provides tools to compute projectile motion in two dimensions.  
You can:

  * Compute forward kinematics: given muzzle velocity, launch angle and time, find Δx and Δy.  
  * Solve inverse kinematics: given Δx, Δy and muzzle velocity, find the two possible (θ, t) solutions.  
  * Generate summary or verbose tables of relative aiming angles and flight times over parameter grids.

---

## Requirements

This project is written in Python 3 and depends on:

  * mpmath==1.3.0  
  * numpy==2.2.5  
  * sympy==1.14.0  

Install with:

```bash
pip install -r requirements.txt
```

---

## Project Layout

```
.
├── requirements.txt
└── src
    ├── kinematics.py          # forward & inverse kinematics
    ├── main.py                # CLI to verify solutions
    ├── solver.py              # symbolic derivation with Sympy
    ├── table_generator.py     # generate summary CSV per Dx
    └── verbose_table_generator.py  # generate full CSV or Markdown grid
```

---

## Usage

### 1. Verify Solutions

Run the example in `src/main.py`:

```bash
python src/main.py
```

This will:

  * Solve for the two (θ, t) pairs that hit the target (Δx, Δy).  
  * Re‐compute forward kinematics to confirm the solution.  

### 2. Generate Summary Table

Use `table_generator.py` to produce a CSV summary of relative angles and times per horizontal distance:

```bash
python src/table_generator.py --samples 200 --vm-min 80 --vm-max 100
```

**Sample output:**

| Dx  | Relative Theta (Deg) | Stdev Theta (Deg) | Mean Time (s) | Stdev Time (s) |
|-----|----------------------|-------------------|---------------|----------------|
| 10  | 0.3765               | 0.0562            | 0.1210        | 0.0102         |
| 15  | 0.5620               | 0.0870            | 0.1764        | 0.0141         |
| 20  | 0.7467               | 0.1146            | 0.2327        | 0.0182         |
| 25  | 0.9297               | 0.1452            | 0.2890        | 0.0225         |
| 30  | 1.1128               | 0.1687            | 0.3456        | 0.0261         |
| 35  | 1.3001               | 0.2010            | 0.4029        | 0.0312         |
| 40  | 1.4926               | 0.2221            | 0.4611        | 0.0343         |
| 45  | 1.6965               | 0.2611            | 0.5210        | 0.0402         |
| 50  | 1.8508               | 0.2816            | 0.5734        | 0.0435         |
| 55  | 2.0507               | 0.3115            | 0.6329        | 0.0480         |
| 60  | 2.2415               | 0.3462            | 0.6909        | 0.0533         |
| 65  | 2.4377               | 0.3751            | 0.7498        | 0.0577         |
| 70  | 2.6322               | 0.4037            | 0.8084        | 0.0622         |
| 75  | 2.7896               | 0.4113            | 0.8616        | 0.0633         |
| 80  | 2.9698               | 0.4550            | 0.9180        | 0.0702         |
| 85  | 3.1629               | 0.4810            | 0.9765        | 0.0742         |
| 90  | 3.3701               | 0.5182            | 1.0371        | 0.0798         |

### 3. Generate Verbose Grid

Produce a full grid in CSV or Markdown format:

```bash
python src/verbose_table_generator.py \
    --vm-min 76 --vm-max 99 --vm-step 1 \
    --dx-min 10 --dx-max 90 --dx-step 5 \
    --dy-min -5 --dy-max 5 --dy-step 1 \
    --format md
```

---

## API Reference

```python
from kinematics import forward_kinematics, solve_theta_time
```

#### forward_kinematics(Vm, θ, t, g=9.81) → (dx, dy)

Compute horizontal and vertical displacements:

  * Vm: muzzle velocity (m/s)  
  * θ: launch angle (radians)  
  * t: time since launch (s)  
  * g: gravitational acceleration (m/s²)  

#### solve_theta_time(dx, dy, Vm, g=9.81) → ((θ₁, t₁), (θ₂, t₂)) | None

Solve for two possible (θ, t) that satisfy:

  dx = Vm·cos θ·t  
  dy = Vm·sin θ·t − ½ g t²  

Returns `None` if no real solutions exist.

---

## Symbolic Derivation

To see the Sympy‐based derivation, run:

```bash
python src/solver.py
```

It prints the exact symbolic solutions for θ and t.
