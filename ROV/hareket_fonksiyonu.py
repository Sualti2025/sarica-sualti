import time
from constants import *

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def send_manual_control(master, x, y, z, r):
    master.mav.manual_control_send(
        master.target_system,
        int(clamp(x, -1000, 1000)),
        int(clamp(y, -1000, 1000)),
        int(clamp(z, MANUAL_Z_MIN, MANUAL_Z_MAX)),
        int(clamp(r, -1000, 1000)),
        0
    )

def hareket_et(master, x, y, z, r, sure=0):
    baslangic = time.time()
    while time.time() - baslangic < sure:
        send_manual_control(master, x, y, z, r)
        time.sleep(1 / COMMAND_RATE_HZ)  # 20 Hz komut gönderme

def ileri_git(master, sure=0):
    hareket_et(master, FORWARD_SCALE, 0, MANUAL_Z_NEUTRAL, 0, sure)

def geri_git(master, sure=0):
    hareket_et(master, -FORWARD_SCALE, 0, MANUAL_Z_NEUTRAL, 0, sure)

def saga_don(master, sure=0):
    hareket_et(master, 0, 0, MANUAL_Z_NEUTRAL, YAW_RATE_SCALE, sure)

def sola_don(master, sure=0):
    hareket_et(master, 0, 0, MANUAL_Z_NEUTRAL, -YAW_RATE_SCALE, sure)

def saga_kay(master, sure=0):
    hareket_et(master, 0, STRAFE_SCALE, MANUAL_Z_NEUTRAL, 0, sure)

def sola_kay(master, sure=0):
    hareket_et(master, 0, -STRAFE_SCALE, MANUAL_Z_NEUTRAL, 0, sure)

def yukari_cik(master, sure=0):
    hareket_et(master, 0, 0, MANUAL_Z_NEUTRAL + DEPTH_RATE_SCALE, 0, sure)

def asagi_in(master, sure=0):
    hareket_et(master, 0, 0, MANUAL_Z_NEUTRAL - DEPTH_RATE_SCALE, 0, sure)
    
def dur(master, sure=0):
    hareket_et(master, 0, 0, MANUAL_Z_NEUTRAL, 0, sure)
