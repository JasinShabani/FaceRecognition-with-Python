import cv2
import numpy as np
import os

Kamera = cv2.VideoCapture(0)
kernel = np.ones((15, 15), np.uint8)

isim = "mustafa"
while True:
    ret, Kare = Kamera.read()
    Kesilmiskare = Kare[0:250, 0:250]
    KesilmiskareGri = cv2.cvtColor(Kesilmiskare, cv2.COLOR_BGR2GRAY)
    Kesilmiskare_HSV = cv2.cvtColor(Kesilmiskare, cv2.COLOR_BGR2HSV)

    Altdeger = np.array([0, 30, 50])
    Ustdeger = np.array([40, 255, 255])

    Renkfiltreleme = cv2.inRange(Kesilmiskare_HSV, Altdeger, Ustdeger)
    Renkfiltreleme = cv2.morphologyEx(Renkfiltreleme, cv2.MORPH_CLOSE, kernel)
    Renkfiltreleme = cv2.dilate(Renkfiltreleme, kernel, iterations=1)
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
        cv2.rectangle(Sonuc, (x, y), (x + w, y + h), (0, 255, 0), 2)
        El_Resim= Renkfiltreleme[y:y+h,x:x+w]
        cv2.imshow("El resmi",El_Resim)
    cv2.imshow("Kare", Kare)
    # cv2.imshow("Kesilmiskare", Kesilmiskare)
    cv2.imshow("Renk filtre sonucu", Renkfiltreleme)
    cv2.imshow("Sonuc", Sonuc)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.imwrite("veri/"+isim+".jpg",El_Resim)


Kamera.release()
cv2.destroyAllWindows()