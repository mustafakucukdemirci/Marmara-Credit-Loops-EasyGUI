# Marmara-Credit-Loops-EasyGUI

__Türkçe__<br>
Marmara kredi döngüleri EASYGUI programınının çalıştırılabilir sürümününün kaynak kodlarıdır.

Programın çalıştırabilmek için bilgisayarınızda python 3.7 ve üstü sürümlerinin bulunması gereklidir.

Alttaki komut ile program arayüzünü çalıştırabilirsiniz. (IDE'ler genellikle bir den çok thread ile çalışırken sorunlar yaşadığı için path ile çalıştırmanızı şiddetle
tavsiye ediyorum)<br>
![komut arayüzü](/readmepictures/runlogin.png)

Mevcut kodlar derlemeye hazır halde olduğu için, doğrudan çalıştırabilmek için subprocess.run kısımlarında ki parametrelerden sadece stdout = subprocess.PIPE kalmalı
ve diğerleri silinmelidir. Silinmeden işlem yapılırsa streamlerden kaynaklı olarak komut istemine gönderilen komutlar tıkanacak ve çalışmayacaktır. Bu parametreler
doğrudan çalıştırılabilir sürümde komut istemcisinin açılmasını engellemek için eklenmiştir.
(Kısayol olarak bir editör ile açıp ctrl+R ile hepsini bir kaç seferde değiştirebilirsiniz.)


__Nasıl Doğrudan Çalıştırılabilir Hale Getirilir?__

pyinstaller -y -F -w --add-data "filepath/history.py";"./" --add-data "filepath/loginui.py";"./" --add-data "filepath/loopChecker.py";"./" --add-data "filepath/loopwindow.py";"./" --add-data "filepath/sidebaar.py";"./"  "filepath/login.py"


Pyinstaller kütüphanesini ve yukarıda ki parametreleri kullanarak programın çalıştırılabilir(executable) hale getirebilirsiniz.

<br><br>

login.py       -> Cüzdan açma, yedekleme vs. işlemlerin bulunduğu dosya.

loginui.py     -> Ana giriş arayüz kodları.

history.py     -> explorer APIden işlem geçmişinin çekilmesi ve işlenmesi.

loopwindow.py  -> Döngü isteklerinin sürekli arka planda kontrol edildiği Thread sınıfı.

loopChecker.py -> Kapalı ve aktif döngülerin kontrol edildiği, kaydedildiği Thread sınıfı.

sidebaar.py    -> Cüzdana giriş yaptıktan sonra açılan ana ekran arayüzünün bulunduğu, gerekli threadlerin başlatıldığı kısım 


<br><br><br><br>
__English__<br>
Marmara Credit Loops EasyGUI executable file source codes.

python 3.7 or higher versions are required.

While testing program, for sake of stabilization, you should run program via path system. <br>
![command prompt](/readmepictures/runlogin.png)

To prevent opening of command prompt in executable version, subprocess.run lines are parameterized. To be able to run program with python you should change parameters
as only remain stdout = subprocess.PIPE. You can do this on any editor by ctrl+R and few operation.

__How to Create Executable Version?__<br>
You should use pyinstaller library and parameters below.
<br>pyinstaller -y -F -w --add-data "filepath/history.py";"./" --add-data "filepath/loginui.py";"./" --add-data "filepath/loopChecker.py";"./" --add-data "filepath/loopwindow.py";"./" --add-data "filepath/sidebaar.py";"./"  "filepath/login.py"


<br><br>

login.py       -> Create wallet, backups etc.

loginui.py     -> Login user interface.

history.py     -> receive operation history of wallet from Explorer API and process them.

loopwindow.py  -> Checks Loop requests.

loopChecker.py -> Closed and active loops check and save locally.

sidebaar.py    -> Main program body and threads. 
































