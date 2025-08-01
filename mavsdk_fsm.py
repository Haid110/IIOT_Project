import asyncio
import random
from mavsdk import System
import cv2
import numpy as np
import csv
import datetime

# --- NDVI Calculation Example ---
def compute_ndvi(nir_frame, rgb_frame):
    nir = nir_frame.astype(float)
    red = rgb_frame[:, :, 2].astype(float)
    bottom = (nir + red)
    bottom[bottom == 0] = 0.01  # Prevent division by zero
    ndvi = (nir - red) / bottom
    return ndvi

# --- FSM States ---
class DroneFSM:
    def __init__(self):
        self.state = 'TakeOff'
        self.wind_speed = 0.0

    async def run(self):
        drone = System()
        await drone.connect(system_address="udp://:14540")

        print("Connecting to drone...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print("Drone connected!")
                break

        while True:
            if self.state == 'TakeOff':
                print("Taking off...")
                await drone.action.arm()
                await drone.action.takeoff()
                await asyncio.sleep(5)
                self.state = 'Surveying'

            elif self.state == 'Surveying':
                print("Surveying...")
                # Fake NDVI input - replace with real camera frames
                rgb = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
                nir = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
                ndvi = compute_ndvi(nir, rgb)

                stress_area = np.sum(ndvi < 0.3) / ndvi.size
                if stress_area > 0.15:
                    print("NDVI Anomaly Detected!")
                    self.state = 'AnomalyAlert'
                    continue

                self.wind_speed = random.uniform(0, 10)
                if self.wind_speed > 8:
                    print(f"High wind detected: {self.wind_speed} m/s")
                    self.state = 'HighWindAlert'
                    continue

                # Simulate waypoint survey step
                await asyncio.sleep(2)
                self.state = 'AnalyzeFrame'

            elif self.state == 'AnalyzeFrame':
                print("Analyzing Frame...")
                # Analysis already done in Surveying for simplicity
                self.state = 'Surveying'

            elif self.state == 'AnomalyAlert':
                print("Alert: Vegetation stress area high!")
                self.state = 'ReturnBase'

            elif self.state == 'HighWindAlert':
                print("Alert: High Wind - Returning to Base!")
                self.state = 'ReturnBase'

            elif self.state == 'ReturnBase':
                print("Returning to launch...")
                await drone.action.return_to_launch()
                break

            await asyncio.sleep(1)


class Logger:
    def __init__(self, filename="logs/mission_log.csv"):
        self.filename = filename
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "state", "ndvi_value", "wind_speed"])

    def log(self, state, ndvi_value, wind_speed):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.datetime.now().isoformat(),
                state,
                round(ndvi_value, 3),
                round(wind_speed, 2)
            ])

# --- Usage Example ---
# In your FSM loop:
# logger = Logger()
# logger.log(current_state, current_ndvi, current_wind_speed)


# --- Main Run ---
if __name__ == "__main__":
    fsm = DroneFSM()
    asyncio.run(fsm.run())
