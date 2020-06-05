Vikipedi Crawler Rapor
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

