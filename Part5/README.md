# Part 5: Explore the High-Gain Response

Continue only through the gain range approved by the instructor. Use the same 30 °C setpoint and begin with PWM zero. Test one gain at a time, starting with the lowest approved value.

For each run, record the actual starting temperature and calculate

$$
P_0=K_p\left|30-T_{\mathrm{start}}\right|.
$$

## Results

| $K_p$ (PWM/°C) | Settles? | Mean/steady temperature (°C) | Amplitude (°C) | Period (s) | Frequency (Hz) | Saturation? |
|---:|:---:|---:|---:|---:|---:|:---:|
| 6 | Yes | 28.24 | N/A | N/A | N/A | No |
| 10 | Yes | 28.82 | N/A | N/A | N/A | No |
| 30 | Yes | 29.56 | N/A | N/A | N/A | No |
| 60 | Yes | 29.76 | 31.5 | 9.2 | 0.11 | Yes |
| 120 | Yes | 29.9 | 32.43 | 9.05 | 0.11 | Yes |

The amplitude recorded for each Kp is the amplitude of the first oscillation. Otherwise, it is the max amplitude observed during the trial.

`N/A` is used because none of the three runs showed sustained oscillations.