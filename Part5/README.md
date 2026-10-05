# Part 5: Explore the High-Gain Response

Continue only through the gain range approved by the instructor. Use the same 30 °C setpoint and begin with PWM zero. Test one gain at a time, starting with the lowest approved value.

For each run, record the actual starting temperature and calculate

$$
P_0=K_p\left|30-T_{\mathrm{start}}\right|.
$$

## Results

Use $K_p=3$ as the existing comparison run. Test $K_p=6$ first, and test $K_p=10$ only if the instructor approves it after reviewing the $K_p=6$ response. The listed $P_0$ values assume a 22 °C start; recalculate them using the actual starting temperature.

| $K_p$ (PWM/°C) | Start temp. (°C) | Predicted $P_0$ | Settles? | Mean/steady temp. (°C) | Response shape | PWM behavior | Amplitude (°C) | Period (s) | Frequency (Hz) | Saturates? |
|---:|---:|---:|:---:|---:|---|---|---:|---:|---:|:---:|
| 3 | 22.00 | 24 | Yes | 27.10 | Smooth; no sustained oscillations | Initially 24, approximately 9 when settled | N/A | N/A | N/A | No |
| 6 |  | 48 if starting at 22 °C |  |  |  |  |  |  |  |  |
| 10 |  | 80 if starting at 22 °C |  |  |  |  |  |  |  |  |

Use `N/A` for amplitude, period, and frequency if sustained oscillations do not occur. In **Response shape**, describe whether the response is smooth, overshoots, oscillates, or fails to settle. In **PWM behavior**, record its approximate range and whether it switches rapidly.

## Oscillation measurements

Ignore the initial transient and use a later repeating section. Define amplitude as half the peak-to-peak temperature:

$$
A=\frac{T_{\max}-T_{\min}}{2}.
$$

Measure the period between successive peaks and calculate frequency:

$$
\tau=t_{\mathrm{peak,2}}-t_{\mathrm{peak,1}},
\qquad
f=\frac{1}{\tau}.
$$

## Evidence and conclusion

Save one strip-chart screenshot and the raw data for every tested gain. If no sustained oscillations appear, report the highest gain tested and compare it with the low-gain response: settling temperature, droop, response speed, and PWM behavior.

Stop P-only control and set PWM to zero immediately if oscillations grow, the temperature moves in the wrong direction, PWM behaves unexpectedly, or the run becomes unsafe. Do not proceed to the next gain without supervision and approval.
