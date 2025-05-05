# table_generator.py

import math
import statistics
from kinematics import solve_theta_time

def make_table():
    Vm = (76.0 + 99.0) / 2.0  # average muzzle velocity
    print("Dx,Dy,theta_low_deg,theta_high_deg,time_low_s,time_high_s,std_theta_deg,std_time_s")
    for dx in range(10, 95, 5):     # 10,15,...,90
        for dy in range(-5, 6):     # -5,-4,...,5
            sols = solve_theta_time(dx, dy, Vm)
            if len(sols) != 2:
                # no real solutions or degenerate
                print(f"{dx},{dy},NA,NA,NA,NA,NA,NA")
                continue

            (th1, t1), (th2, t2) = sols
            th1_deg = math.degrees(th1)
            th2_deg = math.degrees(th2)

            std_th = statistics.pstdev([th1_deg, th2_deg])
            std_t  = statistics.pstdev([t1, t2])

            print(f"{dx},{dy},"
                  f"{th1_deg:.4f},{th2_deg:.4f},"
                  f"{t1:.4f},{t2:.4f},"
                  f"{std_th:.4f},{std_t:.4f}")

if __name__ == "__main__":
    make_table()