from machine import I2C, Pin
import time

# Use I2C(0) — GPIO 0 for SDA, GPIO 1 for SCL
i2c = I2C(0, sda=Pin(0), scl=Pin(1))

print("Scanning I2C bus...")
time.sleep(1)

devices = i2c.scan()

if not devices:
    print("No I2C devices found. Check wiring and power.")
else:
    print("I2C device(s) found at address(es):")
    for device in devices:
        print("  - Decimal: {} | Hex: 0x{:02X}".format(device, device))
