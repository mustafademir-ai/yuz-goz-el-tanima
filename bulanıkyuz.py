import cv2

# Modelleri yükleyelim
yuzxml = cv2.CascadeClassifier("face_detector.xml")
gozxml = cv2.CascadeClassifier("haarcascade_eye.xml")
elxml = cv2.CascadeClassifier("haarcascade_hand.xml")

# Kamerayı başlat
kamera = cv2.VideoCapture(0)

while True:
    donen, kare = kamera.read()
    if not donen:
        break

    gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)

    yuzler = yuzxml.detectMultiScale(gri, 1.1, 5)
    eller = elxml.detectMultiScale(gri, 1.8, 6)

    for (x, y, w, h) in yuzler:
        # Yüzü bulanıklaştır
        yuz_bolgesi = kare[y:y+h, x:x+w]
        bulanik_yuz = cv2.GaussianBlur(yuz_bolgesi, (99, 99), 30)  # (kernel_size, sigma)
        kare[y:y+h, x:x+w] = bulanik_yuz

        # (İsteğe bağlı) bulanık yüzün etrafına yeşil bir çerçeve çiz ve 'YUZ' yaz
        cv2.rectangle(kare, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(kare, "YUZ", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Yüz bölgesi içinde gözleri ara
        gri_goz = gri[y:y+h, x:x+w]
        renkli_goz = kare[y:y+h, x:x+w]
        gozler = gozxml.detectMultiScale(gri_goz, 1.1, 5)

        for (ex, ey, ew, eh) in gozler:
            cv2.rectangle(renkli_goz, (ex, ey), (ex + ew, ey + eh), (0, 255, 255), 2)
            cv2.putText(renkli_goz, "GOZ", (ex, ey - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    for (x, y, w, h) in eller:
        cv2.rectangle(kare, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(kare, "EL", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow("Yuz, Goz ve El Algilama", kare)

    if cv2.waitKey(1) == ord('q'):
        break

kamera.release()
cv2.destroyAllWindows()
