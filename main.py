# Öncelikle, gerekli kütüphaneleri import ediyoruz.
import json
import socket

# Yukarıda verdiğiniz kodları kendi dosyalarınızda kullanabilmeniz için ihtiyacınız olan sınıfları dahil ediyoruz.
from Helper import Helper, HttpClient
from configs import Configs
from PaymentLinkCreateRequest import PaymentLinkCreateRequest

def main():
    # Configs sınıfı için gerekli ayarları yapalım
    publicKey = "YOUR_PUBLIC_KEY"
    privateKey = "YOUR_PRIVATE_KEY"
    baseUrl = "https://api.ipara.com"
    mode = "T"  # Test modunda çalışacaksa "T", canlı modda çalışacaksa "P" olarak ayarlayın
    echo = "https://www.yourdomain.com"  # 3D Secure işlemlerinde kullanılacak URL adresi
    version = "1.0"  # Kullandığınız iPara API versiyonu
    hashString = ""  # HashString, işlem yapacağınız servisin bilgisine göre doldurulmalıdır
    transactionDate = ""  # TransactionDate olarak kullanılacak alan bilgisi

    # Configs sınıfını oluşturalım
    configs = Configs(publicKey, privateKey, baseUrl, mode, echo, version, hashString, transactionDate)

    # PaymentLinkCreateRequest sınıfından bir örnek oluşturalım
    req = PaymentLinkCreateRequest()

    # Host adını alalım ve IP adresini alalım
    hostname = socket.gethostname()
    client_ip = socket.gethostbyname(hostname)

    # Kullanıcıdan gerekli bilgileri alalım
    req.clientIp = client_ip
    req.name = input("Lütfen Müşterinin Adını Giriniz: ")
    req.surname = input("Lütfen Müşterinin Soyadını Giriniz: ")
    req.tcCertificate = input("Lütfen Müşterinin TC Kimlik Numarasını Giriniz(Opsiyonel): ")
    req.email = input("Lütfen Müşterinin E-Posta Adresini Giriniz: ")
    req.gsm = input("Lütfen Müşterinin GSM Numarasını Giriniz: ")
    req.amount = input("Lütfen Ödeme Tutarını Giriniz: ")

    # Helper sınıfından bir örnek oluşturalım
    helper = Helper()

    # TransactionDate'i ayarlayalım
    configs.TransactionDate = helper.GetTransactionDateString()

    # HashString'i oluşturalım
    configs.HashString = configs.PrivateKey + req.name + req.surname + req.email + req.amount + req.clientIp + configs.TransactionDate

    # JSON verisini oluşturalım
    json_data = json.dumps(req.__dict__)

    # Ödeme linki oluşturma isteğini gerçekleştirelim
    result = req.execute(req, configs)

    # Sonucu ekrana basalım
    print("Ödeme linki oluşturma işlemi tamamlandı. Sonuç:", result)

if __name__ == "__main__":
    main()
