# pip install tb-mqtt-client
from tb_device_mqtt import TBDeviceMqttClient
import csv
import time
from datetime import datetime, timedelta
import math
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
HOST = "localhost"
PORT = 1883

def update_timestamp():
    start_date = datetime(2024, 1, 1)
    
    def date_generator():
        current_date = start_date
        while True:
            yield int(current_date.timestamp())
            current_date += timedelta(minutes=60)
    
    return date_generator()

def read_and_send_data(client, csv_file):
    timestamp_gen = update_timestamp()
    
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            telemetry = {
                "co": round(float(row["co"]) * 1000, 1),
                "humidity": round(float(row["humidity"]), 1),
                "light": row["light"].lower() == "true",
                "lpg": round(float(row["lpg"]) * 1000, 1),
                "motion": row["motion"].lower() == "true", 
                "smoke": round(float(row["smoke"]) * 1000, 1),
                "temp": round(float(row["temp"]), 1)
            }
                
            try:
                client.send_telemetry({
                    "ts": next(timestamp_gen) * 1000,
                    "values": telemetry
                })
                print(f"Successfully sent data for device: {row['device']}")
            except Exception as e:
                print(f"Failed to send data: {e}")
            
            time.sleep(0.3)

try:
    client = TBDeviceMqttClient(HOST, port=PORT, username=ACCESS_TOKEN)
    client.connect()
    print("Connected successfully")
    read_and_send_data(client, 'iot_telemetry_data.csv')
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'client' in locals():
        client.disconnect()