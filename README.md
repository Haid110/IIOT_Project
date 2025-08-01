# Project 4: Field-Edge Crop Surveyor (Simulation Prototype)

## 📌 Overview
This project simulates a UAV-based crop health survey system using PX4 SITL, QGroundControl, and MAVSDK-Python. The mission includes NDVI analysis, state-based fault handling, and live telemetry streaming via a dashboard.

---

## 🚀 Features
- FSM-driven mission logic using MAVSDK-Python
- NDVI calculation on RGB + NIR image frames (simulated)
- Simulated high wind and NDVI stress alerts
- PX4 SITL integration
- QGroundControl for live mission tracking
- Flask + Leaflet.js dashboard for real-time status
- CSV logging of mission state and telemetry

---

## 🛠️ Requirements
- Python 3.8+
- PX4 SITL (via PX4-Autopilot)
- QGroundControl
- MAVSDK-Python
- Flask
- OpenCV

Install Python dependencies:
```bash
pip install -r requirements.txt
```

---

## 🧩 Project Structure
```
project4_field_edge/
├── mavsdk_fsm.py           # Main mission control FSM
├── dashboard/
│   ├── app.py              # Flask server
│   └── templates/
│       └── index.html      # Leaflet dashboard
├── logs/                   # NDVI + wind CSV logs
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── docs/                   # Screenshots, diagrams (optional)
```

---

## ✅ How to Run (Simulation)

### 1. Start PX4 SITL
```bash
cd PX4-Autopilot
make px4_sitl_default
```

### 2. Open QGroundControl
- QGC auto-connects via UDP 14550

### 3. Run FSM Mission Script
```bash
python mavsdk_fsm.py
```

### 4. Launch Dashboard (optional)
```bash
cd dashboard
python app.py
```
Then visit: [http://localhost:5000](http://localhost:5000)

---

## 📊 Output
- **Live map** with NDVI values and state via dashboard
- **CSV log** with timestamp, state, NDVI, and wind data
- **Console logs** showing mission logic

---

## 🔄 Next Steps
- Integrate real RGB + NIR camera (hardware phase)
- Use real telemetry for wind input
- Extend dashboard to show NDVI heatmaps
- Deploy FSM to Jetson companion board
