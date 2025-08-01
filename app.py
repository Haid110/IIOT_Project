from flask import Flask, render_template, Response, jsonify
import threading
import time
import random

app = Flask(__name__)

# Shared state for demo
mission_state = {"state": "Surveying", "ndvi_value": 0.45}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/state')
def get_state():
    return jsonify(mission_state)

# Example background thread to simulate NDVI updates
def update_state():
    while True:
        mission_state["ndvi_value"] = round(random.uniform(0.2, 0.8), 2)
        mission_state["state"] = random.choice(["Surveying", "Analyzing", "AnomalyAlert", "HighWindAlert"])
        time.sleep(5)

if __name__ == '__main__':
    t = threading.Thread(target=update_state)
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', port=5000)
