from machine import Pin, I2C
from time import sleep
import scd4x

# Adjust I2C pins for your Pico wiring
i2c = I2C(0, scl=Pin(1), sda=Pin(0))

sensor = scd4x.SCD4X(i2c)

# Stop any ongoing measurements
sensor.stop_periodic_measurement()
sleep(1)

# read serial number
try:
    serial = sensor.serial_number
    print("Sensor serial:", serial)
except Exception as e:
    print("Could not read serial number:", e)
    
# Start periodic measurement
sensor.start_periodic_measurement()
print("Waiting for first measurement...")

while True:
    if sensor.data_ready:
        co2 = sensor.CO2
        temp = sensor.temperature
        rh = sensor.relative_humidity
        print("CO₂: {:.1f} ppm, Temp: {:.2f} °C, RH: {:.1f}%".format(co2, temp, rh))
    sleep(5)