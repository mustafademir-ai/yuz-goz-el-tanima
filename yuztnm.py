import cv2

# Yüz tanıma modeli (Haar Cascade) yükleniyor
yuz_modeli = cv2.CascadeClassifier("face_detector.xml")

# Kamera başlatılıyor
kamera = cv2.VideoCapture(0)

while True:
    # Kameradan görüntü al
    ret, kare = kamera.read()
    if not ret:
        break

    # Griye çevir
    gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)

    # Yüzleri bul
    yuzler = yuz_modeli.detectMultiScale(gri, 1.1, 4)

    # Yüzleri çiz
    for (x, y, w, h) in yuzler:
        cv2.rectangle(kare, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(kare, "YUZ", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Görüntüyü göster
    cv2.imshow("Yüz Tanıma", kare)

    # 'q' ile çık
    if cv2.waitKey(1) == ord("q"):
        break

# Kapat
kamera.release()
cv2.destroyAllWindows()
