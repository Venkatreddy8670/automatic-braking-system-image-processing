
import cv2
import numpy as np
import time
import RPi.GPIO as GPIO
import busio
import board
import adafruit_adxl34x
from picamera2 import Picamera2

# GPIO Setup
LED_PIN = 18
BUZZER_PIN = 25
LDR1_PIN = 23  # Left LDR
LDR2_PIN = 24  # Right LDR

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)
GPIO.output(BUZZER_PIN, GPIO.LOW)
GPIO.setup(LDR1_PIN, GPIO.IN)
GPIO.setup(LDR2_PIN, GPIO.IN)

# I2C Setup for ADXL345
i2c = busio.I2C(board.SCL, board.SDA)
accel = adafruit_adxl34x.ADXL345(i2c)

def get_direction():
    x, y, z = accel.acceleration
    if x > 3.0:
        return "Right"
    elif x < -3.0:
        return "Left"
    else:
        return "Straight"

def detect_signal_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    roi_h = int(height / 2)
    roi_w_start = int(width / 3)
    roi_w_end = int(2 * width / 3)
    roi = hsv[0:roi_h, roi_w_start:roi_w_end]
    roi_bgr = frame[0:roi_h, roi_w_start:roi_w_end]

    lower_red1 = np.array([0, 120, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 120, 100])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(roi, lower_red1, upper_red1)
    mask2 = cv2.inRange(roi, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 100:
            continue
        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * (area / (perimeter * perimeter))
        if 0.5 < circularity <= 1.3:
            cv2.drawContours(roi_bgr, [cnt], -1, (0, 255, 0), 2)
            return "Red"
    return "No light"

def led_buzzer_control(should_led_on, led_state):
    if should_led_on and not led_state:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        GPIO.output(LED_PIN, GPIO.HIGH)
        return True
    elif not should_led_on:
        GPIO.output(LED_PIN, GPIO.LOW)
        return False
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)
        return True

def main():
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    ))
    picam2.start()
    led_state = False
    try:
        while True:
            frame = picam2.capture_array()
            signal = detect_signal_color(frame)
            direction = get_direction()
            ldr1 = GPIO.input(LDR1_PIN)
            ldr2 = GPIO.input(LDR2_PIN)
            should_led_on = False

            if (signal == "Red" and direction == "Straight" and ldr1 == 1 and ldr2 == 1) or                (signal == "No light" and direction == "Right" and ldr1 == 0 and ldr2 == 1) or                (signal == "No light" and direction == "Left" and ldr1 == 1 and ldr2 == 0) or                (signal == "Red" and direction == "Right" and ldr1 == 0 and ldr2 == 1) or                (signal == "Red" and direction == "Left" and ldr1 == 1 and ldr2 == 0):
                should_led_on = True

            led_state = led_buzzer_control(should_led_on, led_state)

            label = f"Signal: {signal} | Turn: {direction} | LDR1: {ldr1} | LDR2: {ldr2} | LED: {'ON' if led_state else 'OFF'}"
            cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            height, width, _ = frame.shape
            cv2.rectangle(frame, (int(width / 3), 0), (int(2 * width / 3), int(height / 2)), (255, 0, 0), 2)
            cv2.imshow("Traffic Light Detection", frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    finally:
        picam2.stop()
        cv2.destroyAllWindows()
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        GPIO.cleanup()

if __name__ == "__main__":
    main()
