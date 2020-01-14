import cv2
import numpy as np
import os

Kamera = cv2.VideoCapture(0)
kernel = np.ones((25, 15), np.uint8)
# (15,15) dir tam ,

def ResimFarkBul(Resim1,Resim2):
    Resim2 =cv2.resize(Resim2,(Resim1.shape[1],Resim1.shape[0]))
    Fark_Resim = cv2.absdiff(Resim1,Resim2)
    Fark_Sayi= cv2.countNonZero(Fark_Resim)
    return Fark_Sayi


def VeriYukle():
    Veri_Isimler = []
    Veri_Resimler= []

    Dosyalar= os.listdir("veri/")
    for Dosya in Dosyalar:
        Veri_Isimler.append(Dosya.replace(".jpg",""))
        Veri_Resimler.append(cv2.imread("veri/"+Dosya,0))
    return Veri_Isimler,Veri_Resimler

def Siniflandir(Resim,Veri_Isimler,Veri_Resimler):
    Min_Index= 0
    Min_Deger= ResimFarkBul(Resim,Veri_Resimler[0])
    for t in range(len(Veri_Isimler)):
        Fark_Deger= ResimFarkBul(Resim,Veri_Resimler[t])
        if(Fark_Deger<Min_Deger):
            Min_Deger = Fark_Deger
            Min_Index=t
    return Veri_Isimler[Min_Index]




Veri_Isimler, Veri_Resimler= VeriYukle()
#Veri_Resim1= cv2.imread("veri/bir.jpg",0)
while True:
    ret, Kare = Kamera.read()
    Kesilmiskare = Kare[160:450, 160:450]
    KesilmiskareGri = cv2.cvtColor(Kesilmiskare, cv2.COLOR_BGR2GRAY)
    Kesilmiskare_HSV = cv2.cvtColor(Kesilmiskare, cv2.COLOR_BGR2HSV)

    Altdeger = np.array([0, 30, 50])
    Ustdeger = np.array([40, 255, 255])

    Renkfiltreleme = cv2.inRange(Kesilmiskare_HSV, Altdeger, Ustdeger)
    Renkfiltreleme = cv2.morphologyEx(Renkfiltreleme, cv2.MORPH_CLOSE, kernel)
    Renkfiltreleme = cv2.dilate(Renkfiltreleme,kernel,iterations=1)

    Sonuc = Kesilmiskare.copy()
    cnts, hierarchy  = cv2.findContours(Renkfiltreleme,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    Max_Genislik=0
    Max_Uzunluk=0
    Max_Index=-1
    for t in range(len(cnts)):
        cnt= cnts[t]
        x, y, w, h = cv2.boundingRect(cnt)
        if(w>Max_Genislik and h>Max_Uzunluk):
            Max_Uzunluk=h
            Max_Genislik=w
            Max_Index=t

    if(len(cnts)>0):
        x, y, w, h = cv2.boundingRect(cnts[Max_Index])
        cv2.rectangle(Sonuc, (x, y), (x + w, y + h), (250, 255, 0), 2)
        El_Resim= Renkfiltreleme[y:y+h,x:x+w]
        cv2.imshow("El resmi",El_Resim)
        print(Siniflandir(El_Resim,Veri_Isimler,Veri_Resimler))

        textt = str(Siniflandir(El_Resim, Veri_Isimler, Veri_Resimler))
        texttt = str(Siniflandir(El_Resim, Veri_Isimler, Veri_Resimler))
        font = cv2.FONT_HERSHEY_SIMPLEX
        Kare = cv2.putText(Kare, texttt, (10, 50), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("Kare", Kare)
        # cv2.imshow("Kesilmiskare", Kesilmiskare)
        cv2.imshow("Renk filtre sonucu", Renkfiltreleme)


        Sonuc =cv2.putText(Sonuc,textt,(10,50),font,1,(0,255,255),2,cv2.LINE_AA)
        cv2.imshow("Sonuc", Sonuc)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Kamera.release()
cv2.destroyAllWindows()
