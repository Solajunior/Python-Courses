from abc import ABC, abstractmethod


class SmartDevice(ABC):
	"""Common interface for every device managed by the command center."""

	def __init__(self, name):
		self.name = name
		self.is_on = False

	@abstractmethod
	def execute_command(self, command):
		"""Each device must define how it handles a command."""
		raise NotImplementedError

	@abstractmethod
	def status(self):
		"""Each device must define the status it reports."""
		raise NotImplementedError


class SmartLight(SmartDevice):
	def __init__(self, name):
		super().__init__(name)
		self.brightness = 50

	def execute_command(self, command):
		if command == "on":
			self.is_on = True
			return f"{self.name} is now on."
		if command == "off":
			self.is_on = False
			return f"{self.name} is now off."
		if command.startswith("brightness "):
			try:
				brightness = int(command.split()[1])
			except (IndexError, ValueError):
				return "Brightness must be a number from 0 to 100."
			if 0 <= brightness <= 100:
				self.brightness = brightness
				return f"{self.name} brightness set to {brightness}%."
			return "Brightness must be from 0 to 100."
		return f"{self.name} does not understand '{command}'."

	def status(self):
		power = "on" if self.is_on else "off"
		return f"{self.name}: {power}, brightness {self.brightness}%"


class SmartFan(SmartDevice):
	def __init__(self, name):
		super().__init__(name)
		self.speed = 1

	def execute_command(self, command):
		if command == "on":
			self.is_on = True
			return f"{self.name} is now on."
		if command == "off":
			self.is_on = False
			return f"{self.name} is now off."
		if command.startswith("speed "):
			try:
				speed = int(command.split()[1])
			except (IndexError, ValueError):
				return "Fan speed must be a number from 1 to 3."
			if 1 <= speed <= 3:
				self.speed = speed
				return f"{self.name} speed set to {speed}."
			return "Fan speed must be from 1 to 3."
		return f"{self.name} does not understand '{command}'."

	def status(self):
		power = "on" if self.is_on else "off"
		return f"{self.name}: {power}, speed {self.speed}"


class SmartLock(SmartDevice):
	def __init__(self, name):
		super().__init__(name)
		self.is_locked = True

	def execute_command(self, command):
		if command == "lock":
			self.is_locked = True
			return f"{self.name} is locked."
		if command == "unlock":
			self.is_locked = False
			return f"{self.name} is unlocked."
		return f"{self.name} does not understand '{command}'."

	def status(self):
		lock_state = "locked" if self.is_locked else "unlocked"
		return f"{self.name}: {lock_state}"


class CommandCenter:
	def __init__(self, devices):
		self.devices = {device.name.lower(): device for device in devices}

	def send_command(self, device_name, command):
		device = self.devices.get(device_name.lower())
		if device is None:
			return f"No device named '{device_name}'."
		return device.execute_command(command.lower())

	def show_status(self):
		for device in self.devices.values():
			print(device.status())

	def run(self):
		print("SMART DEVICE COMMAND CENTER")
		print("Commands: list, use <device> <command>, or quit")
		print("Examples: use living room light on | use front door unlock")

		while True:
			request = input("\ncommand> ").strip()
			if request.lower() == "quit":
				print("Command center closed.")
				break
			if request.lower() == "list":
				self.show_status()
				continue
			if request.lower().startswith("use "):
				device_request = request[4:].lower()
				device_name = next(
					(name for name in sorted(self.devices, key=len, reverse=True)
					 if device_request.startswith(name + " ")),
					None,
				)
				if device_name is None:
					print("Use: use <device name> <command>")
					continue
				command = device_request[len(device_name):].strip()
				print(self.send_command(device_name, command))
				continue
			print("Unknown command. Try list, use <device> <command>, or quit.")


if __name__ == "__main__":
	devices = [
		SmartLight("living room light"),
		SmartFan("bedroom fan"),
		SmartLock("front door"),
	]
	command_center = CommandCenter(devices)
	command_center.run()
