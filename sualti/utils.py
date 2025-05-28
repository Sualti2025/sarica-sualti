# utils.py

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def send_manual_control(master, x, y, z, r):
    """
    Pixhawk'a manuel kontrol komutu gönderir.

    master : mavutil bağlantı nesnesi
    x : ileri-geri (pozitif ileri)
    y : sağa-sola (pozitif sağ)
    z : derinlik (pozitif yukarı)
    r : yaw (pozitif sağa dönme)
    """
    master.mav.manual_control_send(
        master.target_system,
        int(clamp(x, -1000, 1000)),
        int(clamp(y, -1000, 1000)),
        int(clamp(z, 0, 1000)),  # genelde 0-1000 arası
        int(clamp(r, -1000, 1000)),
        0
    )
