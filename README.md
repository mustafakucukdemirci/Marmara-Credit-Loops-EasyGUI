# Marmara-Credit-Loops-EasyGUI

__Türkçe__<br>
Marmara kredi döngüleri EASYGUI programınının çalıştırılabilir sürümününün kaynak kodlarıdır.

Programın çalıştırabilmek için bilgisayarınızda python 3.7 ve üstü sürümlerinin bulunması gereklidir.

Alttaki komut ile program arayüzünü çalıştırabilirsiniz. (IDE'ler genellikle bir den çok thread ile çalışırken sorunlar yaşadığı için path ile çalıştırmanızı şiddetle
tavsiye ediyorum)<br>
![](/readmepictures/runlogin.png)

IDE veya doğrudan çalıştırmak için ntc(not to compile) klasöründe ki kaynak dosyaları kullanınız. pyinstaller ile compile etmek için src dosyasını kullanabilirsiniz.<br>
Komut istemcisinin açılmasını engellemek için compile edilen versiyonda bazı parametreler değiştirilmiştir <br>

__Dil Desteği__<br>
lang klasörü içinde ki tr.json klasörünün aynı formatında istediğiniz dilde çeviri yapabilirsiniz. İngilizce desteği çok kısa süre içerisinde tarafımca eklenecektir.
Dil modülü tamamlandığında, yeni dil seçenekleri eklemek için herhangi bir kod yazımına gerek kalmadan lang klasörüne atılarak yeni dil seçenekleri kullanılabilir olacaktır.<br>
<br>


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
<br><br>
__Rehber__<br>
![giriş](/readmepictures/loginScreen.png)<br>
Burası giriş kısmıdır. En üstteki kısımdan kendinize profil seçebilir ve giriş yapabilirsiniz.<br>
Yeni profil oluşturmak için en üstteki sekmeyi seçiniz.<br>
Dil kısmından diğer dillere geçebilirsiniz.*Dil değiştirdiğinizde* <br>
*değişikliklerin aktif olması için kapatıp tekrar açmanız gerekmektedir*<br>Cüzdan yükle bölümünden kendi wallet.dat dosyanızı yükleyebilirsiniz.<br>
Farklı bir cüzdan yüklediğinizde eski dosyalarınız yedeklenir. Yedeklenmiş dosyalara *yedekten yükle* kısmından erişebilirsiniz.<br>
![yeni profil](/readmepictures/new_profile.png)<br>
Yeni profil oluşturma ekranı<br>
Ana ekranda görünecek ismi girip oluştura tıklayabilirsiniz. Zincire bağlanacak ve sizin için yeni bir hesap oluşturacaktır.<br>
Hesap oluşturulduktan sonra hesabın bilgilerini kaydetmeniz için bir klasör seçmeniz istenecektir. Seçtikten sonra priv key vs.<br>
önemli bilgilerin olduğu bir dosya seçtiğiniz yere kaydedilecektir. Bu dosyayı kimselerle paylaşmayınız.<br>
![txt](/readmepictures/txtFile.png)<br>
Kaydedilen txt dosyasının bir örneği. <br>
![cüzdan yükle](/readmepictures/load_wallet.png)<br>
Cüzdan yükleme sekmesine, yeni cüzdanda kaydedilecek ilk hesabın profil adınızı giriniz.<br>
Mevcut dosyalar yedekleneceği için yedek listesinde görüneceği ismi seçiniz.<br>
Hesabınıza bağlanırken kullanacağınız pubkeyi giriniz.<br>
Cüzdanı aç butonuna tıklayarak gelen ekrandan wallet.dat dosyasını seçiniz.<br>
Yükle dediğiniz zaman program zincire bağlanacak, yeni profil verilerini çekecek, eski verileri yedekleyecektir.<br>
![backup](/readmepictures/backupScreen.png)<br>
Geçmiş backup kayıtlarının tutulduğu yer. Seçip yükle diyerek eski kayıtlarınıza geri dönebilirsiniz.<br><br>
Giriş yap dedikten sonra uygulamanın ana penceresi gelecektir.<br>
![main](/readmepictures/mainScreen.png)<br>
En üst ekranda adresiniz ve pubkeyiniz bulunmaktadır. Sadece tıklayarak, kopyalayabilirsiniz.<br>
Mining,Staking,3xStaking ve boosted özelliklerinin anlık olarak aktif olup olmadığını görebilirsiniz.<br>
Anlık döngü istekleri sayısını ise sağ üstte görebilirsiniz.<br>
Normal bakiye: pubkeye tanımlı bakiyeyi gösterir. Cüzdan bakiyesi, wallet.dat üzerinde ki toplam bakiyeyi gösterir.<br>
Toplam kilitli bakiye ise kilitli(locked) bakiyenizi gösterir.<br>
Coin Gönder sekmesine tıklarsanız:<br>
![coin](/readmepictures/coinGonder.png)<br>
adresi ve gönderilecek miktarı girerek istediğiniz hesaba bakiye gönderimi yapabilirsiniz.<br>



<br><br><br><br>
__English__<br>
Marmara Credit Loops EasyGUI executable file source codes.

python 3.7 or higher versions are required.

While testing program, for sake of stabilization, you should run program via path system. <br>
![command prompt](/readmepictures/runlogin.png)

To run directly, use ntc(not to compile) directory. To make executable, prefer src file to prevent opening command prompt<br>

__Language Support__<br>
Make language files as the same format lang/tr.json.English version will come in a short time.
Whenever langsupport.py is done, new language options can be added without need a single line of code.<br>
<br>

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


<br><br>
__TODO LIST__<br>
#1 - Some threads are not closed after push close. Detect which threads have problem.<br>
~~#2 - Language support~~ __ADDED__<br>
#3 - Catch errors outputs and show output in popup window.<br>
#4 - Update system<br>
#5 - Some visual improvements<br>

<br><br><br>
__Guide To Program Usage__




























