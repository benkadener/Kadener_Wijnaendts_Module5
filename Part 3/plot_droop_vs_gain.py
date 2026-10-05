"""Plot the measured Part 3 steady-state droop versus proportional gain."""

from pathlib import Path

import matplotlib.pyplot as plt


GAINS = [0.25, 0.50, 1.00, 2.00, 3.00]
MEASURED_DROOP_C = [6.65, 5.80, 4.87, 3.73, 2.90]
OUTPUT_PATH = Path(__file__).with_name("droop_vs_gain.png")


figure, axes = plt.subplots(figsize=(7.2, 4.8), constrained_layout=True)
axes.plot(
	GAINS,
	MEASURED_DROOP_C,
	color="#8f2044",
	marker="o",
	markersize=7,
	linewidth=2,
)

for gain, droop in zip(GAINS, MEASURED_DROOP_C):
	axes.annotate(
		f"{droop:.2f} °C",
		(gain, droop),
		xytext=(0, 9),
		textcoords="offset points",
		ha="center",
		fontsize=9,
	)

axes.set_title("Measured Droop Versus Proportional Gain")
axes.set_xlabel(r"Proportional gain, $K_p$ (PWM/°C)")
axes.set_ylabel("Steady-state droop (°C)")
axes.set_xlim(0, 3.25)
axes.set_ylim(0, 7.25)
axes.grid(True, color="#d9dee5", linewidth=0.8)
axes.set_axisbelow(True)

figure.savefig(OUTPUT_PATH, dpi=180)
print(f"Saved plot: {OUTPUT_PATH}")
