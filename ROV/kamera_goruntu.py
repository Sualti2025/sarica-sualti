import cv2

def baslat_kamera(pencere_adi="Kamera Goruntusu"):
    # Jetson'da USB kamera kullanıyorsan 0, CSI kamera ise GStreamer kodu girilmeli
    cap = cv2.VideoCapture(0)  # USB kamera için

    if not cap.isOpened():
        print("[ERROR] Kamera başlatılamadı!")
        return None

    cv2.namedWindow(pencere_adi)
    return cap

def goster_kare(cap, pencere_adi="Kamera Goruntusu"):
    ret, frame = cap.read()
    if not ret:
        print("[WARNING] Kare okunamadı!")
        return False

    cv2.imshow(pencere_adi, frame)
    return True

def kapat_kamera(cap):
    cap.release()
    cv2.destroyAllWindows()
