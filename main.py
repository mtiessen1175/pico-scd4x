import network
import time
from machine import Pin, I2C
import ujson
from umqtt.robust import MQTTClient
from scd4x import SCD4X
import time
import config

#---------- STATIC VALUES -----------
# Publishing interval (seconds)
PUBLISH_INTERVAL = 30
# MQTT setup
MQTT_BROKER = config.mqtt_server
MQTT_TOPIC = config.mqtt_topic
MQTT_USER = config.mqtt_username
MQTT_PASS = config.mqtt_password
MQTT_SSL_PARAMS = {'server_hostname': MQTT_BROKER}
MQTT_SSL = False
MQTT_KEEPALIVE = 120
MQTT_PORT = 0
# Wi-Fi credentials
SSID = config.wifi_ssid
PASSWORD = config.wifi_password

#---------- VISUAL FEEDBACK -----------
# check visually that main.py is running on microcontroller
led = machine.Pin("LED", machine.Pin.OUT)

def blink(n=3, delay=0.3):
    for _ in range(n):
        led.toggle()
        time.sleep(delay)
    led.off()
    
def reconnect_mqtt(client, MQTT_TOPIC):
    try:
        client.connect()  # try to reconnect
        client.publish(MQTT_TOPIC + "/status", b"online", retain=True)
    except Exception as e:
        print("Reconnection failed:", e)

blink(5)  # boot-up blink sequence


#---------- WiFi Connection -----------
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Wait for connection
max_wait = 15
while max_wait > 0:
    led.toggle()
    if wlan.isconnected():
        blink(2)
        print("Wi-Fi connected")
        break
    print("Waiting for Wi-Fi...")
    max_wait -= 1
    time.sleep(1)

if not wlan.isconnected():
    print("Wi-Fi failed to connect")
    blink(20, 0.1)
    machine.reset()  # optional: reset and try again


#---------- MQTT Connection -----------
client = MQTTClient(b"pico1",
                    server=MQTT_BROKER,
                    port=MQTT_PORT,
                    user=MQTT_USER,
                    password=MQTT_PASS,
                    keepalive=MQTT_KEEPALIVE,
                    ssl=MQTT_SSL,
                    ssl_params=MQTT_SSL_PARAMS
                    )

client.set_last_will(MQTT_TOPIC + "/status", b"offline", retain=True)

try:
    client.connect()
    client.publish(MQTT_TOPIC + "/status", b"online", retain=True)
    print("Connected to MQTT")
    blink(3)
except Exception as e:
    print("MQTT connection failed:", e)
    blink(10, 0.1)
    machine.reset()


#---------- Sensor setup -----------
print("Waiting for sensor to power up...")
time.sleep(3)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=10000)
# Try to find the sensor on the bus
found = False
for i in range(10):
    devices = i2c.scan()
    print("I2C scan:", devices)
    if 0x62 in devices:  # 0x62 is the SCD4x address
        found = True
        break
    time.sleep(1)

if found:
    sensor = SCD4X(i2c)
else:
    print("Sensor not found, halting")
    for _ in range(3):
        blink(1, 0.2)
        time.sleep(1)


for i in range(3):
    try:
        sensor.start_periodic_measurement()
        print("Warming up...")
        time.sleep(6)
        print("Sensor measurement started")
        break
    except Exception as e:
        print(f"Sensor init attempt {i+1} failed:", e)
        time.sleep(2)
else:
    print("Sensor failed to start after retries")
    blink(10, 0.1)
    machine.reset()


#---------- MAIN LOOP -----------
no_data_count = 0
while True:
    try:
        try:
            # important to establish connection with MQTT broker and prevent keepalive timeout
            client.check_msg()
        except Exception as e:
            print("Error receiving MQTT messages:", e)
        
        if not wlan.isconnected():
            print("Wi-Fi dropped, reconnecting...")
            wlan.connect(SSID, PASSWORD)
            time.sleep(5)
        print("Waiting for sensor measurement...")            
        if sensor.data_ready:
            co2 = sensor.CO2
            temp = round(sensor.temperature, 2)
            hum = round(sensor.relative_humidity, 2)

            payload = ujson.dumps({
                "co2": co2,
                "temperature": temp,
                "humidity": hum
            })
            
            MAX_RETRIES = 3
            retry = 0
            no_data_count = 0

            while retry < MAX_RETRIES:
                try:
                    client.publish(MQTT_TOPIC, payload)
                    print("Published:", payload)
                    led.on()
                    time.sleep(0.2)
                    led.off()
                    break
                except Exception as e:
                    print("MQTT publish failed:", e)
                    retry += 1
                    reconnect_mqtt(client, MQTT_TOPIC)
                    time.sleep(2)
        else: #if not sensor.data_ready
            no_data_count += 1
            if no_data_count > 3:
                print("Sensor not responding, restarting measurement")
                sensor.start_periodic_measurement()
                time.sleep(6)
                no_data_count = 0
        
        # ping the MQTT broker to not loose connection
        try:
            client.ping()
        except Exception as e:
            print("MQTT ping failed:", e)
            reconnect_mqtt(client, MQTT_TOPIC)
        
        # publishing interval
        time.sleep(PUBLISH_INTERVAL)

    except Exception as e:
        print("Error in main loop:", e)
        blink(8, 0.1)
        reconnect_mqtt(client, MQTT_TOPIC)
