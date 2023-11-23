from datetime import datetime
import pandas as pd

departman_kodlari = {
    "Yönetim": 201,
    "Muhasebe": 202,
    "Ofis": 203,
    "Lojistik": 204,
    "Üretim": 205,
}


def generate_personel_no(departman_no, counter):
    return f"{departman_no}{datetime.now().strftime('%Y')[-2:]}{counter:04d}"


def get_departman_no(departman):
    for key, value in departman_kodlari.items():
        if departman.lower() == key.lower():
            return value
    return None


# sayac okuma
def read_counter_from_file(file_path):
    try:
        with open(file_path, "r") as dosya:
            return int(dosya.read())
    except FileNotFoundError:
        return 1


# sayac yazma
def write_counter_to_file(file_path, counter):
    with open(file_path, "w") as dosya:
        dosya.write(str(counter))


ad = input("Ad giriniz: ")
soyad = input("Soyad giriniz: ")
departman = input("Departman giriniz: ")


departman_no = get_departman_no(departman)
if not departman_no:
    print("Geçersiz departman kodu.")
    exit()

counter = read_counter_from_file("data")

personel_no = generate_personel_no(departman_no, counter)

print(f"{ad} {soyad}'ın personel numarası: {personel_no}")

new_data = pd.DataFrame(
    {
        "Ad": [ad],
        "Soyad": [soyad],
        "Departman": [departman],
        "Personel No": [personel_no],
        "Başlangıç Tarihi": [datetime.now().strftime("%d.%m.%Y")],
    }
)


counter += 1
write_counter_to_file("data", counter)

# excel
try:
    df = pd.read_excel("personel_data.xlsx")
except FileNotFoundError:
    df = pd.DataFrame(
        columns=["Ad", "Soyad", "Departman", "Personel No", "Başlangıç Tarihi"]
    )
df = pd.concat([df, new_data], ignore_index=True)
df.to_excel("personel_data.xlsx", index=False)
