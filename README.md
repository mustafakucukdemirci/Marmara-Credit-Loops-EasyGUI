# Marmara-Credit-Loops-EasyGUI

Marmara Credit Loops EasyGUI executable file source codes.

Marmara kredi döngüleri EASYGUI programınının çalıştırılabilir sürümününün kaynak kodlarıdır.

Programın çalıştırabilmek için bilgisayarınızda python 3.7 ve üstü sürümlerinin bulunması gereklidir.

Alttaki komut ile program arayüzünü çalıştırabilirsiniz. 

![komut arayüzü](/readmepictures/runlogin.png)

Mevcut kodlar derlemeye hazır halde olduğu için, doğrudan çalıştırabilmek için subprocess.run kısımlarında ki parametrelerden sadece stdout = subprocess.PIPE kalmalı
ve diğerleri silinmelidir. Silinmeden işlem yapılırsa streamlerden kaynaklı olarak gerekli komutlar çalışmayacaktır.
(Kısayol olarak bir editör ile açıp ctrl+R ile hepsini bir kaç seferde değiştirebilirsiniz.)


__Nasıl Doğrudan Çalıştırılabilir Hale Getirilir?__

pyinstaller -y -F -w --add-data "filepath/history.py";"./" --add-data "filepath/loginui.py";"./" --add-data "filepath/loopChecker.py";"./" --add-data "filepath/loopwindow.py";"./" --add-data "filepath/sidebaar.py";"./"  "filepath/login.py"


Pyinstaller kütüphanesini ve yukarıda ki parametreleri kullanarak programın çalıştırılabilir(executable) hale getirebilirsiniz.


login.py       -> Cüzdan açma, yedekleme vs. işlemlerin bulunduğu dosya.

loginui.py     -> Ana giriş arayüz kodları.

history.py     -> explorer APIden işlem geçmişinin çekilmesi ve işlenmesi.

loopwindow.py  -> Döngü isteklerinin sürekli arka planda kontrol edildiği Thread sınıfı.

loopChecker.py -> Kapalı ve aktif döngülerin kontrol edildiği, kaydedildiği Thread sınıfı.

sidebaar.py    -> Cüzdana giriş yaptıktan sonra açılan ana ekran arayüzünün bulunduğu, gerekli threadlerin başlatıldığı kısım 









































