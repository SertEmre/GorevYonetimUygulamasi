import json
import os

class Gorev:
    def __init__(self, baslik, aciklama):
        self.baslik = baslik
        self.aciklama = aciklama  
        self.tamamlanmaDurumu = False

class GorevYonetimi:
    def __init__(self):
        self.gorevler = []
        self.gorevleriDosyadanYukle()
    
    def gorevleriDosyadanYukle(self):
        if os.path.exists("gorevler.json"):
            with open("gorevler.json", "r", encoding="utf-8") as file:
                gorev_listesi = json.load(file)
                for gorev_sozluk in gorev_listesi: 
                    yeni_gorev = Gorev(
                        baslik=gorev_sozluk["baslik"],
                        aciklama=gorev_sozluk["aciklama"]
                    )
                    yeni_gorev.tamamlanmaDurumu = gorev_sozluk["tamamlanmaDurumu"]
                    self.gorevler.append(yeni_gorev)
            print("Görevler yüklendi")
        else:
            print("Tamamlanacak görev yok")

    def gorevEkle(self, gorev: Gorev):
        self.gorevler.append(gorev)
        self.gorevleriDosyayaKaydet()
        print("Yeni görev eklendi.")

    def gorevleriListele(self):
        if len(self.gorevler) == 0:
            print("Tamamlanacak görev bulunmuyor")
        else:
            for sira, gorev in enumerate(self.gorevler, start=1):
                durum = "Tamamlandı" if gorev.tamamlanmaDurumu else "Devam ediyor"
                print(f"{sira}. Başlık: {gorev.baslik} - Açıklama: {gorev.aciklama} - Durumu: {durum}")
    
    def gorevTamamla(self, sira_numarasi):  
        if 0 < sira_numarasi <= len(self.gorevler):
            secilen_gorev = self.gorevler[sira_numarasi - 1]
            secilen_gorev.tamamlanmaDurumu = True
            self.gorevleriDosyayaKaydet()
            print(f"{secilen_gorev.baslik} görevi tamamlandı.")
        else:
            print("Geçersiz numara girdiniz.")     

    def gorevleriDosyayaKaydet(self):
        kaydedilecek_liste = []
        for gorev in self.gorevler:
            gorev_sozluk = {
                "baslik": gorev.baslik,
                "aciklama": gorev.aciklama,
                "tamamlanmaDurumu": gorev.tamamlanmaDurumu
            }
            kaydedilecek_liste.append(gorev_sozluk)
        
        with open("gorevler.json", "w", encoding="utf-8") as file:
            json.dump(kaydedilecek_liste, file, ensure_ascii=False, indent=4)

yonetim = GorevYonetimi()

while True:
    print("Görev Uygulaması".center(50, "*"))
    secim = input("1- Görev Ekle\n2- Görevleri Listele\n3- Görev Durumunu Güncelle\n4- Çıkış Yap\nSeçiminiz: ")

    if secim == "4":
        print("Çıkış")
        break
    elif secim == "1":
        baslik = input("Görev Başlığı: ")
        aciklama = input("Görev Açıklaması: ")
        yeni_gorev = Gorev(baslik=baslik, aciklama=aciklama)
        yonetim.gorevEkle(yeni_gorev)
    elif secim == "2":
        yonetim.gorevleriListele()
    elif secim == "3":
        yonetim.gorevleriListele()
        try:
            sira = int(input("Tamamlamak istediğiniz görev numarasını girin: "))
            yonetim.gorevTamamla(sira)
        except ValueError:
            print("Lütfen sadece sayı giriniz.")
    else:
        print("Geçersiz seçim yaptınız")
