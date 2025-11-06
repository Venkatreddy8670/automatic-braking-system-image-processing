# 🚗 Automatic Braking System Using Image Processing

This project demonstrates an **Automatic Braking System** using **Image Processing** on a **Raspberry Pi 4**. 
The system integrates computer vision, sensor inputs, and real-time decision-making to automatically simulate braking using an LED and buzzer.

---

## 🧠 Project Overview

The system detects **red traffic lights** through image processing, reads **directional data** from an **ADXL345 accelerometer**, 
and uses **LDR sensors** to simulate vehicle indicator conditions. Based on these inputs, it triggers a braking action represented by an LED and buzzer.

---

## ⚙️ Features

- Real-time **traffic light detection** using OpenCV
- **Accelerometer-based** direction sensing (Left, Right, Straight)
- Dual **LDR sensor inputs** for turn detection
- **LED & Buzzer simulation** for safe braking demonstration
- Integrated using **Raspberry Pi 4B** and **Python**

---

## 🧰 Hardware Requirements

- Raspberry Pi 4 Model B  
- Pi Camera Module 3 NoIR Wide  
- ADXL345 Accelerometer (I2C interface)  
- HW072 LDR Sensors (x2)  
- Buzzer  
- LED (for brake simulation)

---

## 💻 Software Requirements

- Python 3.x  
- OpenCV  
- NumPy  
- Picamera2  
- RPi.GPIO  
- Adafruit ADXL34x Library

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## 🧩 Circuit Connections

| Component | Pin | Raspberry Pi GPIO |
|------------|-----|-------------------|
| LED        | Data | GPIO 18 |
| Buzzer     | Data | GPIO 25 |
| LDR1 (Left)| Data | GPIO 23 |
| LDR2 (Right)| Data | GPIO 24 |
| ADXL345    | SDA/SCL | GPIO 2 / GPIO 3 |
| Pi Camera  | Ribbon Cable | CSI Port |

---

## ▶️ Run the Program

```bash
python3 main.py
```

Press **'q'** to stop the video window safely.

---

## 📊 Working Logic

1. **Traffic Light Detection** – Uses color filtering in HSV to identify red signals.  
2. **Direction Detection** – Accelerometer determines Left / Right / Straight orientation.  
3. **Decision Logic** – Combines sensor data to decide when to apply brakes.  
4. **Braking Simulation** – LED turns ON and buzzer sounds for 5 seconds before LED lights up.

---

## 🖼️ Output Example

- Real-time video feed with status overlay:  
  `Signal: Red | Turn: Straight | LDR1: 1 | LDR2: 1 | LED: ON`

---

## 📁 Folder Structure

```
automatic-braking-system-image-processing/
│
├── main.py
├── requirements.txt
├── README.md
└── report.docx
```

---

## 👩‍💻 Author

**VENKATREDDY**  
Department of ECE  
[AMC Engineering College]  

---

## 🪄 License

This project is for educational and research purposes only.  
Feel free to use and modify it with proper credit.
