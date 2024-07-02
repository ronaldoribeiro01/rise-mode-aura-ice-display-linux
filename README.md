# Rise Mode Aura Ice Display Linux Support

This Python script reads the CPU temperature from a Linux system and sends the data to Aura Ice Display. The script uses the `sensors` command to retrieve the CPU temperature and the `pyusb` library to communicate with the USB device.

## Installation

1. Clone the repository:

	```bash
	git clone https://github.com/ronaldoribeiro01/rise-mode-aura-ice-display-linux.git
	cd rise-mode-aura-ice-display-linux
	```

2. Install the required Python packages:

	```bash
	pip install -r requirements.txt
	```

3. Install the `lm-sensors` package:

	```bash
	sudo apt-get install lm-sensors
	```

4. Configure `sensors`:

	```bash
	 sudo sensors-detect
	```

## Usage

Run the script with root privileges:

```bash
sudo python rise_mode_aura_ice_display_linux.py
```

## Troubleshooting

- If you encounter permission issues, you might need to run the script as root or adjust the USB device permissions.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
