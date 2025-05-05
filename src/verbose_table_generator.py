# src/verbose_table_generator.py

import argparse
import math
from kinematics import solve_theta_time

def frange(start: float, stop: float, step: float):
    """
    Floating‐point range generator inclusive of stop (if it lands on a step).
    """
    vals = []
    n_steps = int(math.floor((stop - start) / step))
    for i in range(n_steps + 1):
        vals.append(start + i * step)
    # maybe include stop if the above loop missed it due to rounding
    if not math.isclose(vals[-1], stop) and vals[-1] + step > stop:
        vals.append(stop)
    return vals

def verbose_table(
    vm_min: float,
    vm_max: float,
    vm_step: float,
    dx_min: float,
    dx_max: float,
    dx_step: float,
    dy_min: float,
    dy_max: float,
    dy_step: float,
    fmt: str
) -> None:
    """
    Iterate over Dx, Dy, Vm in steps, solve each, and print raw results:
      Dx, Dy, Vm, Relative Theta (Deg), Time (s)
    in either CSV or Markdown format.
    """
    headers = [
        "Dx",
        "Dy",
        "Vm",
        "Relative Theta (Deg)",
        "Time (s)"
    ]

    # print header
    if fmt == "csv":
        print(",".join(headers))
    else:  # markdown
        print("| " + " | ".join(headers) + " |")
        print("|" + "|".join(["---"] * len(headers)) + "|")

    dx_vals = frange(dx_min, dx_max, dx_step)
    dy_vals = frange(dy_min, dy_max, dy_step)
    vm_vals = frange(vm_min, vm_max, vm_step)

    for dx in dx_vals:
        for dy in dy_vals:
            aim_dir_deg = math.degrees(math.atan2(dy, dx))
            for vm in vm_vals:
                sols = solve_theta_time(dx, dy, vm)
                if len(sols) != 2:
                    continue

                # take the low-angle solution
                (th_low, t_low), _ = sols
                shot_deg  = math.degrees(th_low)
                rel_angle = shot_deg - aim_dir_deg

                row = [
                    f"{dx:.4f}",
                    f"{dy:.4f}",
                    f"{vm:.4f}",
                    f"{rel_angle:.4f}",
                    f"{t_low:.4f}"
                ]

                if fmt == "csv":
                    print(",".join(row))
                else:
                    print("| " + " | ".join(row) + " |")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate verbose grid of ballistic solutions"
    )
    parser.add_argument(
        "--vm-min",
        type=float,
        default=76.0,
        help="minimum muzzle velocity"
    )
    parser.add_argument(
        "--vm-max",
        type=float,
        default=99.0,
        help="maximum muzzle velocity"
    )
    parser.add_argument(
        "--vm-step",
        type=float,
        default=1.0,
        help="step size for muzzle velocity (must be > 0)"
    )
    parser.add_argument(
        "--dx-min",
        type=float,
        default=10.0,
        help="minimum horizontal distance"
    )
    parser.add_argument(
        "--dx-max",
        type=float,
        default=90.0,
        help="maximum horizontal distance"
    )
    parser.add_argument(
        "--dx-step",
        type=float,
        default=5.0,
        help="step size for horizontal distance (must be > 0)"
    )
    parser.add_argument(
        "--dy-min",
        type=float,
        default=-5.0,
        help="minimum vertical offset"
    )
    parser.add_argument(
        "--dy-max",
        type=float,
        default=5.0,
        help="maximum vertical offset"
    )
    parser.add_argument(
        "--dy-step",
        type=float,
        default=1.0,
        help="step size for vertical offset (must be > 0)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["csv", "md"],
        default="csv",
        help="output format: csv or md (markdown)"
    )
    args = parser.parse_args()

    # validate steps
    for name, step in [("vm-step", args.vm_step),
                       ("dx-step", args.dx_step),
                       ("dy-step", args.dy_step)]:
        if step <= 0:
            parser.error(f"{name} must be positive and non-zero")

    verbose_table(
        vm_min=args.vm_min,
        vm_max=args.vm_max,
        vm_step=args.vm_step,
        dx_min=args.dx_min,
        dx_max=args.dx_max,
        dx_step=args.dx_step,
        dy_min=args.dy_min,
        dy_max=args.dy_max,
        dy_step=args.dy_step,
        fmt=args.format,
    )
