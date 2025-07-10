# pico-scd4x
Raspberry Pi Pico W and SCD4X sensor

Connecting a SCD4X sensor (temperature, humidity, CO2)* to a Rpi Pico 2W and publish the measurements to an MQTT broker. I used the [MicroPython_SCD4X](https://github.com/peter-l5/MicroPython_SCD4X) driver from peter-l5, which is based on the [adafruit_scd4x.py](https://github.com/adafruit/Adafruit_CircuitPython_SCD4X/blob/main/adafruit_scd4x.py).

Steps:
1. Download the .uf2 firmware from [MicroPython](https://micropython.org/download/RPI_PICO2_W/)
2. Connect the Pico via USB and drag .uf2 to RPI-RP2 drive (flashes the firmware and reboots the Pico)
3. Access Pico via CLI (or use an IDE like [Thonny](https://thonny.org/)).
    - On Linux OS: `apt install picocom`
    - `picocom /dev/ttyACM0 -b 115200` to start the MicroPython REPL on the Pico
    - Check if install works:
        ```python
        >>> import machine
        >>> led = machine.Pin("LED", machine.Pin.OUT)
        >>> led.toggle()
        ```
4. Upload the MicroPython MQTT client library [robust.py](https://github.com/micropython/micropython-lib/blob/master/micropython/umqtt.robust/umqtt/robust.py)
    - via Thonny:
        1. Open the Files pane (View &rarr; Files).
        2. Navigate to the Pico device.
        3. Right-click &rarr; New Directory &rarr; name it: "umqtt"
        4. Upload *robust.py* into that folder
5. Add a configuration file (*config.py*) and create variables for Wifi and MQTT connections:
    - `wifi_ssid` = local WIFI name
    - `wifi_password` = local WIFI password
    - `mqtt_server` = the server address running the MQTT broker
    - `mqtt_topic` = the MQTT topic to publish the sensor readings to
    - `mqtt_username` = MQTT user (optional, depending on MQTT setup)
    - `mqtt_password` = MQTT password -"-
6. Connect the sensor to the Pico and upload the *main.py* to the device in order to read/publish the sensor data (via MQTT)



Useful resources:
- [Rpi Pico W-Series Documentation](https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf)
- [Rpi Pico GPIO-Connections diagram](https://www.elektronik-kompendium.de/sites/raspberry-pi/2611041.htm)
- [SCD4X sensor datasheets](https://sensirion.com/products/catalog/SEK-SCD41)
- [Mosquitto (Open-source MQTT broker)](https://mosquitto.org/)

Additional helper scripts:
- *I2Cscan.py* checks if sensor can be found on I2C bus
- *sample_read_sensor_data.py* simple script to test read sensor data

\* I used an SCD41 sensor from SEED-Studio