import network, socket
from machine import Pin, PWM

# ── Motor ──────────────────────────────
ENA = PWM(Pin(14), freq=1000)
IN1 = Pin(26, Pin.OUT)
IN2 = Pin(27, Pin.OUT)
ENA.duty_u16(0); IN1.off(); IN2.off()

motor_on = False
dir_fwd  = True
speed    = 150

def apply():
    if not motor_on:
        ENA.duty_u16(0); IN1.off(); IN2.off()
    else:
        IN1.value(dir_fwd); IN2.value(not dir_fwd)
        ENA.duty_u16(speed * 257)
    print("Motor:", "ON" if motor_on else "OFF",
          "|", "FWD" if dir_fwd else "REV",
          "| PWM:", speed)

# ── WiFi AP ────────────────────────────
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='FlywheelControl', password='flywheel123')
ap.ifconfig(('192.168.4.1','255.255.255.0','192.168.4.1','8.8.8.8'))
print("IP:", ap.ifconfig()[0])

# ── HTML من ملف منفصل ──────────────────
with open('index.html', 'rb') as f:
    HTML = f.read()
print("HTML loaded:", len(HTML), "bytes")

# ── HTTP ───────────────────────────────
def param(req, key):
    k = key + b'='
    i = req.find(k)
    if i < 0: return None
    s = i + len(k)
    e = s
    while e < len(req) and req[e:e+1] not in (b' ',b'&',b'\r',b'\n'):
        e += 1
    return req[s:e].decode()

def respond(conn, body, ctype=b'text/plain'):
    conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Type: ' + ctype + b'\r\nConnection: close\r\n\r\n')
    conn.sendall(body if isinstance(body, (bytes, bytearray)) else body.encode())

def handle(conn):
    global motor_on, dir_fwd, speed
    try:
        conn.settimeout(3.0)
        req = conn.recv(512)
        if not req: return
        if   b'POST /power'     in req:
            motor_on = not motor_on; apply()
            respond(conn, b'1' if motor_on else b'0')
        elif b'POST /speed'     in req:
            v = param(req, b'v')
            if v: speed = max(0, min(255, int(v)))
            if motor_on: apply()
            respond(conn, b'ok')
        elif b'POST /direction' in req:
            dir_fwd = not dir_fwd
            if motor_on: apply()
            respond(conn, b'1' if dir_fwd else b'0')
        else:
            conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n')
            for i in range(0, len(HTML), 512):
                conn.sendall(HTML[i:i+512])
    except Exception as e:
        print("ERR:", e)
    finally:
        conn.close()

# ── Server ─────────────────────────────
srv = socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(('0.0.0.0', 80))
srv.listen(3)
print("Ready: http://192.168.4.1")

while True:
    try:
        conn, _ = srv.accept()
        handle(conn)
    except OSError:
        pass
