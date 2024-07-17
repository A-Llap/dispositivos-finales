from paho.mqtt.client import Client, MQTTMessage
from paho.mqtt.enums import CallbackAPIVersion
import random
import json
from matplotlib import pyplot as plt
import datetime
import os


broker = '<url>'
port = 8883
topic = 'centralEsp32/temperature'
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = '<username>'
password = '<password>'


# consumir todos los mensajes del broker y guardarlos en jsonl
# plotear todo jsonl
# actualizar plot con cada nueva entrada y guardarla en en jsonl

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, props):
        print(client, userdata, flags, rc, props)
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = Client(
        client_id=client_id,
        callback_api_version=CallbackAPIVersion.VERSION2
    )
    # Set CA certificate
    client.tls_set(ca_certs='./server-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


cdict = {0: 'red', 1: 'blue', 2: 'green', 3: 'cyan', 4: 'magenta', 5: 'teal'}


def plot_jsonl(jsonlfile: str):
    xs: dict[int, list] = {}
    ys: dict[int, list] = {}

    with open(jsonlfile, 'r', encoding='utf-8') as f:
        for line in f:
            json_message = json.loads(line)

            node = json_message['node']
            time = json_message['time']
            temperature = json_message['temperature']

            true_time = datetime.datetime.fromtimestamp(time)

            if node not in xs:
                xs[node] = []
                ys[node] = []

            xs[node].append(true_time)
            ys[node].append(temperature)

    for node in xs:
        plt.plot(xs[node], ys[node], color=cdict[node],
                 label=f'Node {node}', marker='o', markersize=3)
        # set x-axis format
        plt.gcf().autofmt_xdate()

    plt.draw()
    plt.pause(0.1)
    plt.clf()


def subscribe(client: Client):
    def on_message(client, userdata, msg: MQTTMessage):
        decoded_message = msg.payload.decode()
        json_message = json.loads(decoded_message)

        with open('./temperature.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps(json_message))
            f.write('\n')

        plot_jsonl('./temperature.jsonl')

    client.subscribe(topic, qos=0)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)

    plt.ion()
    if os.path.exists('./temperature.jsonl'):
        plot_jsonl('./temperature.jsonl')
    client.loop_forever()


if __name__ == '__main__':
    run()
