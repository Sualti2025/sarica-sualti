# serit_takip.py
import cv2
import numpy as np

def serit_takip(frame):
    # 1. Görüntüyü gri tonlamaya çevir (siyah şerit için uygundur)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2. Gaussian blur ile görüntüyü yumuşat (gürültü azaltma)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Eşikleme: Siyah şeridi beyaz, arka planı siyah yapar
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)

    # 4. Kontur bulma: Eşiklenmiş görüntüdeki nesneleri bulur
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Görüntüye çizim yapmak için kopyasını al
    output = frame.copy()

    if contours:
        # En büyük konturu bul (genelde şerit olur)
        largest_contour = max(contours, key=cv2.contourArea)

        # Kontur çizimini görüntüye uygula
        cv2.drawContours(output, [largest_contour], -1, (0, 255, 0), 2)

    # İşlenmiş görüntüyü döndür
    return output
