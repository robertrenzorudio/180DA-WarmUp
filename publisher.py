import argparse
import paho.mqtt.client as mqtt
import random
import sys
import time

broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt/"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        print(f"Connection returned code: {rc}")

    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)

    return client

def publish(client: mqtt, msg):
    status, _ = client.publish(topic, msg)

    if status == 0:
        print(f"Sending: {msg}")
    else:
        print("Error in sending a message")

def main():
    global port, topic

    usg_msg = "python3 {} -p [PORT] -t [TOPIC]\n".format(sys.argv[0])
    parser = argparse.ArgumentParser(usage=usg_msg)
    parser.add_argument("-p", type=int, required=False, help=f"Port Number (Default = {port})")
    parser.add_argument("-t", type=str, required=False, help=f"Topic (Default = {topic})")
    args = parser.parse_args()

    # Parse arguments
    port = args.p if args.p else port
    topic = args.t if args.t else topic

    client = connect_mqtt()
    client.loop_start()

    i = 0
    while True:
        time.sleep(0.5)
        publish(client, str(i))
        i += 1

if __name__ == "__main__":
    main()
