Vikipedi Crawler Rapor
Ali Emre Kürekci
Vikipedi, kullanıcıları tarafından ortaklaşa olarak birçok dilde hazırlanan, özgür, bağımsız, ücretsiz, reklamsız, kâr amacı gütmeyen bir internet ansiklopedisidir. Media Wiki yazılımı kullanılarak hazırlanmaktadır. Sürekli eklemeler ve değişiklikler yapıldığı için hiçbir zaman tamamlanmayacağı varsayılmaktadır.

Herkesin paylaşım yapmasına olanak sağlayan Vikipedi ‘de bilgi güvenliğinin sağlanması da elbette büyük önem kazanıyor. Bu bilgi güvenliği, güvenilirliğini ispatlamış -yine kullanıcılar tarafından hazırlanan- bot veya özel yetkili gruplar tarafından denetimler yapılarak sağlanabiliyor. Bu yetkili kişiler denetimi gerçekleştirdikten sonra eğer doküman üzerinde yapılan değişiklik hatalı ise döküman bir önceki sürüme geri yüklenir veya eklenen değişiklik kaldırılır.

Ben yaptığım çalışma ile şüpheli değişikleri makine öğrenmesi kullanarak tespit etmeyi hedefliyorum. Dökümanın geçmişine bakarak değişiklik yapan kullanıcıların web crawler tekniği ile kişisel olmayan Vikipedi verilerini BeatifulSoup ve selenium kütüphanelerini kullanarak aldım. Kullanıcının kayıtlı olup olmadığına, Vikipedi tarafından verilen ünvanı olup olmadığına, yıl, ay, gün olarak ne kadar süredir kayıtlı olduğuna, bu zamana kadar kaç değişiklik yaptığına ve değişiklik yaptığı dokümandaki bayt boyutunda değişim değerine bakarak şüpheli(suspect:True) ve değil(False) olarak bir  sınıflandırma yaptım.

Aldığım verileri gereksiz bilgilerden kurtulmak için ön işlem ve veri temizliği yaptım. Düzenlediğim verileri “csv” klasörü altında cleaned_data_#.csv(# dosya numarası) dosya ismiyle kaydettim.

Temizlenen verileri kullanarak eğitim verisi(train data) oluşturdum. Cross-validation(K-fold) yöntemini kullanarak eğitim verisinin doğruluğunu(accuracy) ölçtüm. Vikipedi’de araştırma konusu olarak yoğun bir veri kümesi elde etmek amacıyla 1. Ve 2. Dünya Savaşını seçtim. İki konudan da 500’er veri aldım ve temizledim. Sınıflandırma algoritması olarak Naive Bayes kullandım ve aldığım sonuçlar şöyle:
Linkler:
1.Dünya Savaşı: https://tr.wikipedia.org/w/index.php?title=I._D%C3%BCnya_Sava%C5%9F%C4%B1&action=history
Toplam şüphe (True) sayısı: 71 (500 veri içinde)
2.Dünya Savaşı: https://tr.wikipedia.org/w/index.php?title=II._D%C3%BCnya_Sava%C5%9F%C4%B1&action=history
Toplam şüphe (True) sayısı: 70 (500 veri içinde)
K = 5 (K-fold için)
Sınıflandırmayı yine 5 kere yaptım(5*5) aldığım sonuçlar sırasıyla:
1.Dünya Savaşı			|		2.Dünya Savaşı
Accuracy:	0,63				|		0,86
		0,63				|		0,87
		0,68				|		0,85
		0,67				|		0,81
		0,66				|		0,75

İki veri setinin toplam doğruluk oranlarının ortalaması ise 0.71’dir.

Sonuç olarak kullanıcıdan alınan Vikipedi geçmiş sayfası linki ile yazdığım program kullanılarak 0.71 doğruluk oranıyla sayfadaki şüpheli değişimleri tespit edebiliyorum. Yazdığım program daha doğru sınıflandırma amacıyla farklı sınıflandırma algoritmaları eklenerek veya veri ön işlemi geliştirilerek daha da ilerletilebilir.

Notlar:
Programı kullanabilmek için kullandığınız chrome sürümüne ait driverın indirilmiş ve program içindeki ilgili path değişkenine tanıtılmış olamsı geriyor.
Ondan sonrası çok kolay! SEARCH_ADDRESSES dizisine crawler yapmak istediğiniz viki geçmiş linkini yapıştırmanız gerekiyor.
Önemli değişkenlerin açıklaması:
data_directory: Sonuçların yazdırılacağı adres.
DATA_LIMIT: Crawl etmek istediğiniz data sınırı
file_number: kaydedeceğiniz dosya indexi
is_there_data: Crawl yapmak için False değeri alması gerekiyor. Datayı çektikten sonra True olarak ayarlayarak, veri temizleme işlemine geçebilirsiniz
is_data_cleaned: Accuracy almak için True yapılır. Data çekildikten sonra temizleme işlemi yapılmadıysa False olarak atanmalıdır.
driver_path: Indirdiğiniz chrome drivirini tanıtmalısınız
K: K-fold çapraz validasyon için girmek istediğiniz K değeri

En

Wikipedia Crawler Report
Ali Emre Kürekci|160709031 | HW3

Wikipedia is a free, independent, ad-free, non-profit internet encyclopedia, prepared in several languages jointly by its users. It is prepared using Media Wiki software. It is assumed that it will never be completed, as continuous additions and changes are made.

Of course, it is important to provide information security in Vikipedi that provides everyone can share information. It can be provided by proved is reliability bots that are made by human or real authorized users. After checking by made these group of people and bots, the changings are removed or changed to the last version of document.

I aim to determine suspect cases with the help of machine learning with my project. I looked for history of Wikipedia subject and took non-personal data of Wikipedia users with web crawler technic by using selenium and BeautifulSoup libraries. I classified as True or False by looking whether the user registered or not, the user took a degree from Wikipedia or not, how many changing the user made until now and what size of changing the user made on the document.

I preprocessed and cleaned the data to remove unnecessary information. I saved the prepared data as cleaned_data_#.csv (# file number) file.

I create train data by using the cleaned data. I measured the accuracy by using cross-validation(K-fold) method. I chose I. World War and II. World War to get big data. I got 500 data for each subject and cleaned them. I used Naïve Bayesian as classification algorithm and the results are like:
Links:
1.World War: https://tr.wikipedia.org/w/index.php?title=I._D%C3%BCnya_Sava%C5%9F%C4%B1&action=history
Total Suspect (True) count: 71 (in 500)
2.World War: https://tr.wikipedia.org/w/index.php?title=II._D%C3%BCnya_Sava%C5%9F%C4%B1&action=history
Total Suspect (True) count: 70 (in 500)
K = 5 (for K-fold)
I run 5(5*5) times the program again and results are respectively:
I. World War			|		II. World War
Accuracy:	0,63				|		0,86
		0,63				|		0,87
		0,68				|		0,85
		0,67				|		0,81
		0,66				|		0,75

Total accuracy rate of two data sets is 0.71.

As a conclusion, by using the program I can determine suspect changings of a Wikipedia document with a link taken from user. The program can evolve to classify more reliable results by adding different classification algorithms and by developing preprocessing.

 # global variables and user inputs
DOMAIN = "https://tr.wikipedia.org/"
file_number = 1
SEARCH_ADDRESSES = ["https://tr.wikipedia.org/w/index.php?title=I._D%C3%BCnya_Sava%C5%9F%C4%B1&action=history",
                    "https://tr.wikipedia.org/w/index.php?title=II._D%C3%BCnya_Sava%C5%9F%C4%B1&action=history"]
DATA_LIMIT = 500
data_directory = "wikipedia\\csv\\"
is_there_data = True
is_data_cleaned = True
K = 5                                                                                                  # K-Fold
# driver path for showing to selenium
driver_path = "C:\\Users\\ali19\\OneDrive\\Belgeler\\selenium\\chromedriver.exe"

Important Nots:
In order to use the program, the driver of the chrome version you use must be downloaded and introduced to the relevant path variable in the program. The program is proper for Turkish Wikipedia pages! (The domain is https://tr.wikipedia.org/)
In SEARCH_ADDRESSES, you should add which wiki page you want to crawl.
Important variable explanation:
data_directory: which results are written directory
DATA_LIMIT: Data limit that you want to crawl.
file_number: Saving file index
is_there_data: In order to crawl, it should take False.After cleaning data, you can pass clean process by changing True.
is_data_cleaned: In order to take accuracy, assign True. If you didn’t cleaned data yet, It should be False.
driver_path: You should introduce chrome driver on it
K: K value for cross validation K-fold.

Respectively called functions and their meanings:

def get_user_info(user_link):
It is called by main to get user information, it takes user link and returns text of all ‘a’ html tag

def get_change_size(user_link):
It is called by main to get document change size that was made by the related user, it takes user link and returns change size

def check_revocation(user_link):
It is called by main to check whether the user revocation the changing or not, it takes user link and returns True or False

def preprocessing_data(file):
It is called by main if data exists to prepare data to future usage, it takes data file name and create cleaned_data_#.txt(# file number)

def registration_info_process(registration):
It is called by preprocessing_data and also degree_process functions to convert from registration that is argument string to integer list contain registration information and returns it.

def post_size_process(post_str):
It is called by preprocessing_data and also degree_process functions to prepare post size data of user, it takes string and returns post size integer data of current user

def degree_process(line):
It is called by preprocessing_data function for users who are includes degree informations, to determine degrees of the current user, it takes line read by preprocessing_data function and returns prepared user information list

def write_data(table, file_name):
It is called by preprocessing_data funstion to write all prepare user data(table list) to a csv file(file_name)
def create_train_data(user_info):
It is called main, takes pandas read csv file and returns 80% of the csv file as train and remain as test data

def prediction_by_naive_bayes(trainNB, testNB):
The Naive Bayes classification algorithm called by main and returns accuracy of train and test datas




