# import streamlit as st
# import requests
# from PIL import Image
# import pandas as pd
# import time
#
# # Konfiguracja strony
# st.set_page_config(page_title="Klasyfikacja Obrazów", layout="wide", page_icon="🖼️")
#
# # Stylizacja główna
# st.markdown("""
#     <style>
#     .stApp {
#         background-color: #f5f5f5;
#     }
#     .title {
#         color: #4CAF50;
#         text-align: center;
#         font-size: 3em;
#         font-weight: bold;
#     }
#     .upload-box {
#         border: 2px dashed #4CAF50;
#         padding: 20px;
#         border-radius: 10px;
#         text-align: center;
#         background-color: #ffffff;
#     }
#     </style>
#     """, unsafe_allow_html=True)
#
# # Nagłówek aplikacji
# st.markdown('<div class="title">🎨 Klasyfikacja Obrazów</div>', unsafe_allow_html=True)
# st.write("Prześlij jedno lub więcej zdjęć, aby uzyskać klasyfikację w 4 kategoriach.")
#
# # Sekcja ładowania plików
# st.markdown('<div class="upload-box">', unsafe_allow_html=True)
# uploaded_files = st.file_uploader("Przeciągnij i upuść zdjęcia lub wybierz z dysku",
#                                   type=["jpg", "jpeg", "png"], accept_multiple_files=True)
# st.markdown('</div>', unsafe_allow_html=True)
#
#
# # Funkcja do przesyłania plików do API
# def query_api(image_file):
#     url = "https://your-api-url.com/predict"  # Zastąp własnym endpointem
#     files = {"file": image_file}
#     response = requests.post(url, files=files)
#     return response.json()
#
#
# # Sekcja wyników
# if uploaded_files:
#     st.subheader("🔄 Klasyfikacja zdjęć w toku...")
#     progress_bar = st.progress(0)
#
#     results = []
#     col1, col2 = st.columns([1, 2])  # Kolumny dla estetyki
#
#     for idx, uploaded_file in enumerate(uploaded_files):
#         # Wyświetlanie zdjęcia
#         image = Image.open(uploaded_file)
#         col1.image(image, caption=f"📷 {uploaded_file.name}", width=250)
#
#         # Symulacja ładowania (opcjonalne)
#         # time.sleep(1)
#
#         # Przesyłanie zdjęcia do API
#         with st.spinner(f"Klasyfikowanie zdjęcia: {uploaded_file.name}"):
#             try:
#                 api_response = query_api(uploaded_file)
#                 categories = api_response.get("categories", {})
#                 results.append({"Plik": uploaded_file.name, **categories})
#             except Exception as e:
#                 st.error(f"Błąd przetwarzania pliku {uploaded_file.name}: {str(e)}")
#                 results.append({"Plik": uploaded_file.name, "Błąd": "Nie udało się pobrać wyników."})
#
#         # Aktualizacja paska postępu
#         progress_bar.progress((idx + 1) / len(uploaded_files))
#
#     # Wyświetlanie wyników
#     if results:
#         st.subheader("📊 Wyniki klasyfikacji:")
#         df = pd.DataFrame(results)
#         st.table(df.style.format("{:.2%}", subset=pd.IndexSlice[:, df.columns[1:]]))

import streamlit as st
import requests
import pandas as pd
from PIL import Image
import io

# Estetyczny wygląd aplikacji
st.set_page_config(page_title="Klasyfikacja Animacji", layout="wide")

# Nagłówek
st.title("Klasyfikacja Animacji")
st.write("Prześlij jedno lub kilka zdjęć, a model zwróci prawdopodobieństwo przynależności do jednej z 4 kategorii.")

# Sekcja przesyłania zdjęć
st.subheader("1️⃣ Prześlij zdjęcia")
uploaded_files = st.file_uploader("Wybierz jedno lub więcej zdjęć...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Funkcja do przesyłania zdjęcia do API
def query_api(image_file):
    url = "https://your-api-url.com/predict"
    files = {"file": image_file}
    response = requests.post(url, files=files)
    return response.json()

# Wyświetlanie wyników
if uploaded_files:
    st.subheader("2️⃣ Wyniki klasyfikacji")
    results = []

    # Tworzenie dwóch kolumn dla estetyki
    col1, col2 = st.columns([1, 2])

    # Przetwarzanie każdego zdjęcia
    for uploaded_file in uploaded_files:
        # Wyświetlenie obrazu
        image = Image.open(uploaded_file)
        col1.image(image, caption=f"Przesłany obraz: {uploaded_file.name}", width=300)

        # Przesyłanie do API
        with st.spinner(f"Klasyfikuję zdjęcie {uploaded_file.name}..."):
            try:
                # Przekazanie pliku do API
                api_response = query_api(uploaded_file)
                categories = api_response.get("categories", {})
                results.append({"Nazwa pliku": uploaded_file.name, **categories})
            except:
                st.error("Błąd połączenia z API. Upewnij się, że API działa poprawnie.")
                results.append({"Nazwa pliku": uploaded_file.name, "Błąd": "Nie udało się pobrać danych z API."})

    # Wyświetlenie wyników jako tabela
    if results:
        st.write("### Wyniki:")
        df = pd.DataFrame(results)
        col2.table(df.style.format("{:.2%}", subset=pd.IndexSlice[:, df.columns[1:]]))
