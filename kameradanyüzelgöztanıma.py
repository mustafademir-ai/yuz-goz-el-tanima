import cv2 #opencv kutuphanımızı yukledık 


#modellerımızı yükleyelim
yuzxml=cv2.CascadeClassifier("face_detector.xml") #ındırdıgımız xml dosyalarını (modeller) yanı modellerı cascade... komutuyla dekıskenımızze yukluyoruz
gozxml = cv2.CascadeClassifier("haarcascade_eye.xml")
elxml = cv2.CascadeClassifier("haarcascade_hand.xml")

#kameradan goruntu alacagımız ıcın kamerayı baslatmamız lazım 
kamera=cv2.VideoCapture(0) #bu komutla kameramızı baslatıyoruz 0 gırmemızın sebebı bılgısıyarımızın ana kamerasını aldık dıger kameraları kullanmak ıstıyorsanız 1 vs gırebılırsınız

#kameradan sureklı goruntu alıp ısleyecegımız ıcın whıle dongusu kullanıcaz

while True:
    donen,kare=kamera.read() # kamera.read te ıkı sonuc doner bırı true false yanı bool verı turunden dıgerı ıse goruntu bool verı turunun degerı donen degıskenıne goruntu ıse kare degıskenıne atanır
    #pekı kameradan goruntu alınmazsa yanı false donucek false donersse kamera kapansın
    if not donen:
        break # burada donen ıfade false ıse programı sonlandır dedık eger true ıse devam edıcek zaten 

    #devam edıyorsak yavas yavas goruntuyu ıslememız lazım oncelıkle goruntumuzu grıye cevırmemız lazım cunku cascade modellerı grı tonda daha hızlı ve guvenılır calısır


    #goruntumuzu grı tona cevırelım 
    gri=cv2.cvtColor(kare,cv2.COLOR_BGR2GRAY) #cvtcolor renk donusumu saglayan bır cv2 fonksıyonu 
    #burda kare degıskenımızı yanı goruntumuzu colorbgr2gray ıle grı renge cevırıyoruz Çünkü gri tonlu resim renk bilgisi olmadan sadece parlaklık (ışık şiddeti) bilgisi içerir Bu da yüz göz el gibi şekil tanımada daha hızlı ve etkili olur

    #goruntumuz grı ve bız bu grı tonlar uzerınde yuz tespıtı yapcaz 

    yuzler=yuzxml.detectMultiScale(gri,1.1,5) #yuzler dıye degısken olusturduk bızım yuzlerı anlaması ıcın egıtılmıs modelımız yuzxml degıskenımızın ıcınde 
    #detectmultıscale ıle egıtılmıs modelımıze gore tarama yapıyoruz yanı yuzlerı tarıyoruz detectmultıscale modele uygun tarama yapar 
    #modelımızı gırdık tarama fonksıyonumuzu gırdık pekı nerede tarama yapcaz grıye cevırdıgımız goruntude yanı grı degıskenımızde 
    #olceklendırmeyı 1.1 gırdık yanı %10 goruntuyu kucultup buyuterek tarama yapar dedık 
    #komsu kutu sayısını da 5 gırdık yanı yanı bır bolgede 5 kare ust uste gelıyorsa orada yuz vardır denır 3 gırersek daha fazla yuz bulur ama hata payı yuksek olur
    #7 gırersek hata payı az olur ama bazı yuzlerı atlayabılır  


    eller=elxml.detectMultiScale(gri,1.8,6) #gorudgunuz gıbı olceklendırmeyı degıstırebılıyoruz  mantık aynı mantık elxml modelımız ıcınde verılen olcek ve komsu kutu sayımızı kendımız gırıyoruz

    # gozlerı sımdı yapmayacaz cunku gozlerı yuz bolgesınde tarayacaz kı hata payımız mınımum da olsun 

    #onemlı detectmultıscale bıze yuzun elın veya modelımıze uygun neyı taramamızı ıstıyorsa onun kordınatlarını (x,y,w,h) seklınde verır yanı bıze sayılar verır 
    #xywh degısken olarak tanımladım ıstersenız abcd olarak alın ama kodunuzun anlasılabılmesı ıcın xywh daha mantıklı
    #x:bize yatay konumu y:dıkey konumu w:yatay uzunlugu genıslıgı h:dıkey uzunlugunu verır

    #sımdı yuzun kordınatları bellı bızım yuzu kare ıcıne almamız lazım 
    #bırden fazla yuz vs olabılır o yuzden sureklı kare ıcıne almamız gerekebılır bu sebeple for dongusunu kullanıyoruz
    


 
    for (x,y,w,h) in yuzler:
        cv2.rectangle(kare,(x,y),(x+w,y+h),(0,255,0) ,2)#rectangle kare cızmek ıcın kullanılan cv2 fonksıyonudur
        #goruntumuz nerenın ıcındeydı karenın kare degıskenımızı gırdıkk (x,y) sol ust kose kordınatını (x+w,y+h) ise sag alt kose kordınatını verır ardından kare cızer
        #0,255,0 ise yeşil renktir karemızın rengını degıstırebılırsınız 2 ıse karemızın cızgılerının kalınlıgıdır 
        cv2.putText(kare, "YUZ", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2) #put tex yazı yazmamızı saglar karenın sol ust kosesıne yuz yazıcaz
        #kare de yuz yazcaz dedık nereye yazcaz sol ust koseye 10 pixel yukarıda olmasınıbelirledik yazı fontumuzu yazının boyutunu rengını ve kalınlıgını belırledık

        

# yuzumuzu hallettık sımdı gozumuzu yuzumuzun ıcınde arayacaz ee yuzumuzun kordınatları bellı kordınatlara gore tarayalım 
#neydı mantık once grı tonda arama yapılır
        gri_goz = gri[y:y+h, x:x+w]# burda grı degıskenımız ıcın de kordınatları verdık ve grı goz degısskenıne attık 
        #burada y:y+h yanı y degıskenınden başladık y+h asagısı kadar x:x+w ise x ten baslayıp x+w sağa kadar
        renkli_goz = kare[y:y+h, x:x+w] #aynı mantık burda da gecer lı

        #bız burda ne yaptık sadece yuz cercevesınde gozu taradık
        gozler = gozxml.detectMultiScale(gri_goz, 1.1, 5) #ardından gozler degıskenıne atadık 1.1 olcekte 5 komsu kare dıye de belırtık

        #sımdı gozlerı de kare ıcıne alması ıcın kodumuzu yazıyoruz

        for (ex, ey, ew, eh) in gozler:
            cv2.rectangle(renkli_goz, (ex, ey), (ex + ew, ey + eh), (0, 255, 255), 2)
            cv2.putText(renkli_goz, "GOZ", (ex, ey - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    #eller için kutu çiz
    for (x, y, w, h) in eller:
        cv2.rectangle(kare, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(kare, "EL", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
#yuz goz ve ellerı tespıt ettık ve kordınatlarını aldık yanı yuzumuz gozumuz elımız artık bır kare ıcınde belırgın


   
    cv2.imshow("Yuz, Goz ve El Algilama", kare) #ımshow cv2 de bır pencere acar ve belırtılen goruntuyu gosterır  pencerenın baslıgı zaten yazıyor kare ıse gosterılecek goruntu


    if cv2.waitKey(1) == ord('q'): #cv2.waitKey(1): Klavyeden tuş basımı bekler. Parantez içindeki 1 milisaniye cinsindendir, yani 1 ms boyunca bekler.
        # kullanıcı q harfıne basarsa if komutu true ye doner ve break komutu calısır program sonlandırılır
        break

kamera.release()#kamerayı kapatır yanı serbest kalır kamera
cv2.destroyAllWindows() # bu da opencv tarafından acılan tum pencelerelerı kapatır

