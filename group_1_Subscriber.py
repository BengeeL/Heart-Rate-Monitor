# GROUP 1

# Benjamin 
# Paige
# Harpreet
# Gwen 

import threading
import paho.mqtt.client as mqtt

MQTT_BROKER = 'localhost'
PORT = 1883

class Subscriber:
    def __init__(self, topic):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        
        self.topic = topic
        self.is_connected = False
    
    def connect(self, topic):
        # Update Params
        self.topic = topic

        # Connect to Broker
        self.client.connect(MQTT_BROKER, PORT)
        self.client.subscribe(self.topic)
        self.is_connected = True
        print(f'Subscriber connected to : {self.topic}\n...')
        
        # Start background thread for network loop
        self.thread = threading.Thread(target=self.client.loop_forever)
        self.thread.daemon = True  # Set as daemon for proper program termination
        self.thread.start()

    def disconnect(self):
        if self.is_connected:
            self.client.unsubscribe(self.topic)
            self.client.disconnect()
            self.is_connected = False
            print(f'Subscriber disconnected from topic: {self.topic}\n...')

            # Wait for the thread to finish
            self.thread.join() 


if __name__ == '__main__':
    topic = 'DEBUG' 
    sub = Subscriber(topic)
    sub.connect()