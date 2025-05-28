import math
import time
from pymavlink import mavutil

def request_imu_data(master):
    master.mav.request_data_stream_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_EXTRA1,
        10,
        1
    )

def get_attitude(master, log_file):
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
