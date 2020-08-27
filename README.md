# Marmara-Credit-Loops-EasyGUI

__Türkçe__<br>
Marmara kredi döngüleri EASYGUI programınının çalıştırılabilir sürümününün kaynak kodlarıdır.

Programın çalıştırabilmek için bilgisayarınızda python 3.7 ve üstü sürümlerinin bulunması gereklidir.

Alttaki komut ile program arayüzünü çalıştırabilirsiniz. (IDE'ler genellikle bir den çok thread ile çalışırken sorunlar yaşadığı için path ile çalıştırmanızı şiddetle
tavsiye ediyorum)<br>
![](/blob/main/runlogin.png)

IDE veya doğrudan çalıştırmak için ntc(not to compile) klasöründe ki kaynak dosyaları kullanınız. pyinstaller ile compile etmek için src dosyasını kullanabilirsiniz.<br>
Komut istemcisinin açılmasını engellemek için compile edilen versiyonda bazı parametreler değiştirilmiştir <br>

__Dil Desteği__<br>
lang klasörü içinde ki tr.json klasörünün aynı formatında istediğiniz dilde çeviri yapabilirsiniz. İngilizce desteği çok kısa süre içerisinde tarafımca eklenecektir.
Dil modülü tamamlandığında, yeni dil seçenekleri eklemek için herhangi bir kod yazımına gerek kalmadan lang klasörüne atılarak yeni dil seçenekleri kullanılabilir olacaktır.<br>
<br>


__Nasıl Doğrudan Çalıştırılabilir Hale Getirilir?__

pyinstaller -y -F -w --add-data "file_path/history.py";"." --add-data "file_path/langsupport.py";"." --add-data "file_path/loginui.py";"." --add-data "file_path/loopChecker.py";"." --add-data "file_path/loopwindow.py";"." --add-data "file_path/sidebaar.py";"." --hidden-import pkg_resources.py2_warn  "file_path/login.py"


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

![](/blob/main/fetch-params.png)<br>
Eğer ki daha önce parametreleri çekmediyseniz, önce parametrelerin indirilmesini beklemelisiniz. Yaklaşık olarak 1.5GB parametreler indiriliyor, indirme süresi internet hızınızla bağlantılı olarak değişecektir.
![giriş](/blob/main/loginScreen.png)<br>
Burası giriş kısmıdır. En üstteki kısımdan kendinize profil seçebilir ve giriş yapabilirsiniz.<br>
Yeni profil oluşturmak için en üstteki sekmeyi seçiniz.<br>
Dil kısmından diğer dillere geçebilirsiniz.*Dil değiştirdiğinizde* <br>
*değişikliklerin aktif olması için kapatıp tekrar açmanız gerekmektedir*<br>Cüzdan yükle bölümünden kendi wallet.dat dosyanızı yükleyebilirsiniz.<br>
Farklı bir cüzdan yüklediğinizde eski dosyalarınız yedeklenir. Yedeklenmiş dosyalara *yedekten yükle* kısmından erişebilirsiniz.<br>
![yeni profil](/blob/main/new_profile.png)<br>
Yeni profil oluşturma ekranı<br>
Ana ekranda görünecek ismi girip oluştura tıklayabilirsiniz. Zincire bağlanacak ve sizin için yeni bir hesap oluşturacaktır.<br>
Hesap oluşturulduktan sonra hesabın bilgilerini kaydetmeniz için bir klasör seçmeniz istenecektir. Seçtikten sonra priv key vs.<br>
önemli bilgilerin olduğu bir dosya seçtiğiniz yere kaydedilecektir. Bu dosyayı kimselerle paylaşmayınız.<br>
![txt](/blob/main/txtFile.png)<br>
Kaydedilen txt dosyasının bir örneği. <br>
![cüzdan yükle](/blob/main/load_wallet.png)<br>
Cüzdan yükleme sekmesine, yeni cüzdanda kaydedilecek ilk hesabın profil adınızı giriniz.<br>
Mevcut dosyalar yedekleneceği için yedek listesinde görüneceği ismi seçiniz.<br>
Hesabınıza bağlanırken kullanacağınız pubkeyi giriniz.<br>
Cüzdanı aç butonuna tıklayarak gelen ekrandan wallet.dat dosyasını seçiniz.<br>
Yükle dediğiniz zaman program zincire bağlanacak, yeni profil verilerini çekecek, eski verileri yedekleyecektir.<br>
![backup](/blob/main/backupScreen.png)<br>
Geçmiş backup kayıtlarının tutulduğu yer. Seçip yükle diyerek eski kayıtlarınıza geri dönebilirsiniz.<br><br>
Giriş yap dedikten sonra uygulamanın ana penceresi gelecektir.<br>
![main](/blob/main/mainScreen.png)<br>
En üst ekranda adresiniz ve pubkeyiniz bulunmaktadır. Sadece tıklayarak, kopyalayabilirsiniz.<br>
Mining,Staking,3xStaking ve boosted özelliklerinin anlık olarak aktif olup olmadığını görebilirsiniz.<br>
Anlık döngü istekleri sayısını ise sağ üstte görebilirsiniz.<br>
Normal bakiye: pubkeye tanımlı bakiyeyi gösterir. Cüzdan bakiyesi, wallet.dat üzerinde ki toplam bakiyeyi gösterir.<br>
Toplam kilitli bakiye ise kilitli(locked) bakiyenizi gösterir.<br>
Coin Gönder sekmesine tıklarsanız:<br>
![coin](/blob/main/coinGonder.png)<br>
adresi ve gönderilecek miktarı girerek istediğiniz hesaba bakiye gönderimi yapabilirsiniz.<br>
![lockCoin](/blob/main/lockCoin.png)<br>
Miktarı girerek coin kitle diyerek kitleyebilir ve coin aç diyerek(aktif hale geldiğinde) kilitli coinlerinizi açabilirsiniz.<br>
![mining](/blob/main/Mining.png)<br>
Mining Aç ve Staking aç butonları ile mining ve stakingi aktifleştirebilirsiniz. Mining veya Staking kapat<br>
dediğiniz zaman hem mining hem de staking kapanmaktadır.<br><br>

*Döngü İstekleri Bölümü*<br>
![firstloop](/blob/main/firstLoopRequest.png)<br>
*ilk döngü isteği:* ilgili yerleri doldurarak girmiş olduğuz pubkey adresine sahip kişiye döngü isteği göndermiş olursunuz.<br>
Keşidecinin döngü istekleri bölümüne düşer. Onaylaması durumunda döngü gerçekleşmiş olur.<br>
![loop_check](/blob/main/loop_check.png)<br>
*döngü kontrolü:* Batonu girerek bitmiş veya aktif olan bütün döngüleri görebilirsiniz.<br>
Zincirden veri gelme süresi bazen uzayabildiği için bir süre beklemeniz gerekebilir.<br>
![loop transfer](/blob/main/loopTransfer.png)<br>
*döngü transferi:* hali hazırda bulunan döngünüzü bir başka hesaba transfer edebilirsiniz.(Karşıdan döngünün isteğinin yapılmış olması gerekmektedir.)<br>
Daha sonra alıcının pubkeyini ve göndermek istediğiniz döngünün batonunu girerek mevcut döngünüzü transfer edebilirsiniz<br>
![loop Request](/blob/main/loopRequest.png)<br>
*döngü isteği:* ilk döngü isteğinden farklı olarak zaten varolan bir döngüyü istemek için yapılır.<br>
İstek yapılan hesabın pubkeyi ve istenilen döngünün batonu girilerek istek gönderilir.<br>
Daha sonra gönderici hesapta döngü transferi işlemlerini yaparak döngüyü gönderebilir.<br>


<br><br><br><br>
__English__<br>
Marmara Credit Loops EasyGUI executable file source codes.

python 3.7 or higher versions are required.

While testing program, for sake of stabilization, you should run program via path system. <br>
![command prompt](/blob/main/runlogin.png)

To run directly, use ntc(not to compile) directory. To make executable, prefer src file to prevent opening command prompt<br>

__Language Support__<br>
Make language files as the same format lang/tr.json.English version will come in a short time.
Whenever langsupport.py is done, new language options can be added without need a single line of code.<br>
<br>

__How to Create Executable Version?__<br>
You should use pyinstaller library and parameters below.
<br>pyinstaller -y -F -w --add-data "file_path/history.py";"." --add-data "file_path/langsupport.py";"." --add-data "file_path/loginui.py";"." --add-data "file_path/loopChecker.py";"." --add-data "file_path/loopwindow.py";"." --add-data "file_path/sidebaar.py";"." --hidden-import pkg_resources.py2_warn  "file_path/login.py"


<br><br>

login.py       -> Create wallet, backups etc.

loginui.py     -> Login user interface.

history.py     -> receive operation history of wallet from Explorer API and process them.

loopwindow.py  -> Checks Loop requests.

loopChecker.py -> Closed and active loops check and save locally.

sidebaar.py    -> Main program body and threads. 


<br><br>
__TODO LIST__<br>
~~#1 - Language support~~ __ADDED__<br>
#2 - Catch errors outputs and show output in popup window.<br>
#3 - Update system<br>
#4 - Some visual improvements<br>

<br><br><br>
__Guide To Program Usage__<br>
will be added sooon...



























