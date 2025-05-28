# -*- coding: utf-8 -*-
from pymavlink import mavutil
import time
import math
from hareket import ileri_git, geri_git, saga_kay, sola_kay, yukari_cik, asagi_in, saga_don, sola_don, dur, ileri_saga_kay, ileri_sola_kay

connection_string = '/dev/ttyACM0'
baud_rate = 115200
TARGET_MODE = 'GUIDED'

master = None

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

# --- Ana Program ---
if __name__ == '__main__':
    print("[INFO] Pixhawk'a bağlanılıyor...")
    master = mavutil.mavlink_connection(connection_string, baud=baud_rate)
    master.wait_heartbeat()
    print("[INFO] Bağlantı başarılı.")

    set_mode(TARGET_MODE)
    arm_vehicle()
    time.sleep(2)
    request_imu_data()

    try:
        print("[INFO] Görev başlıyor. IMU verileri 'imu_log.txt' dosyasına kaydedilecek.")
        
        with open("imu_log.txt", "w") as log_file:
            while True:
                get_attitude(log_file)

                dur(master)
                time.sleep(2)

                ileri_git(master)
                time.sleep(2)

                ileri_git(master)
                time.sleep(2)


                ileri_sola_kay(master)
                time.sleep(2)

                ileri_sola_kay(master)
                time.sleep(2)

                dur(master)
                time.sleep(1)

                break  # Test sonrası durması için

    except KeyboardInterrupt:
        print("\n[INFO] Kullanıcı tarafından durduruldu.")

    finally:
        dur(master)
        disarm_vehicle()
        master.close()
        print("[INFO] Program sonlandı.")
