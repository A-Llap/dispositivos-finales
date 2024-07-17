from paho.mqtt.client import Client, MQTTMessage
from paho.mqtt.enums import CallbackAPIVersion
from matplotlib import pyplot as plt
import pandas as pd

import random
import json
import os


broker = '<url>'
port = 8883
topic = 'centralEsp32/mass'
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


def print_table(jsonlfile: str):
    df = pd.read_json(jsonlfile, lines=True)
    # from unix time
    df['time'] = pd.to_datetime(df['time'], unit='s')
    print(df)


def subscribe(client: Client):
    def on_message(client, userdata, msg: MQTTMessage):
        decoded_message = msg.payload.decode()
        json_message = json.loads(decoded_message)

        with open('./mass.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps(json_message))
            f.write('\n')

        print_table('./mass.jsonl')

    client.subscribe(topic, qos=0)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)

    plt.ion()
    if os.path.exists('./mass.jsonl'):
        print_table('./mass.jsonl')
    client.loop_forever()


if __name__ == '__main__':
    run()