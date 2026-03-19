## 1. Definicja Problemu i Cel Projektu
Tradycyjne systemy wykrywania intruzów (NIDS) opierają się na statycznych regułach i sygnaturach. Ich główną wadą jest generowanie ogromnej liczby fałszywych alarmów.

**Cel projektu:** Stworzenie systemu NIDS wykorzystującego algorytmy uczenia maszynowego do klasyfikacji ruchu sieciowego jako "normalny" lub "atak". System będzie analizował metadane połączeń sieciowych, co pozwala na zachowanie prywatności (brak deszyfrowania payloadu pakietów) i szybką detekcję. Głównym celem optymalizacyjnym jest maksymalizacja wykrywalności ataków przy jednoczesnym drastycznym ograniczeniu fałszywych alarmów.

## 2. Wybór Zbioru Danych (Dataset)
Do treningu i ewaluacji modelu wybrany został zbiór **[CICIDS2017](https://www.kaggle.com/datasets/kk0105/cicids2017)** (Canadian Institute for Cybersecurity). 

**Uzasadnienie wyboru:**
* Zbiór ten zawiera odzwierciedlenie nowoczesnych wektorów ataków (m.in. DDoS, Brute Force, Web Attacks, Infiltration, Botnet).
* Zawiera realistyczny "ruch tła", co jest kluczowe do nauki wzorców normalnego zachowania użytkowników.
* Zamiast surowych plików PCAP, dostarcza gotowe, wyekstrahowane cechy przepływów sieciowych

## 3. Architektura Systemu (High-Level)
System będzie składał się z następujących etapów:
1. **Pobranie danych:** Odbiór wektora cech (metadanych) pojedynczego połączenia sieciowego.
2. **Preprocessing:** Czyszczenie braków, normalizacja wartości numerycznych i kodowanie protokołów do formatu zrozumiałego dla modelu, zgodnie z wyuczonymi parametrami.
3. **Predykcja:** Przepuszczenie wektora przez wytrenowany model klasyfikacyjny.
4. **Werdykt:** Zwrócenie przez API odpowiedzi klasyfikującej połączenie z odpowiednim prawdopodobieństwem (Atak vs Normalny ruch).

## 4. Podejście algorytmiczne

Ponieważ analizowane dane mają strukturę tabelaryczną (wyliczone statystyki przepływów), projekt oprze się na uczeniu nadzorowanym w celu rozwiązania problemu klasyfikacji binarnej. Zamiast sieci neuronowych, wykorzystane zostaną wydajne algorytmy zespołowe oparte na drzewach decyzyjnych, takie jak XGBoost.

## 5. Wymagania Technologiczne
* **Język:** Python 3.9+
* **Analiza i obróbka danych:** `pandas`, `numpy`
* **Wizualizacja:** `matplotlib`, `seaborn`
* **Uczenie maszynowe:** `scikit-learn`, `xgboost`
* **Wdrożenie i API:** `FastAPI`, `uvicorn`
