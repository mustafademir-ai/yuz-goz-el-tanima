import cv2

# Modelleri yükle
face_cascade = cv2.CascadeClassifier("face_detector.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
hand_cascade = cv2.CascadeClassifier("haarcascade_hand.xml")  # Ayrı indirilmeli

# Kamerayı başlat
kamera = cv2.VideoCapture(0)

while True:
    ret, kare = kamera.read()
    if not ret:
        break

    gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)

    # Yüz algılama
    yuzler = face_cascade.detectMultiScale(gri, 1.1, 5)

    # El algılama
    eller = hand_cascade.detectMultiScale(gri, 1.8,6)

    # Yüzler için kutu çiz
    for (x, y, w, h) in yuzler:
        cv2.rectangle(kare, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(kare, "YUZ", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Gözleri yüz bölgesi içinde ara
        roi_gray = gri[y:y+h, x:x+w]
        roi_color = kare[y:y+h, x:x+w]
        gozler = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)

        for (ex, ey, ew, eh) in gozler:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 255), 2)
            cv2.putText(roi_color, "GOZ", (ex, ey - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Eller için kutu çiz
    for (x, y, w, h) in eller:
        cv2.rectangle(kare, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(kare, "EL", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Sonuçları göster
    cv2.imshow("Yuz, Goz ve El Algilama", kare)

    # Çıkmak için 'q' tuşuna bas
    if cv2.waitKey(1) == ord('q'):
        break

kamera.release()
cv2.destroyAllWindows()
