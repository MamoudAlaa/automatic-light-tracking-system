"""Verify 2nd-order transfer function parameters and simulated step response for the LDR-Servo tracking system."""
import math

PO = 33.3      # Percent overshoot (%)
Tp = 0.3178    # Peak time (s)

ln_po = math.log(PO / 100.0)
zeta = -ln_po / math.sqrt(math.pi**2 + ln_po**2)
wd = math.pi / Tp
wn = wd / math.sqrt(1.0 - zeta**2)
sigma = zeta * wn
ts_2pct = 4.0 / sigma

print(f"Damping ratio (zeta):     {zeta:.4f}")
print(f"Damped frequency (wd):    {wd:.4f} rad/s")
print(f"Natural frequency (wn):   {wn:.4f} rad/s")
print(f"Closed-loop poles:        {-sigma:.2f} +/- {wd:.2f}j")
print(f"Settling time (Ts, 2%):   {ts_2pct:.4f} s")
print(f"Transfer Function G(s):   {wn**2:.2f} / (s^2 + {2*sigma:.2f}s + {wn**2:.2f})")

# Simulated unit step response peak verification
dt = 0.0001
t_end = 2.0
phi = math.acos(zeta)
sqrt_1_z2 = math.sqrt(1.0 - zeta**2)

y_peak = 0.0
t_peak = 0.0
steps = int(t_end / dt) + 1
for i in range(steps):
    t = i * dt
    y = 1.0 - (math.exp(-sigma * t) / sqrt_1_z2) * math.sin(wd * t + phi)
    if y > y_peak:
        y_peak = y
        t_peak = t

sim_po = (y_peak - 1.0) * 100.0
print("\nSimulated Step Response Peak Verification:")
print(f"Simulated Peak Overshoot: {sim_po:.2f}%")
print(f"Simulated Peak Time (Tp): {t_peak:.4f} s")
