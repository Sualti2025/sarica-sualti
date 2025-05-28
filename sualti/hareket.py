from utils import send_manual_control


FORWARD_SCALE = 1500
STRAFE_SCALE = 1000
YAW_RATE_SCALE = 1000
DEPTH_RATE_SCALE = 400
MANUAL_Z_NEUTRAL = 500
MANUAL_Z_MIN = 0
MANUAL_Z_MAX = 1000

def ileri_git(master):
    master.mav.manual_control_send(master.target_system, FORWARD_SCALE, 0, MANUAL_Z_NEUTRAL, 0, 0)
    print("Ileri git")

def geri_git(master):
    master.mav.manual_control_send(master.target_system, -FORWARD_SCALE, 0, MANUAL_Z_NEUTRAL, 0, 0)
    print("Geri git")

def saga_kay(master):
    master.mav.manual_control_send(master.target_system, 0, STRAFE_SCALE, MANUAL_Z_NEUTRAL, 0, 0)
    print("Saga kay")

def sola_kay(master):
    master.mav.manual_control_send(master.target_system, 0, -STRAFE_SCALE, MANUAL_Z_NEUTRAL, 0, 0)
    print("Sola kay")

def yukari_cik(master):
    master.mav.manual_control_send(master.target_system, 0, 0, MANUAL_Z_NEUTRAL + DEPTH_RATE_SCALE, 0, 0)
    print("Yukari cik")

def asagi_in(master):
    master.mav.manual_control_send(master.target_system, 0, 0, MANUAL_Z_NEUTRAL - DEPTH_RATE_SCALE, 0, 0)
    print("Asagi in")

def saga_don(master):
    master.mav.manual_control_send(master.target_system, 0, 0, MANUAL_Z_NEUTRAL, YAW_RATE_SCALE, 0)
    print("Saga don")

def sola_don(master):
    master.mav.manual_control_send(master.target_system, 0, 0, MANUAL_Z_NEUTRAL, -YAW_RATE_SCALE, 0)
    print("Sola don")

def dur(master):
    master.mav.manual_control_send(master.target_system, 0, 0, MANUAL_Z_NEUTRAL, 0, 0)
    print("Dur")

def ileri_saga_kay(master):
    # İleri (X) + Sağa Kay (Y)
    send_manual_control(master, 1500, 1000, MANUAL_Z_NEUTRAL, 0)
    print("İleri ve sağa kay")

def ileri_sola_kay(master):
    # İleri (X) + Sola Kay (Y negatif)
    send_manual_control(master, 1500, -1000, MANUAL_Z_NEUTRAL, 0)
    print("İleri ve sola kay")
