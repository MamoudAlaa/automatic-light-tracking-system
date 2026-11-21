# Automatic Light Tracking System (LDR–Servo, LabVIEW & Arduino)

A closed-loop single-axis solar/light tracking system that measures differential light intensity using two **LDR (photoresistor)** sensors, processes the error in **LabVIEW** via the **LINX** toolkit over serial (`COM3`), and drives a **servo motor** to align with the light source.

## System Architecture
1. **Sensing Stage:** Two LDR voltage-divider circuits wired to Arduino analog inputs measure light intensity ($V_1$, $V_2$) and compute the differential voltage $\Delta V = V_1 - V_2$.
2. **Data Acquisition & Control (LabVIEW + LINX):** Reads analog voltages in real time via LINX `Analog Read` VIs, computes the target angle $\theta$, and commands the servo via `Servo Set Pulse Width VI` with an emergency `STOP` control.
3. **Actuation Stage:** Standard RC servo motor (5V shared rail) tilts the solar panel / sensor mount across $0^\circ\text{--}180^\circ$.

## Corrected Mathematical Model & Transfer Function

### 1. Differential Voltage-to-Angle Mapping
For a symmetric sensor range $\Delta V \in [-0.9\text{ V},\ +0.9\text{ V}]$ centered at midday ($\theta_0 = 90^\circ$):

$$\theta = K \cdot \Delta V + 90^\circ$$

To keep $\theta$ strictly within the physical servo limits $[0^\circ,\ 180^\circ]$:

$$K = \frac{90^\circ}{0.9\text{ V}} = 100^\circ/\text{V}$$

Using measured sensor readings $V_1 = 3.06152\text{ V}$ and $V_2 = 2.67578\text{ V}$ ($\Delta V = 0.38574\text{ V}$):

$$\theta = 100 \times 0.38574 + 90^\circ = 128.57^\circ$$

In LabVIEW LINX, the `Servo Set Pulse Width VI` accepts PWM pulse width in **microseconds** ($\mu\text{s}$), mapped linearly from angle $\theta \in [0^\circ, 180^\circ]$ (e.g., $500\text{--}2500\,\mu\text{s}$ or $1000\text{--}2000\,\mu\text{s}$ depending on servo calibration).

### 2. Second-Order Control System Identification
From the experimental step response ($PO = 33.3\%$, peak time $T_p = 0.3178\text{ s}$):

| Parameter | Formula | Value |
|---|---|---|
| **Damping Ratio ($\zeta$)** | $\frac{-\ln(PO/100)}{\sqrt{\pi^2 + \ln^2(PO/100)}}$ | **$0.3304$** |
| **Damped Natural Frequency ($\omega_d$)** | $\frac{\pi}{T_p}$ | **$9.885\text{ rad/s}$** |
| **Natural Frequency ($\omega_n$)** | $\frac{\omega_d}{\sqrt{1 - \zeta^2}}$ | **$10.473\text{ rad/s}$** |
| **Settling Time ($T_s$, 2%)** | $\frac{4}{\zeta \omega_n}$ | **$1.156\text{ s}$** |

Resulting closed-loop second-order transfer function:

$$G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2} = \frac{109.69}{s^2 + 6.92s + 109.69}$$

## LabVIEW & Project Files
- `project 1.vi` — Main closed-loop LDR-to-servo tracking VI (LINX serial acquisition, angle mapping, servo PWM output, STOP safety control).
- `servo test1.vi` — Standalone servo sweep/calibration VI.
- `Step Response.vi` — Closed-loop step response testing and gain tuning VI.
- `simulate_step_response.py` — Python script verifying the 2nd-order transfer function step response and performance metrics.

*(Note: Upload the binary `.vi` files and PDF report from the local LabVIEW project archive if running directly in LabVIEW.)*

## Team & Supervision
- **Course Project:** Automatic Control Systems — Mechatronics Engineering, Egypt-Japan University for Science and Technology (E-JUST), May 2025
- **Team Members:** Mahmoud A. Mohamed, Shahd Mohamed Ali, Aya Gamal, Adham Yasser
- **Supervisor:** Prof. Ayman NadaLINX) with 2nd-order transfer function control modeling
