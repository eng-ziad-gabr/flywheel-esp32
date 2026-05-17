# ⚙️ FLYWHEEL — Wireless Energy Storage Control System

> A hand-built flywheel energy storage prototype controlled wirelessly from any smartphone browser via ESP32 Wi-Fi.

![Control Panel](https://img.shields.io/badge/UI-Browser%20Based-00d4ff?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-ESP32%20%2F%20Pico%20W-blue?style=flat-square)
![Language](https://img.shields.io/badge/Language-MicroPython-yellow?style=flat-square)
![Driver](https://img.shields.io/badge/Driver-L298N-red?style=flat-square)

---

## 🎯 What is this?

A flywheel spins at high speed and stores **kinetic energy** (E = ½·I·ω²).  
A second DC motor on the opposite shaft acts as a **generator**, converting that energy back to electricity to light LEDs.

The entire system is controlled wirelessly through a **browser-based control panel** served directly from the ESP32 — no app, no cloud, no internet required.

---

## 🛠️ Hardware

| Component | Details |
|-----------|---------|
| Microcontroller | ESP32 / Raspberry Pi Pico W |
| Motor Driver | L298N Dual H-Bridge |
| Motor (Drive side) | DC motor — controls flywheel spin |
| Motor (Generator side) | DC motor — harvests kinetic energy |
| Power Supply | 6× Li-ion batteries in series (~22V) |
| Frame | Hand-built pine wood + MDF base |
| Flywheel discs | Solid pine, ~25cm diameter |

### Pin Wiring

```
ENA → GPIO 14   (PWM, 1000 Hz)
IN1 → GPIO 26   (Direction bit 1)
IN2 → GPIO 27   (Direction bit 2)

FORWARD : IN1=HIGH, IN2=LOW
REVERSE : IN1=LOW,  IN2=HIGH
STOP    : ENA duty = 0
```

---

## 💻 Software

### File Structure

```
/
├── main.py       # MicroPython HTTP server + motor control logic
└── index.html    # Animated web control panel (served from flash)
```

### Wi-Fi Access Point

```
SSID     : FlywheelControl
Password : flywheel123
IP       : 192.168.4.1
Port     : 80 (HTTP)
```

Connect your phone to **FlywheelControl**, then open `http://192.168.4.1` in your browser.

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serves the HTML control panel |
| POST | `/power` | Toggle motor ON/OFF → returns `1` or `0` |
| POST | `/speed?v=N` | Set PWM speed (0–255) → returns `ok` |
| POST | `/direction` | Toggle FWD/REV → returns `1` or `0` |

---

## 🌐 Control Panel Features

- **Animated SVG flywheel** — spins faster/slower and reverses direction in sync with the real motor
- **Power button** — glowing ON/OFF toggle
- **Speed slider** — PWM 0 to 255 with live display
- **Direction button** — FORWARD / REVERSE
- **Status panel** — motor state, direction, and current PWM value
- Dark theme, mobile-optimized, zero dependencies

---

## ⚡ Energy Flow

```
Battery Pack
    ↓
L298N Motor Driver
    ↓
Drive Motor → Flywheel (stores E = ½·I·ω²)
                  ↓
           Generator Motor
                  ↓
               LEDs 💡
```

---

## 🚀 Flash & Run

1. Flash MicroPython firmware to your ESP32
2. Upload both files using **Thonny** or **mpremote**:
   ```bash
   mpremote cp main.py :main.py
   mpremote cp index.html :index.html
   ```
3. Reset the board — it boots as a Wi-Fi AP automatically
4. Connect your phone to **FlywheelControl** and open `192.168.4.1`

---

## 🔭 Future Improvements

- [ ] RPM sensor (Hall effect) for closed-loop PID speed control
- [ ] INA219 voltage/current sensor to display live generator wattage
- [ ] WebSocket for real-time bidirectional data streaming
- [ ] Capacitor bank to smooth generator output
- [ ] Steel flywheel disc for higher energy density

---

## 📄 License

MIT License — feel free to build on it.
