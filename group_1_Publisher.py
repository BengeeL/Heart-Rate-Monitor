# GROUP 1

# Benjamin 
# Paige
# Harpreet
# Gwen 

import random
import threading
import time
import paho.mqtt.client as mqtt
from group_1_Utils import Utils
from group_1_HeartRateSensor import HeartRateSensor

MQTT_BROKER = 'localhost'
PORT = 1883

class Publisher:
    def __init__(self, topic, user):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        
        self.heart_sensor = HeartRateSensor()
        self.utils = Utils()

        self.topic = topic
        self.user = user
        self.is_publishing = False  

    def connect(self, topic, user):
        print("Connect")

        # Update Params
        self.topic = topic
        self.user = user

        # Connect to Broker
        self.client.connect(MQTT_BROKER, PORT)

    def disconnect(self):
        print("Disconnect")

        # Stop Publisher
        if (self.is_publishing):
            self.stop_publish()

        # Disconnect from the Broker
        self.client.disconnect()

    def update_sensor(self, heart_state, min_fluctuation, max_fluctuation):
        # Heart beats per min for resting and active heart
        base_rates_options = {
            "resting": 70,
            "active": 140,
        }

        # Get current median for heart beat. Default to 70 
        base_rate = base_rates_options.get(heart_state, 70) 

        # Update Heart Sensor
        self.heart_sensor = HeartRateSensor(base_rate, min_fluctuation, max_fluctuation)
        print(f"Heart Sensor Updated: " +
              f"Base Rate = {base_rate}, " + 
              f"Min Fluct = {min_fluctuation}, " +
              f"Max Fluct = {max_fluctuation}")

    def start_publish(self):
        print("Start Publish")

        self.is_publishing = True  

        # Function to generate packet
        def generate_heart_rate_data():
            while self.is_publishing:
                # Get Heart Rate Data
                heart_rate = int(self.heart_sensor.get_heart_rate)

                # Format Data
                data = self.utils.get_json_data(heart_rate, self.user)
                print(f'{data}')

                # Simulate miss transmission for 1% probability
                if random.random() < 0.01:
                    print("Simulating data loss for data:", data)
                else:
                    self.client.publish(self.topic, data)   

                time.sleep(1) 

        # Start a separate thread for publishing to avoid blocking the GUI
        threading.Thread(target=generate_heart_rate_data).start()

    def stop_publish(self):
        print("Stop Publish")

        self.is_publishing = False 
        

if __name__ == '__main__':
    topic = 'DEBUG' 
    sub = Publisher(topic)
    sub.run()