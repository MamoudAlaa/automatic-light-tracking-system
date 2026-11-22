"""Verify 2nd-order transfer function parameters and plot step response."""
import math
import numpy as np
import matplotlib.pyplot as plt

PO = 33.3       # Target percent overshoot (%)
Tp = 0.3178     # Target peak time (s)

ln_po = math.log(PO / 100.0)
zeta = -ln_po / math.sqrt(math.pi**2 + ln_po**2)
wd = math.pi / Tp
wn = wd / math.sqrt(1.0 - zeta**2)
ts_2pct = 4.0 / (zeta * wn)

print(f"Damping ratio (zeta):      {zeta:.4f}")
print(f"Damped frequency (wd):     {wd:.4f} rad/s")
print(f"Natural frequency (wn):    {wn:.4f} rad/s")
print(f"Closed-loop poles:         {-zeta*wn:.4f} +/- {wd:.4f}j")
print(f"Settling time (Ts, 2%):    {ts_2pct:.4f} s")
print(f"Transfer Function G(s):    {wn**2:.2f} / (s^2 + {2*zeta*wn:.2f}s + {wn**2:.2f})")

t = np.linspace(0, 2.2, 1000)
phi = np.arccos(zeta)
y = 1.0 - (np.exp(-zeta * wn * t) / np.sqrt(1.0 - zeta**2)) * np.sin(wd * t + phi)
print(f"Simulated Peak:            {y.max():.4f} (PO = {(y.max()-1)*100:.2f}%) at t = {t[np.argmax(y)]:.4f} s")
