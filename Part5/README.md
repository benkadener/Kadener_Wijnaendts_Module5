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
| 60 | Yes | 29.76 | 3.15 | 9.2 | 0.11 | No |
| 120 | Yes | 29.76 | 3.15 | 9.2 | 0.11 | No |

`N/A` is used because none of the three runs showed sustained oscillations.

## Response observations

- **Kₚ = 6:** started at 23.75 °C, so P₀ = 6 × |30 − 23.75| = 37.5, which rounds to PWM 38. The response rose smoothly and settled near 28.24 °C. PWM settled near 11 and did not saturate.
- **Kₚ = 10:** started at 23.60 °C, so P₀ = 10 × |30 − 23.60| = PWM 64. The response was smooth with small measurement fluctuations and settled near 28.82 °C. PWM settled near 12 and did not saturate.
- **Kₚ = 30:** started at 26.80 °C, so P₀ = 30 × |30 − 26.80| = PWM 96. The response had a small damped transient but no sustained oscillation, then settled near 29.56 °C. PWM settled near 13 and did not saturate.
