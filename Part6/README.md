## Question 3: Loop gain and fractional droop

All experiments used heating toward a 30 °C setpoint, so the appropriate directional susceptibility is the Module 4 heating value

$$
\chi_{T,h}=0.4872\ \frac{^\circ\mathrm C}{\mathrm{PWM\ count}}.
$$

With $T_{\mathrm{amb}}=22^\circ$C, the initial setpoint displacement is

$$
T_{\mathrm{set}}-T_{\mathrm{amb}}=30-22=8^\circ\mathrm C.
$$

For each gain,

$$
L=K_p\chi_{T,h},
\qquad
\text{measured fractional droop}
=\frac{T_{\mathrm{set}}-T_{\mathrm{ss}}}{8},
\qquad
\text{predicted fractional droop}=\frac{1}{1+L}.
$$

| $K_p$ (PWM/°C) | $L=K_p\chi_{T,h}$ | Measured droop (°C) | Measured fractional droop | Predicted $1/(1+L)$ | Measured − predicted |
|---:|---:|---:|---:|---:|---:|
| 0.25 | 0.1218 | 6.65 | 0.8313 | 0.8914 | -0.0602 |
| 0.50 | 0.2436 | 5.80 | 0.7250 | 0.8041 | -0.0791 |
| 1.00 | 0.4872 | 4.87 | 0.6088 | 0.6724 | -0.0637 |
| 2.00 | 0.9744 | 3.73 | 0.4662 | 0.5065 | -0.0402 |
| 3.00 | 1.4616 | 2.90 | 0.3625 | 0.4062 | -0.0437 |
| 6.00 | 2.9232 | 1.76 | 0.2200 | 0.2549 | -0.0349 |
| 10.00 | 4.8720 | 1.18 | 0.1475 | 0.1703 | -0.0228 |
| 30.00 | 14.6160 | 0.44 | 0.0550 | 0.0640 | -0.0090 |

The $K_p=0.25$ run most clearly has small loop gain, with $L=0.1218\ll1$. The $K_p=0.50$ run is also in the low-gain range but is less strongly separated from one. The $K_p=1$ run is intermediate, the $K_p=2$ run is near $L=1$, and the larger gains have $L>1$ and substantially less fractional droop.

For every gain, the measured fractional droop is slightly smaller than the one-lump prediction, meaning the measured temperature settled somewhat closer to the setpoint than predicted. Plausible reasons include uncertainty in the true ambient temperature, using a single susceptibility measured over a different temperature/PWM range, PWM rounding at low gains, incomplete settling, nonlinear passive heat transfer, and temperature dependence of TEC properties. The heating susceptibility was used because every run commanded heating; using the cooling susceptibility would not represent these experiments.
