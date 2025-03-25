import requests
import time
import random
import pyfiglet
import sys

# Renk kodları
GREEN = "\033[92m"  # Yeşil
RED = "\033[91m"  # Kırmızı
RESET = "\033[0m"  # Renk sıfırla

# User-Agent (Bot engellemelerini aşmak için)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Türkiye'de yaygın sosyal medya platformları URL şablonları ve hata mesajları (Telegram dahil)
SOCIAL_MEDIA_SITES = [
    ("Instagram", "https://www.instagram.com/{}", "Sorry, this page isn't available."),
    ("Twitter", "https://twitter.com/{}", "User not found"),
    ("TikTok", "https://www.tiktok.com/@{}", "Couldn't find this account"),
    ("YouTube", "https://www.youtube.com/{}", "This page isn’t available"),
    ("Facebook", "https://www.facebook.com/{}", "Sorry, this content isn't available"),
    ("Snapchat", "https://www.snapchat.com/add/{}", None),
    ("LinkedIn", "https://www.linkedin.com/in/{}", "Profile not found"),
    ("Reddit", "https://www.reddit.com/user/{}", "Sorry, nobody on Reddit goes by that name"),
    ("Pinterest", "https://www.pinterest.com/{}", "Oops, we couldn't find that page"),
    ("WhatsApp", "https://wa.me/{}", "User not found"),
    ("Telegram", "https://t.me/{}", "User not found")  # Telegram dahil
]

# RGB karışık renk seçimi
def random_rgb_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"\033[38;2;{r};{g};{b}m"

# Renkli ASCII "SONSUZ" banner'ı yazdırma
def print_banner():
    banner_text = "SONSUZ"
    ascii_banner = pyfiglet.figlet_format(banner_text, font="slant")  # "slant" fontu kullan
    color = random_rgb_color()  # RGB karışık renk seç
    print(f"{color}{ascii_banner}{RESET}")

# Kullanıcı adı varyasyonlarını oluştur
def generate_username_variations(first_name, last_name=None):
    variations = []
    
    # İsim ve soyisim ile çeşitli varyasyonlar
    if last_name:
        variations.extend([
            first_name.lower() + last_name.lower(),
            first_name.capitalize() + last_name.capitalize(),
            first_name.lower() + "_" + last_name.lower(),
            first_name.capitalize() + "_" + last_name.capitalize(),
            last_name.lower() + first_name.lower(),
            last_name.capitalize() + first_name.capitalize(),
            first_name.lower() + "123",
            last_name.lower() + "123",
            first_name.lower() + last_name.lower() + "1",
            first_name.capitalize() + last_name.capitalize() + "123",
            first_name.lower() + "_" + last_name.lower() + "_01",
            first_name[0].lower() + last_name.lower() + "01",  # İlk harf + soyisim
            first_name.lower() + last_name[0].lower() + "2025",  # İsim + soyismin ilk harfi + yıl
            first_name + "." + last_name,
            first_name.lower() + "_" + last_name.capitalize(),
            first_name.capitalize() + "_" + last_name.lower(),
            first_name[0].upper() + last_name.capitalize(),
            first_name[0].lower() + last_name.upper()
        ])
    
    # Tek isimle varyasyonlar
    else:
        variations.extend([
            first_name.lower(),
            first_name.capitalize(),
            first_name.lower() + "123",
            first_name.capitalize() + "123",
            first_name.lower() + "_01",
            first_name.capitalize() + "_01",
            first_name + "2025",  # İsim + yıl
            first_name.lower() + "." + str(random.randint(1, 9999)),
            first_name + str(random.randint(100, 999)),
            first_name + "!" + str(random.randint(1, 999)),
            first_name + "_xx",  # İsim + sembol
            first_name.lower() + "x",
            first_name.upper() + str(random.randint(10, 999)),
            first_name[0].upper() + "@" + str(random.randint(100, 999)),
            first_name[0].lower() + "*" + str(random.randint(1000, 9999))
        ])
        
    return variations

# Platformun sayfasını kontrol et. Kullanıcı adı varsa yeşil [+], yoksa kırmızı [-] döndür.
def check_platform(response, site_name, username, error_text):
    page_content = response.text.lower()  # Sayfa içeriğini küçük harfe çevirerek kontrol et

    # Hata metnini kontrol et
    if response.status_code == 404 or (error_text and error_text.lower() in page_content):
        return f"{RED}[-]{RESET} {site_name}: https://www.{site_name.lower()}.com/{username}"
    else:
        return f"{GREEN}[+]{RESET} {site_name}: https://www.{site_name.lower()}.com/{username}"

# Kullanıcıyı karşılayan fonksiyon
def welcome_message():
    print_banner()  # Renkli banner yazdır
    print("Hoşgeldiniz! Bu yazılım kullanılarak sosyal medya kullanıcı adları sorgulanabilir.")
    print("Lütfen bir seçenek girin:")

# Ana menü fonksiyonu
def main_menu():
    while True:
        welcome_message()

        print("\n1. İsim Soyisimle Sorgulama")
        print("2. Kullanıcı Adı ile Sorgulama")
        print("3. Çıkış")
        choice = input("\nSeçiminizi yapın (1/2/3): ").strip()

        if choice == "1":
            first_name = input("\nİsim ve soyisimi girin (Örn: Ahmet Yılmaz): ").strip()
            names = first_name.split()
            if len(names) == 2:
                first_name, last_name = names
                print(f"\n{first_name} {last_name} için kullanıcı adı varyasyonları oluşturuluyor...\n")

                variations = generate_username_variations(first_name, last_name)

                print(f"Bulunan Kullanıcı Adı Varyasyonları: {variations}\n")

                for username in variations:
                    print(f"\n🔍 '{username}' için sorgulama başlatılıyor...\n")
                    search_by_username(username)
            else:
                print("Geçersiz isim soyisim formatı. Lütfen isim ve soyismi doğru formatta girin.")

        elif choice == "2":
            username = input("\nSorgulamak istediğiniz kullanıcı adını girin: ").strip()
            search_by_username(username)
        elif choice == "3":
            print("Çıkış yapılıyor...")
            sys.exit()  # Programı sonlandırır
        else:
            print("Geçersiz seçim! Lütfen 1, 2 veya 3 girin.")

# Kullanıcı Adı ile Sorgulama
def search_by_username(username):
    print(f"\n🔍 '{username}' için sorgulama başlatılıyor...\n")

    # Sonuçları saklamak için
    results = {"found": [], "not_found": []}

    # Kullanıcı adını her platformda kontrol et
    for site_name, url_template, error_text in SOCIAL_MEDIA_SITES:
        url = url_template.format(username)

        try:
            response = requests.get(url, headers=HEADERS, timeout=5)

            result = check_platform(response, site_name, username, error_text)

            # Eğer kullanıcı adı bulunamadıysa
            if "[-]" in result:
                results["not_found"].append(result)
                print(result, end="\r", flush=True)  # Anlık olarak göster
            else:
                results["found"].append(result)
                print(result, end="\r", flush=True)  # Anlık olarak göster

        except requests.RequestException:
            error_message = f"{RED}[-]{RESET} {site_name}: Hata - Siteye erişilemiyor!"
            results["not_found"].append(error_message)
            print(error_message, end="\r", flush=True)

        time.sleep(1)  # Hızlı istekleri önlemek için bekleme süresi

    # Sonuçları dosyaya yaz
    file_name = f"{username}_scamer.txt"

    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"🔍 Kullanıcı Adı: {username}\n")
        f.write("------------ KULLANICI BULUNDU ------------\n")
        for found in results["found"]:
            f.write(f"{found}\n")

        f.write("------------ KULLANICI BULUNAMADI ------------\n")
        for not_found in results["not_found"]:
            f.write(f"{not_found}\n")

        f.write("\n===========================================\n")
    
    print("\n✅ Sorgulama tamamlandı! Sonuçlar dosyaya yazıldı.")
    print(f"Sonuçlar '{file_name}' dosyasına yazıldı.")
    print("Yeni bir kullanıcı adı girebilirsiniz...\n")

# Başlangıç fonksiyonunu çağır
if __name__ == "__main__":
    main_menu()
