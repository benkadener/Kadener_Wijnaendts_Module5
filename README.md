# Part 6: Submit A2

## A2: TEC Heating and Cooling Analysis

- **Type:** Team assignment, 10 points
- **Due:** Wednesday, October 7, at 6:00 PM
- **Moodle filename:** `A2_Lastname_Lastname.pdf`
- **Moodle submission:** Each student uploads the team PDF separately; teammates may upload the same PDF.
- **Repository file:** None required for this short analysis.

Submit a concise **one-to-two-page PDF** containing the following numbered sections. Show intermediate algebra, units, and substitutions clearly enough that another student could reproduce every numerical result.

## 1. Part 4: Combined Graph and Fits

Include one temperature-versus-signed-PWM graph containing:

- Heating and cooling data
- A fitted line for each direction
- The PWM range used for each fit
- Clearly labeled axes with units

## 2. Part 5.1: Measured Slopes

Report:

- Heating slope $m_h$ with units
- Cooling-slope magnitude $m_c$ with units
- Measured ratio $r=m_h/m_c$
- Whether either dataset shows visible curvature
- How any curvature affected the chosen fitting range

## 3. Part 5.2: PWM and the Slope-Ratio Model

Show that PWM gives

$$
\langle I\rangle=DI,
\qquad
\langle I^2\rangle=DI^2.
$$

Use the steady-state energy balance to derive the heating and cooling slopes and show that

$$
\frac{\dot Q_J}{\dot Q_P}=\frac{r-1}{r+1}.
$$

Substitute the measured value of $r$ and report the numerical value of $\dot Q_J/\dot Q_P$.

## 4. Part 5.3: Laird Datasheet Calculation

Cite the Laird datasheet page or table used to obtain:

- Module resistance $R_M$
- Maximum current $I_{\max}$
- Maximum cold-side heat pumping $Q_{c,\max}$
- Maximum temperature difference $\Delta T_{\max}$

For every value, state its units, meaning, and operating conditions. Calculate $\dot Q_{J,\max}$, infer $\dot Q_{P,\max}$, and then calculate

$$
r_{\mathrm{Laird},\max}
=\frac{\dot Q_{P,\max}+\dot Q_{J,\max}}
{\dot Q_{P,\max}-\dot Q_{J,\max}}.
$$

This is the heating-to-cooling slope ratio predicted from the datasheet maximum-current values.

## 5. Part 5.4: Compare the Ratios

Compare the measured $r$ with $r_{\mathrm{Laird},\max}$. Explain why exact agreement is not required, including why a duty cycle of $D=1$ does not necessarily mean that $I=I_{\max}$.

## 6. Part 5.4: Passive Conduction

State the direction of passive heat flow when the object is:

- Hotter than room temperature
- Colder than room temperature

Explain why approximately symmetric passive conduction opposes both heating and cooling but cannot, by itself, explain unequal heating and cooling slope magnitudes.

## Do Not Include

Do not repeat the C2/C3 circuit sketches, apparatus descriptions, safety demonstration, or code documentation. Retain the class data and working code for later modules, but no new Git checkpoint is required for this short assignment.

## A2 Rubric

| Criterion | Points |
|---|---:|
| Items 1–2: Part 4 graph, measured slopes, units, fitting ranges, and ratio are clearly presented | 2 |
| Item 3: PWM averaging proof, steady-state energy balance, slope-ratio derivation, and numerical result are correct | 3 |
| Item 4: Relevant Laird values and operating conditions are correctly located, cited, interpreted, and used in a dimensionally clear calculation | 2 |
| Items 5–6: Comparison and passive-conduction explanation show sound physical reasoning | 2 |
| PDF is concise, legible, and complete | 1 |
| **Total** | **10** |
