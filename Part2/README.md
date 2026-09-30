# Part 2: Sign Test at Low Gain

## Choosing a low gain

From the Module 4 steady-state fits, the temperature susceptibilities are:

- Heating: $\chi_{T,h}=0.49\ ^\circ\mathrm{C/PWM}$
- Cooling magnitude: $|\chi_{T,c}|=0.20\ ^\circ\mathrm{C/PWM}$

The corrected room temperature is approximately $T_{\mathrm{amb}}=22^\circ$ C. This changes temperature differences and initial errors, but a constant temperature offset does not change the fitted slopes. The Module 4 graph shows about $35^\circ$ C at zero PWM; if that point was recorded before the apparatus reached equilibrium, the slopes may also be inaccurate and should be checked with the instructor.

The dimensionless loop gain is

$$
L=K_p|\chi_T|.
$$

This compares the controller gain with the measured response of the apparatus. The assignment defines low gain as $L\ll1$. We choose $L=0.1$ as a practical low-gain target; it is a chosen test value, not another measurement.

Solving $K_p=L/|\chi_T|$ gives

$$
K_{p,h}=\frac{0.1}{0.49}\approx0.20\ \mathrm{PWM}/^\circ\mathrm C,
$$

$$
K_{p,c}=\frac{0.1}{0.20}=0.50\ \mathrm{PWM}/^\circ\mathrm C.
$$

Because the Arduino receives integer PWM values, these gains may round to zero for very small errors. If the temperature trend is not visible, use $K_p=1.0$. This gives $L_h=0.49$ and $L_c=0.20$, which are still below one but are not as strongly in the $L\ll1$ range.

## Test procedure

1. Set PWM to zero and let the measured temperature settle near $22^\circ$ C.
2. Enter the chosen $K_p$ in the GUI.
3. **Heating:** use a setpoint such as $30^\circ$ C. Enable P-only mode and confirm positive error, positive signed PWM, `HEAT`, and increasing temperature.
4. **Cooling:** the instructions require a setpoint slightly below room temperature. The GUI currently permits only $30$--$35^\circ$ C, so obtain instructor approval before lowering its setpoint range. With an approved setpoint below $22^\circ$ C, confirm negative error, negative signed PWM, `COOL`, and decreasing temperature. A $30^\circ$ C setpoint while the block is at $22^\circ$ C would command heating, not cooling.
5. Disable P-only mode after confirming each trend. Stop immediately if the temperature moves in the wrong direction.

For a $32.5^\circ$ C setpoint, the corrected initial error and estimated open-loop heating PWM are

$$
e_0=32.5-22=10.5^\circ\mathrm C,
\qquad
P_{\mathrm{required}}\approx\frac{10.5}{0.49}\approx21\ \mathrm{counts}.
$$

Save the screenshots, raw CSV data, initial temperatures, setpoints, $K_p$ values, and calculated $L$ values for both tests.
