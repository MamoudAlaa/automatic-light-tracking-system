"""Verify 2nd-order transfer function parameters for the LDR-Servo tracking system."""
import math

PO = 33.3       # Percent overshoot (%)
Tp = 0.3178     # Peak time (s)

ln_po = math.log(PO / 100.0)
zeta = -ln_po / math.sqrt(math.pi**2 + ln_po**2)
wd = math.pi / Tp
wn = wd / math.sqrt(1.0 - zeta**2)
ts_2pct = 4.0 / (zeta * wn)

print(f"Damping ratio (zeta):      {zeta:.4f}")
print(f"Damped frequency (wd):     {wd:.4f} rad/s")
print(f"Natural frequency (wn):    {wn:.4f} rad/s")
print(f"Settling time (Ts, 2%):    {ts_2pct:.4f} s")
print(f"Transfer Function G(s):    {wn**2:.2f} / (s^2 + {2*zeta*wn:.2f}s + {wn**2:.2f})")
