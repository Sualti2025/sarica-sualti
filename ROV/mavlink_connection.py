from pymavlink import mavutil

def connect(connection_string='/dev/ttyACM0', baud_rate=115200):
    print("[INFO] Pixhawk'a bağlanılıyor...")
    master = mavutil.mavlink_connection(connection_string, baud=baud_rate)
    master.wait_heartbeat()
    print("[INFO] Bağlantı başarılı.")
    return master

def set_mode(master, mode_name):
    # if master is None: return False
    mode_id = master.mode_mapping().get(mode_name)
    if mode_id is None:
        print(f"Mod {mode_name} bulunamadı!")
        return False
    master.set_mode(mode_id)
    return True

def arm_vehicle(master):
    master.arducopter_arm()
    master.motors_armed_wait()
    print("Araç arm edildi.")

def disarm_vehicle(master):
    master.arducopter_disarm()
    master.motors_disarmed_wait()
    print("Araç disarm edildi.")
