# pico-scd4x
Raspberry Pi Pico W and SCD4X sensor

Connecting a SCD4X sensor (temperature, humidity, CO2)* to a Rpi Pico 2W and publish the measurements to an MQTT broker. I used the [MicroPython_SCD4X](https://github.com/peter-l5/MicroPython_SCD4X) driver from peter-l5, which is based on the [adafruit_scd4x.py](https://github.com/adafruit/Adafruit_CircuitPython_SCD4X/blob/main/adafruit_scd4x.py).

Steps:
1. Download the .uf2 firmware from [MicroPython](https://micropython.org/download/RPI_PICO2_W/)
2. Connect the Pico via USB and drag .uf2 to RPI-RP2 drive (flashes the firmware and reboots the Pico)
3. Access Pico via CLI (or use an IDE like [Thonny](https://thonny.org/)).
  - on Linux OS: `apt install picocom`
  - `picocom /dev/ttyACM0 -b 115200` to start the MicroPython REPL on the Pico
  - check if install works:
    ```python
    >>> import machine
    >>> led = machine.Pin("LED", machine.Pin.OUT)
    >>> led.toggle()
    ```
4. Connect the sensor to the Pico and save the main.py on the device in order to read/publish the sensor data (via MQTT)



\* I used the SCD41 sensor from SEED-Studio