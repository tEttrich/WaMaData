import json
import connect_wlan
import time
import gc

from umqtt.simple import MQTTClient
from machine import Pin, I2C, Timer
from imu import MPU6050

DeviceName = 'wama01'
MqttServer = '192.168.178.49'
MqttPort = 1883
MqttC = MQTTClient(DeviceName, MqttServer, MqttPort)


def read_imu(tim):
    global DataCounter, imuReadings
    accel = mpu6050.accel
    imuReadings.append(accel.xyz)
    DataCounter += 1


def start_sampling(i2c):
    # Reading 100 values from the IMU with 100Hz
    print("Acquiring Data...")

    tim = Timer(-1)
    tim.init(period=100, mode=Timer.PERIODIC, callback=read_imu)

    while (True):
        if DataCounter > 99:
            tim.deinit()
            break


if __name__ == "__main__":
    connect_wlan.connect()
    connect_wlan.synchronize_rtc()

    led = Pin(2, Pin.OUT)

    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
    mpu6050 = MPU6050(i2c)

    # sample and publish sensor data every 30 seconds
    while True:
        DataCounter = 0
        imuReadings = []
        led.off()

        t = time.time()
        start_sampling(mpu6050)  # writes sensor data to list 'imuReadings'

        MqttC.connect()

        # publish every single dataset from list 'imuReadings'
        for i in imuReadings:
            # formatting the tuple of floats to .5f
            i = '{0:3.5f},{1:3.5f},{2:3.5f}\n'.format(i[0], i[1], i[2])
            j = tuple(float(s) for s in i.strip("()").split(","))
            ax, ay, az = j

            # create and format timestamp
            ts = time.localtime(t)
            dt = "{0}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}".format(ts[0], ts[1], ts[2], ts[3], ts[4], ts[5])

            # create message string
            msg = json.dumps({'dev': 'wama01',
                              'datetime': dt,
                              'time': t,
                              'x_a': ax,
                              'y_a': ay,
                              'z_a': az})

            # publish message
            try:
                MqttC.publish('/WaMaProject/data', msg)
                time.sleep(0.01)
            except Exception as e:
                print("Exception publish: " + str(e))

        MqttC.disconnect()

        led.on()
        gc.collect
        time.sleep(30)
