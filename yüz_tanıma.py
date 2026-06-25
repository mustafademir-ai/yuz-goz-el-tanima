import cv2                          # OpenCV kütüphanesini içe aktar (görüntü işleme için)
import tkinter as tk               # Tkinter GUI kütüphanesi (arayüz oluşturmak için)
from tkinter import filedialog     # Dosya seçme penceresi için
from PIL import Image, ImageTk     # Pillow kütüphanesinden görüntü işleme ve tkinter uyumu için

# FOTOĞRAF SEÇİP YÜZ TESPİTİ YAPAN FONKSİYON
def open_file():
    # Dosya seçme penceresi açılır ve kullanıcıdan dosya yolu alınır
    file_path = filedialog.askopenfilename()
    
    if file_path:  # Eğer bir dosya seçildiyse
        img = cv2.imread(file_path)  # OpenCV ile resmi renkli olarak oku
        
        # Gri tonlamalı versiyonunu oluştur (yüz algılamak için)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Haar Cascade algoritması ile yüzleri tespit et
        # scaleFactor: görüntüyü kaç kere küçülterek arama yapılacak (1.19 iyi bir değer)
        # minNeighbors: bir bölgede kaç tane eşleşme olursa yüz sayılır (5 güvenilir sonuç için)
        # minSize: minimum yüz boyutu (30x30 piksel)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.04, minNeighbors=5, minSize=(30, 30))
        
        # Algılanan tüm yüzler için döngü
        for (x, y, w, h) in faces:
            # Yüz çevresine mavi renkli dikdörtgen çiz (kalınlık 2 piksel)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,255, 0), 2)
            
            # Yüzün altına "YUZ" yazısını mavi renkte ve uygun boyutta yaz
            cv2.putText(img, "YUZ", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # OpenCV'nin BGR formatından RGB formatına çevir (PIL ve Tkinter için gerekli)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Numpy dizisini PIL Image objesine dönüştür
        img = Image.fromarray(img)
        
        # Görüntüyü 600x400 piksele yeniden boyutlandır (LANCZOS kaliteli resize yöntemi)
        img = img.resize((600, 400), Image.LANCZOS)
        
        # PIL Image objesini Tkinter ile uyumlu PhotoImage formatına dönüştür
        img = ImageTk.PhotoImage(img)
        
        # Canvas üzerinde görüntüyü göstermek için referansı sakla (garbage collector önlemek için)
        canvas.img = img
        
        # Canvas'a resmi 0,0 köşesinden yerleştir (sol üst köşe, anchor=tk.NW)
        canvas.create_image(0, 0, anchor=tk.NW, image=img)


# Yüz algılama için önceden eğitilmiş Haar Cascade modelini yükle
face_cascade = cv2.CascadeClassifier('face_detector.xml')

# Ana pencere oluşturuluyor
root = tk.Tk()
root.title("YÜZ TANIMA")  # Pencere başlığı ayarlanıyor

# 600x400 piksel boyutlarında bir Canvas (tuval) oluşturuluyor
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()  # Canvas pencereye ekleniyor ve gösteriliyor

# "dosya seç" adlı bir buton oluşturuluyor, tıklanınca open_file fonksiyonu çağrılır
open_button = tk.Button(root, text="dosya seç", command=open_file)
open_button.pack()  # Buton pencereye ekleniyor ve gösteriliyor

# Tkinter döngüsünü başlat (pencereyi canlı tutar)
root.mainloop()
