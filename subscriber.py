import argparse
import paho.mqtt.client as mqtt
import sys

broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt/"

def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        print(f"Connection return code: {rc}")
        subscribe(client)

    def on_disconnect(client, userdata, rc):
        print(f"Disconnected with return code: {rc}") 
    
    def on_message(client, userdata, message):
        print(f"Received message: {message.payload.decode()} on topic {message.topic} with QoS {message.qos})")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker, port)
    return client

def subscribe(client: mqtt):
    client.subscribe(topic)

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
    client.loop_forever()
    
if __name__ == "__main__":
    main() 
