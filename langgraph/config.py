
# Veritabanı Bağlantı Bilgileri
DB_HOST = "localhost"
DB_DATABASE = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_PORT = "5432"

# Tablo Adları
HASTAID_TABLE_NAME = "hastaid"
HASTALAB_TABLE_NAME = "hastalab"

# Tablo Şemaları ve Açıklamaları
HASTAID_COLUMNS_INFO = {
    "patient_id": "Hastanın eşsiz kimlik numarası (INTEGER). 'Hasta ID'si X olan kişi' gibi sorgularda 'patient_id = X' şeklinde kullanılır.",
    "age": "Hastanın yaşı (INTEGER).",
    "gender": "Hastanın cinsiyeti (VARCHAR).",
    "blood_type": "Hastanın kan grubu (VARCHAR). Örnek: 'A+', 'O-'.",
    "Height (cm)": "Hastanın boyu santimetre cinsinden (REAL).",
    "Weight (kg)": "Hastanın kilosu kilogram cinsinden (REAL).",
    "bmi": "Vücut Kitle İndeksi (REAL).",
    "Temperature (C)": "Vücut Sıcaklığı Santigrat derece (°C) (REAL).",
    "Heart_Rate (bpm)": "Kalp Atış Hızı (dakikadaki atım sayısı) (INTEGER).",
    "Blood_Pressure (mmHg)": "Kan Basıncı (VARCHAR). Örnek: '120/80'."
}

HASTALAB_COLUMNS_INFO = {
    "patient_id": "Hastanın eşsiz kimlik numarası (INTEGER). 'Hasta ID'si X olan kişi' gibi sorgularda 'patient_id = X' şeklinde kullanılır.",
    "result_date": "Laboratuvar sonucunun alındığı tarih (DATE veya VARCHAR).",
    "hemoglobin": "Hemoglobin seviyesi (g/dL) (REAL).",
    "hematocrit": "Hematokrit yüzdesi (%) (REAL).",
    "wbc": "Beyaz kan hücresi sayısı (×10^3/µL) (REAL).",
    "rbc": "Kırmızı kan hücresi sayısı (×10^6/µL) (REAL).",
    "platelets": "Trombosit (platelet) sayısı (/µL) (INTEGER).",
    "mch": "Ortalama korpüsküler hemoglobin (pg) (REAL).",
    "mchc": "Ortalama korpüsküler hemoglobin konsantrasyonu (g/dL) (REAL).",
    "mcv": "Ortalama korpüsküler hacim (fL) (REAL).",
    "rdw": "Eritrosit dağılım genişliği (%) (REAL).",
    "mpv": "Ortalama trombosit hacmi (fL) (REAL).",
    "notes": "Klinik notlar veya hasta şikayetleri (TEXT veya VARCHAR)."
}

# Şemaları LLM için formatlama
def format_columns_info_for_prompt(table_name, columns_info_dict):
    formatted_string = f"'{table_name}' tablosu için kullanabileceğin kolonlar ve açıklamaları:\n"
    for col_name, col_desc in columns_info_dict.items():
        display_col_name = f'"{col_name}"' if any(c in ' ()/' for c in col_name) else col_name
        formatted_string += f"- {display_col_name}: {col_desc}\n"
    return formatted_string

# Prompt'ta kullanılacak formatlanmış şema bilgileri
HASTAID_SCHEMA_PROMPT_INFO = format_columns_info_for_prompt(HASTAID_TABLE_NAME, HASTAID_COLUMNS_INFO)
HASTALAB_SCHEMA_PROMPT_INFO = format_columns_info_for_prompt(HASTALAB_TABLE_NAME, HASTALAB_COLUMNS_INFO)

# Tüm tablo bilgilerini birleştirme
FULL_SCHEMA_PROMPT = f"{HASTAID_SCHEMA_PROMPT_INFO}\n{HASTALAB_SCHEMA_PROMPT_INFO}"