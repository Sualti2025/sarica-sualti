import time
from constants import TARGET_MODE
from mavlink_connection import connect, set_mode, arm_vehicle, disarm_vehicle
from hareket_fonksiyonu import ileri_git, geri_git, saga_don, sola_don, saga_kay, sola_kay, yukari_cik, asagi_in, dur
from imu_kontrol import request_imu_data, get_attitude
from kamera_goruntu import baslat_kamera, goster_kare, kapat_kamera
from serit_takip import serit_takip
import cv2

if __name__ == '__main__':
    master = connect()
    set_mode(master, TARGET_MODE)
    arm_vehicle(master)
    request_imu_data(master)

    cap = baslat_kamera()
    if cap is None:
        exit()

    print("[INFO] Görev başlıyor. IMU verileri 'imu_log.txt' dosyasına kaydedilecek.")
    try:
        with open("imu_log.txt", "w") as log_file:
            while True:
                get_attitude(master, log_file)

                ret, frame = cap.read()
                if not ret:
                    break
                
                # Şerit takibi uygula
                islenmis = serit_takip(frame)

                # İşlenmiş görüntüyü göster
                cv2.imshow("Serit Takibi", islenmis)

                saga_kay(master, 2)

                sola_kay(master, 2)

                dur(master, 1)

                if cv2.waitKey(1) & 0xFF == 27:  # ESC tuşuna basılırsa çık
                    break

    except KeyboardInterrupt:
        print("\n[INFO] Kullanıcı tarafından durduruldu.")
    finally:
        dur(master)
        disarm_vehicle(master)
        master.close()
        kapat_kamera(cap)
        print("[INFO] Program sonlandı.")
