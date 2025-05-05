
# table_generator.py
import argparse
import math
import random
import statistics
from kinematics import solve_theta_time

def make_table(samples: int,
               vm_min: float,
               vm_max: float,
               fmt: str) -> None:
    """
    Generate and print per-dx relative-angle and time stats
    in either CSV or Markdown format.
    """
    headers = [
        "Dx",
        "Relative Theta (Deg)",
        "Stdev Theta (Deg)",
        "Mean Time (s)",
        "Stdev Time (s)",
    ]

    # Print header
    if fmt == "csv":
        print(",".join(headers))
    else:  # markdown
        print("| " + " | ".join(headers) + " |")
        print("|" + "|".join(["---"] * len(headers)) + "|")

    # Iterate dx values
    for dx in range(10, 95, 5):  # 10, 15, ..., 90
        rel_angles = []
        t_vals = []

        for dy in range(-5, 6):  # -5, -4, ..., 5
            aim_dir_deg = math.degrees(math.atan2(dy, dx))
            for _ in range(samples):
                Vm = random.uniform(vm_min, vm_max)
                sols = solve_theta_time(dx, dy, Vm)
                if len(sols) != 2:
                    continue

                (th1, t1), (_th2, _t2) = sols
                shot_deg = math.degrees(th1)
                rel_angles.append(shot_deg - aim_dir_deg)
                t_vals.append(t1)

        # No valid samples?
        if not rel_angles:
            row = [str(dx)] + ["NA"] * (len(headers) - 1)
        else:
            mean_rel = statistics.mean(rel_angles)
            std_rel = statistics.stdev(rel_angles) if len(rel_angles) > 1 else 0.0
            mean_t = statistics.mean(t_vals)
            std_t = statistics.stdev(t_vals) if len(t_vals) > 1 else 0.0
            row = [
                str(dx),
                f"{mean_rel:.4f}",
                f"{std_rel:.4f}",
                f"{mean_t:.4f}",
                f"{std_t:.4f}",
            ]

        # Print row
        if fmt == "csv":
            print(",".join(row))
        else:  # markdown
            print("| " + " | ".join(row) + " |")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate per-dx relative-angle and time statistics"
    )
    parser.add_argument(
        "--samples", "-n",
        type=int,
        default=100,
        help="number of Vm samples per (Dx,Dy)"
    )
    parser.add_argument(
        "--vm-min",
        type=float,
        default=76.0,
        help="minimum Vm for sampling"
    )
    parser.add_argument(
        "--vm-max",
        type=float,
        default=99.0,
        help="maximum Vm for sampling"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["csv", "md"],
        default="csv",
        help="output format: csv (default) or md (markdown)"
    )
    args = parser.parse_args()

    make_table(
        samples=args.samples,
        vm_min=args.vm_min,
        vm_max=args.vm_max,
        fmt=args.format,
    )
