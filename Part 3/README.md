# Part 3: Measure Droop Versus Gain

## Gain selection

Use the corrected Module 4 heating susceptibility:

$$
\chi_{T,h}=0.4872\ ^\circ\mathrm C/\text{PWM count}.
$$

For $T_{\mathrm{amb}}=22^\circ$C and $T_{\mathrm{set}}=30^\circ$C:

$$
e_0=T_{\mathrm{set}}-T_{\mathrm{amb}}=8^\circ\mathrm C,
$$

$$
P_{\mathrm{required}}\approx\frac{8}{0.4872}=16.4,
\qquad
P_0=K_p|e_0|=8K_p.
$$

Have the instructor approve the gain sequence before running it.

## Results

For every gain, begin with PWM 0, enable P-only mode, and wait for the temperature to settle or clearly fail to settle. Calculate droop using

$$
\text{droop}=30^\circ\mathrm C-T_{\mathrm{final}}.
$$

| $K_p$ (PWM/°C) | Predicted $P_0$ | Actual start temperature (°C) | Setpoint (°C) | Final temperature (°C) | Droop (°C) | Final PWM | Notes |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.25 | 2 |  | 30 |  |  |  |  |
| 0.50 | 4 |  | 30 |  |  |  |  |
| 1.00 | 8 |  | 30 |  |  |  |  |
| 2.00 | 16 |  | 30 |  |  |  |  |
| 3.00 | 24 | 22 | 30 | 27.10 |  | 9 |  |

In the Notes column, record whether the response settled, oscillated, saturated, or behaved unexpectedly.

