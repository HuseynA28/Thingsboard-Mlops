from tb_device_mqtt import TBDeviceMqttClient
import csv
import time
from datetime import datetime
import math

from dotenv import load_dotenv
import os
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
HOST = "localhost"
PORT = 1883


def update_timestamp(old_ts):
    # Convert original timestamp to datetime
    old_date = datetime.fromtimestamp(float(old_ts))
    # Create new timestamp with current year but same month/day/time
    current_year = datetime.now().year
    new_date = datetime(current_year, old_date.month, old_date.day, 
                       old_date.hour, old_date.minute, old_date.second)
    return int(new_date.timestamp())

def read_and_send_data(client, csv_file):
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            telemetry = {
                "co": (float(row["co"]) * 100),
                "humidity": (float(row["humidity"])),
                "light": row["light"].lower() == "true",
                "lpg": (float(row["lpg"]) * 100),
                "motion": row["motion"].lower() == "true", 
                "smoke": (float(row["smoke"]) * 100),
                "temp": (float(row["temp"]))
            }
                
            try:
                client.send_telemetry({
                    "ts": update_timestamp(row["ts"]) * 1000,
                    "values": telemetry
                })
                print(f"Successfully sent data for device: {row['device']}")
            except Exception as e:
                print(f"Failed to send data: {e}")
            
            time.sleep(0.5)

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