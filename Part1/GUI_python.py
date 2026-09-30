"""Display Arduino temperature measurements in a rolling strip chart."""

import csv
import re
import sys
from collections import deque

import pyqtgraph as pg
import serial
from PySide6 import QtCore, QtGui, QtWidgets


# ---------- Settings to change before running ----------
SERIAL_PORT = "/dev/cu.usbmodem101"
BAUD_RATE = 9600
WINDOW_DURATION_SECONDS = 120.0
UPDATE_INTERVAL_MILLISECONDS = 100
CSV_FILENAME = "temperature_measurements.csv"
INITIAL_SETPOINT_C = 32.5
INITIAL_PROPORTIONAL_GAIN = 1.0


# This matches the serial line printed by the Part 3 Arduino sketch.
MEASUREMENT_LINE = re.compile(
	r"^Temperature \(C\):\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)),\s*"
	r"Time \(s\):\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)),\s*"
	r"PWM:\s*(\d+),\s*Heat/Cool:\s*([01])\s*$"
)


def parse_measurement(line):
	"""Return time, temperature, PWM, and direction, or None if malformed."""
	match = MEASUREMENT_LINE.fullmatch(line.strip())
	if match is None:
		return None

	temperature = float(match.group(1))
	time_seconds = float(match.group(2))
	pwm = int(match.group(3))
	heat_cool = int(match.group(4))

	return time_seconds, temperature, pwm, heat_cool


def calculate_p_control(setpoint, temperature, gain):
	"""Return temperature error, signed output, PWM magnitude, and direction."""
	error = setpoint - temperature
	signed_pwm = gain * error
	direction = "HEAT" if signed_pwm >= 0 else "COOL"
	pwm = max(0, min(255, int(round(abs(signed_pwm)))))
	return error, signed_pwm, pwm, direction


class TemperatureWindow(QtWidgets.QMainWindow):
	"""Read Arduino measurements and provide manual serial controls."""

	def __init__(self):
		super().__init__()
		self.setWindowTitle("TEC Temperature")

		# Keep the rolling chart data separate from the CSV output values.
		self.times = deque()
		self.temperatures = deque()
		self.setpoints = deque()
		self.errors = deque()
		self.signed_pwms = deque()
		self.serial_buffer = b""
		self.latest_temperature = None
		self.setpoint = INITIAL_SETPOINT_C
		self.proportional_gain = INITIAL_PROPORTIONAL_GAIN

		# Create the manual controls and the live values shown above the plots.
		controls = QtWidgets.QGroupBox("Manual controls")
		controls_layout = QtWidgets.QGridLayout(controls)

		self.direction_switch = QtWidgets.QCheckBox("HEAT")
		self.direction_switch.setChecked(True)
		self.direction_switch.toggled.connect(self.direction_changed)
		controls_layout.addWidget(QtWidgets.QLabel("Direction"), 0, 0)
		controls_layout.addWidget(self.direction_switch, 0, 1)

		self.pwm_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
		self.pwm_slider.setRange(0, 255)
		self.pwm_slider.setValue(0)
		self.pwm_slider.valueChanged.connect(self.slider_changed)
		controls_layout.addWidget(QtWidgets.QLabel("PWM"), 1, 0)
		controls_layout.addWidget(self.pwm_slider, 1, 1)

		self.pwm_input = QtWidgets.QLineEdit("0")
		self.pwm_input.setValidator(QtGui.QIntValidator(0, 255, self))
		self.pwm_input.setMaximumWidth(80)
		self.pwm_input.editingFinished.connect(self.text_pwm_changed)
		controls_layout.addWidget(self.pwm_input, 1, 2)

		self.p_mode_switch = QtWidgets.QCheckBox("P-only mode")
		self.p_mode_switch.toggled.connect(self.p_mode_changed)
		controls_layout.addWidget(self.p_mode_switch, 2, 0)

		self.setpoint_input = QtWidgets.QLineEdit(str(INITIAL_SETPOINT_C))
		self.setpoint_input.setValidator(QtGui.QDoubleValidator(30.0, 35.0, 2, self))
		self.setpoint_input.setMaximumWidth(80)
		self.setpoint_input.editingFinished.connect(self.setpoint_changed)
		controls_layout.addWidget(QtWidgets.QLabel("Setpoint (30-35 C)"), 2, 1)
		controls_layout.addWidget(self.setpoint_input, 2, 2)

		self.gain_input = QtWidgets.QLineEdit(str(INITIAL_PROPORTIONAL_GAIN))
		self.gain_input.setValidator(QtGui.QDoubleValidator(0.0, 1000.0, 2, self))
		self.gain_input.setMaximumWidth(80)
		self.gain_input.editingFinished.connect(self.gain_changed)
		controls_layout.addWidget(QtWidgets.QLabel("Kp (PWM/C)"), 3, 1)
		controls_layout.addWidget(self.gain_input, 3, 2)

		self.temperature_value = QtWidgets.QLabel("-- C")
		self.pwm_value = QtWidgets.QLabel("--")
		self.direction_value = QtWidgets.QLabel("--")
		self.time_value = QtWidgets.QLabel("-- s")
		self.error_value = QtWidgets.QLabel("-- C")
		self.signed_pwm_value = QtWidgets.QLabel("--")
		live_values = QtWidgets.QFormLayout()
		live_values.addRow("Temperature", self.temperature_value)
		live_values.addRow("PWM", self.pwm_value)
		live_values.addRow("Direction", self.direction_value)
		live_values.addRow("Elapsed time", self.time_value)
		live_values.addRow("Error", self.error_value)
		live_values.addRow("Requested u", self.signed_pwm_value)
		controls_layout.addLayout(live_values, 0, 3, 4, 1)

		# The first plot displays the measured temperature over Arduino time.
		self.temperature_plot = pg.PlotWidget()
		self.temperature_plot.setLabel("bottom", "Time", units="s")
		self.temperature_plot.setLabel("left", "Temperature", units="C")
		self.temperature_plot.enableAutoRange()
		self.temperature_plot.showGrid(x=True, y=True, alpha=0.25)
		self.temperature_plot.addLegend()
		self.temperature_curve = self.temperature_plot.plot(
			pen=pg.mkPen("#d95f02", width=2), name="Temperature"
		)
		self.setpoint_curve = self.temperature_plot.plot(
			pen=pg.mkPen("#008c95", width=2, style=QtCore.Qt.PenStyle.DashLine),
			name="Setpoint",
		)
		# Plot error separately because it is a temperature difference rather than
		# an absolute temperature.
		self.error_plot = pg.PlotWidget()
		self.error_plot.setLabel("bottom", "Time", units="s")
		self.error_plot.setLabel("left", "Error (setpoint - measured)", units="C")
		self.error_plot.showGrid(x=True, y=True, alpha=0.25)
		self.error_curve = self.error_plot.plot(pen=pg.mkPen("#555555", width=2))

		# A signed PWM plot displays magnitude and direction at the same time:
		# positive is HEAT, negative is COOL, and zero is off.
		self.pwm_plot = pg.PlotWidget()
		self.pwm_plot.setLabel("bottom", "Time", units="s")
		self.pwm_plot.setLabel("left", "Signed PWM (+ heat / - cool)")
		self.pwm_plot.setYRange(-255, 255)
		self.pwm_plot.showGrid(x=True, y=True, alpha=0.25)
		self.pwm_curve = self.pwm_plot.plot(pen=pg.mkPen("#7b3294", width=2))

		central_widget = QtWidgets.QWidget()
		layout = QtWidgets.QVBoxLayout(central_widget)
		layout.addWidget(controls)
		layout.addWidget(self.temperature_plot)
		layout.addWidget(self.error_plot)
		layout.addWidget(self.pwm_plot)
		self.setCentralWidget(central_widget)

		# Start with the TEC off and put the Arduino under serial control.
		self.serial_port = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0)
		self.send_control_command(0, "HEAT")
		self.csv_file = open(CSV_FILENAME, "a", newline="")
		self.csv_writer = csv.writer(self.csv_file)
		if self.csv_file.tell() == 0:
			self.csv_writer.writerow(
				["time_s", "temperature_C", "pwm", "heat_cool"]
			)
			self.csv_file.flush()

		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.read_measurements)
		self.timer.start(UPDATE_INTERVAL_MILLISECONDS)

	def set_pwm_value(self, pwm):
		"""Keep the slider and text box synchronized at a valid PWM value."""
		pwm = max(0, min(255, pwm))
		self.pwm_slider.blockSignals(True)
		self.pwm_input.blockSignals(True)
		self.pwm_slider.setValue(pwm)
		self.pwm_input.setText(str(pwm))
		self.pwm_slider.blockSignals(False)
		self.pwm_input.blockSignals(False)
		return pwm

	def send_control_command(self, pwm, direction=None):
		"""Send one direction and PWM command to the Arduino."""
		if direction is None:
			direction = "HEAT" if self.direction_switch.isChecked() else "COOL"
		command = f"SET PWM {pwm} DIR {direction}\n"
		self.serial_port.write(command.encode("ascii"))

	def p_mode_changed(self, enabled):
		"""Enable feedback control or return to safe manual zero output."""
		self.direction_switch.setEnabled(not enabled)
		self.pwm_slider.setEnabled(not enabled)
		self.pwm_input.setEnabled(not enabled)
		if enabled:
			self.update_p_control()
		else:
			self.set_pwm_value(0)
			self.send_control_command(0)

	def setpoint_changed(self):
		"""Validate the setpoint and update an active P controller."""
		try:
			setpoint = float(self.setpoint_input.text())
		except ValueError:
			setpoint = INITIAL_SETPOINT_C
		setpoint = max(30.0, min(35.0, setpoint))
		self.setpoint = setpoint
		self.setpoint_input.setText(f"{setpoint:g}")
		if self.p_mode_switch.isChecked():
			self.update_p_control()

	def gain_changed(self):
		"""Validate the proportional gain and update an active controller."""
		try:
			gain = float(self.gain_input.text())
		except ValueError:
			gain = INITIAL_PROPORTIONAL_GAIN
		gain = max(0.0, min(1000.0, gain))
		self.proportional_gain = gain
		self.gain_input.setText(f"{gain:g}")
		if self.p_mode_switch.isChecked():
			self.update_p_control()

	def update_p_control(self):
		"""Calculate and send P output from the latest measured temperature."""
		if self.latest_temperature is None:
			self.set_pwm_value(0)
			self.send_control_command(0, "HEAT")
			return

		error, signed_pwm, pwm, direction = calculate_p_control(
			self.setpoint,
			self.latest_temperature,
			self.proportional_gain,
		)
		self.error_value.setText(f"{error:.2f} C")
		self.signed_pwm_value.setText(f"{signed_pwm:.2f}")
		self.set_pwm_value(pwm)
		self.direction_switch.setText(direction)
		self.direction_switch.blockSignals(True)
		self.direction_switch.setChecked(direction == "HEAT")
		self.direction_switch.blockSignals(False)
		self.send_control_command(pwm, direction)

	def slider_changed(self, pwm):
		"""Send a command when the user moves the PWM slider."""
		pwm = self.set_pwm_value(pwm)
		self.send_control_command(pwm)

	def text_pwm_changed(self):
		"""Clamp typed PWM input and send the resulting command."""
		try:
			pwm = int(self.pwm_input.text())
		except ValueError:
			pwm = 0
		pwm = self.set_pwm_value(pwm)
		self.send_control_command(pwm)

	def direction_changed(self, heating):
		"""Send the current PWM with the newly selected direction."""
		self.direction_switch.setText("HEAT" if heating else "COOL")
		self.send_control_command(self.pwm_slider.value())

	def read_measurements(self):
		"""Read all currently available lines and process valid ones."""
		if self.serial_port.in_waiting:
			self.serial_buffer += self.serial_port.read(self.serial_port.in_waiting)

		while b"\n" in self.serial_buffer:
			raw_line, self.serial_buffer = self.serial_buffer.split(b"\n", 1)
			line = raw_line.decode("ascii", errors="ignore")
			measurement = parse_measurement(line)
			if measurement is None:
				continue

			time_seconds, temperature, pwm, heat_cool = measurement
			print(
				f"Temperature (C): {temperature:.2f}, "
				f"Time (s): {time_seconds:.2f}, PWM: {pwm}, "
				f"Heat/Cool: {heat_cool}"
			)
			self.csv_writer.writerow(
				[time_seconds, temperature, pwm, heat_cool]
			)
			self.csv_file.flush()

			self.latest_temperature = temperature
			setpoint = self.setpoint
			error = setpoint - temperature
			self.times.append(time_seconds)
			self.temperatures.append(temperature)
			self.setpoints.append(setpoint)
			self.errors.append(error)
			self.signed_pwms.append(pwm if heat_cool else -pwm)

			self.temperature_value.setText(f"{temperature:.2f} C")
			self.pwm_value.setText(str(pwm))
			self.direction_value.setText("HEAT" if heat_cool else "COOL")
			self.time_value.setText(f"{time_seconds:.2f} s")
			self.error_value.setText(f"{error:.2f} C")
			if self.p_mode_switch.isChecked():
				self.update_p_control()
			oldest_time = time_seconds - WINDOW_DURATION_SECONDS
			while self.times and self.times[0] < oldest_time:
				self.times.popleft()
				self.temperatures.popleft()
				self.setpoints.popleft()
				self.errors.popleft()
				self.signed_pwms.popleft()

		# Refresh both plots after processing the available serial data.
		self.temperature_curve.setData(list(self.times), list(self.temperatures))
		self.setpoint_curve.setData(list(self.times), list(self.setpoints))
		self.error_curve.setData(list(self.times), list(self.errors))
		self.pwm_curve.setData(list(self.times), list(self.signed_pwms))

	def closeEvent(self, event):
		"""Turn the TEC off, then close files and the serial connection."""
		self.timer.stop()
		try:
			self.send_control_command(0, "HEAT")
			self.serial_port.flush()
		except serial.SerialException:
			pass
		self.serial_port.close()
		self.csv_file.close()
		event.accept()


def main():
	"""Start the display application."""
	application = QtWidgets.QApplication(sys.argv)
	window = TemperatureWindow()
	window.resize(900, 500)
	window.show()
	sys.exit(application.exec())


if __name__ == "__main__":
	main()
