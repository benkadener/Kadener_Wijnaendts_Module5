"""Overlay measured Part 3 droop and the Module 4 model prediction."""

from pathlib import Path

import matplotlib.pyplot as plt


GAINS = [0.25, 0.50, 1.00, 2.00, 3.00]
MEASURED_DROOP_C = [6.65, 5.80, 4.87, 3.73, 2.90]
HEATING_SUSCEPTIBILITY_C_PER_PWM = 0.4872
SETPOINT_C = 30.0
AMBIENT_C = 22.0
OUTPUT_PATH = Path(__file__).with_name("predicted_vs_measured_droop.png")


initial_error = SETPOINT_C - AMBIENT_C
predicted_droop = [
	initial_error / (1 + HEATING_SUSCEPTIBILITY_C_PER_PWM * gain)
	for gain in GAINS
]

figure, axes = plt.subplots(figsize=(7.2, 4.8), constrained_layout=True)
axes.plot(
	GAINS,
	MEASURED_DROOP_C,
	color="#8f2044",
	marker="o",
	markersize=7,
	linewidth=2,
	label="Measured droop",
)
axes.plot(
	GAINS,
	predicted_droop,
	color="#176b87",
	marker="s",
	markersize=6,
	linewidth=2,
	linestyle="--",
	label="Predicted droop",
)

axes.set_title("Measured and Predicted Droop Versus Gain")
axes.set_xlabel(r"Proportional gain, $K_p$ (PWM/°C)")
axes.set_ylabel("Steady-state droop (°C)")
axes.set_xlim(0, 3.25)
axes.set_ylim(0, 8)
axes.grid(True, color="#d9dee5", linewidth=0.8)
axes.set_axisbelow(True)
axes.legend(frameon=False)

figure.savefig(OUTPUT_PATH, dpi=180)

for gain, measured, predicted in zip(GAINS, MEASURED_DROOP_C, predicted_droop):
	print(
		f"Kp={gain:.2f}: measured={measured:.2f} C, "
		f"predicted={predicted:.2f} C"
	)
print(f"Saved plot: {OUTPUT_PATH}")
