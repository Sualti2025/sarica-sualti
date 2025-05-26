from pymavlink import mavutil
import time
import math

# --- MAVLink Bağlantı ---
connection_string = '/dev/ttyACM0'
baud_rate = 115200

FORWARD_SCALE = 1500
STRAFE_SCALE = 1000
YAW_RATE_SCALE = 1000
DEPTH_RATE_SCALE = 400
MANUAL_Z_NEUTRAL = 500
MANUAL_Z_MIN = 0
MANUAL_Z_MAX = 1000
TARGET_MODE = 'GUIDED'
COMMAND_RATE_HZ = 20

master = None

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def set_mode(mode_name):
    if master is None: return False
    mode_id = master.mode_mapping().get(mode_name)
    if mode_id is None:
        print(f"Mod {mode_name} bulunamadı!")
        return False
    master.set_mode(mode_id)
    return True

def arm_vehicle():
    master.arducopter_arm()
    master.motors_armed_wait()
    print("Araç arm edildi.")

def disarm_vehicle():
    master.arducopter_disarm()
    master.motors_disarmed_wait()
    print("Araç disarm edildi.")

def send_manual_control(x, y, z, r):
    master.mav.manual_control_send(
        master.target_system,
        int(clamp(x, -1000, 1000)),
        int(clamp(y, -1000, 1000)),
        int(clamp(z, MANUAL_Z_MIN, MANUAL_Z_MAX)),
        int(clamp(r, -1000, 1000)),
        0)

# --- IMU Verisi İsteği ve Kaydetme ---
def request_imu_data():
    master.mav.request_data_stream_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_EXTRA1,  # ATTITUDE mesajı
        10,
        1
    )

def get_attitude(log_file):
    msg = master.recv_match(type='ATTITUDE', blocking=False)
    if msg:
        roll = math.degrees(msg.roll)
        pitch = math.degrees(msg.pitch)
        yaw = math.degrees(msg.yaw)
        rollspeed = math.degrees(msg.rollspeed)
        pitchspeed = math.degrees(msg.pitchspeed)
        yawspeed = math.degrees(msg.yawspeed)

        log_line = f"{time.time():.2f}, Roll: {roll:.1f}, Pitch: {pitch:.1f}, Yaw: {yaw:.1f}, RollRate: {rollspeed:.1f}, PitchRate: {pitchspeed:.1f}, YawRate: {yawspeed:.1f}"
        
        print("[IMU]", log_line)
        log_file.write(log_line + "\n")
        log_file.flush()

# --- Komut Fonksiyonları ---
def ileri_git():
    send_manual_control(FORWARD_SCALE, 0, MANUAL_Z_NEUTRAL, 0)
    print("İleri git")

def geri_git():
    send_manual_control(-FORWARD_SCALE, 0, MANUAL_Z_NEUTRAL, 0)
    print("Geri git")

def saga_don():
    send_manual_control(0, 0, MANUAL_Z_NEUTRAL, YAW_RATE_SCALE)
    print("Sağa dön")

def sola_don():
    send_manual_control(0, 0, MANUAL_Z_NEUTRAL, -YAW_RATE_SCALE)
    print("Sola dön")

def saga_kay():
    send_manual_control(0, STRAFE_SCALE, MANUAL_Z_NEUTRAL, 0)
    print("Sağa kay")

def sola_kay():
    send_manual_control(0, -STRAFE_SCALE, MANUAL_Z_NEUTRAL, 0)
    print("Sola kay")

def yukari_cik():
    send_manual_control(0, 0, MANUAL_Z_NEUTRAL + DEPTH_RATE_SCALE, 0)
    print("Yukarı çık")

def asagi_in():
    send_manual_control(0, 0, MANUAL_Z_NEUTRAL - DEPTH_RATE_SCALE, 0)
    print("Aşağı in")

def dur():
    send_manual_control(0, 0, MANUAL_Z_NEUTRAL, 0)
    print("Dur")

# --- Ana Program ---
if __name__ == '__main__':
    print("[INFO] Pixhawk'a bağlanılıyor...")
    master = mavutil.mavlink_connection(connection_string, baud=baud_rate)
    master.wait_heartbeat()
    print("[INFO] Bağlantı başarılı.")

    set_mode(TARGET_MODE)
    arm_vehicle()
    request_imu_data()

    try:
        print("[INFO] Görev başlıyor. IMU verileri 'imu_log.txt' dosyasına kaydedilecek.")
        
        with open("imu_log.txt", "w") as log_file:
            while True:
                get_attitude(log_file)

                # dur()
                # time.sleep(2)
                
                # dur()
                # time.sleep(2)

                # saga_kay()
                # time.sleep(2)

                # sola_kay()
                # time.sleep(2)
                # break

    except KeyboardInterrupt:
        print("\n[INFO] Kullanıcı tarafından durduruldu.")

    finally:
        dur()
        disarm_vehicle()
        master.close()
        print("[INFO] Program sonlandı.")
