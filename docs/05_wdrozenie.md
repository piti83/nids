## Kamień Milowy 5 - Wdrożenie modelu i monitorowanie

### 1. Architektura produkcyjna systemu (High-Level)
W ramach ostatniego etapu projektu, wytrenowany i zoptymalizowany model **XGBoost** został przeniesiony ze środowiska badawczego (Jupyter Notebook) do działającego środowiska uruchomieniowego (API). Prototyp systemu detekcji intruzów (NIDS) został zaprojektowany w architekturze klient-serwer:
* **Serwer produkcyjny NIDS (FastAPI):** Odpowiada za przyjmowanie żądań sieciowych, walidację danych wejściowych, uruchamianie silnika predykcyjnego oraz zwracanie werdyktu w czasie rzeczywistym.
* **Klient / Czujnik sieciowy (Symulator):** Skrypt symulujący agenta monitorującego ruch sieciowy, który pobiera metadane połączeń, formatuje je i przesyła do analizy przez API.

### 2. Implementacja Serwera API (`main.py`)
Do stworzenia interfejsu programistycznego wykorzystano nowoczesny, asynchroniczny framework **FastAPI** oraz serwer **Uvicorn**. Główne założenia implementacyjne:
* **Ładowanie modelu w pamięci (In-Memory Inference):** Model XGBoost jest wczytywany z formatu binarnego JSON (`xgboost_v1.json`) tylko raz – podczas startu serwera. Zapobiega to kosztownemu narzutowi I/O przy każdym zapytaniu i umożliwia obsługę żądań z minimalną latencją.
* **Walidacja danych przy użyciu Pydantic:** Zdefiniowano ścisły model danych wejściowych (`NetworkFlow`), który weryfikuje, czy przesyłany wektor cech zawiera dokładnie **40 znormalizowanych kolumn** wyselekcjonowanych na wcześniejszych etapach projektu. Zapobiega to awariom silnika predykcyjnego.
* **Zastosowanie Zoptymalizowanego Progu:** Wewnątrz endpointu `/predict` zaimplementowano logikę opartą na metodzie `predict_proba()`. Zamiast domyślnego progu odcięcia (0.50), zastosowano wyznaczony w Kamieniu Milowym 4 optymalny próg **`0.9942`**. Pozwala to na niemal całkowite wyeliminowanie fałszywych alarmów (FPR), co było głównym celem biznesowym projektu.

### 3. Implementacja Klienta Symulacyjnego (`client.py`)
W celu weryfikacji działania systemu w warunkach zbliżonych do rzeczywistych, stworzono skrypt klienta, który:
* Wczytuje nieużywany wcześniej w procesie produkcyjnym zbiór testowy (`test_data.joblib`).
* Losuje próbki reprezentujące zarówno ruch bezpieczny (**BENIGN**), jak i nowoczesne wektory ataków (**ATTACK**).
* Miesza wybrane próbki w losowej kolejności, a następnie cyklicznie (w odstępach 1.5 sekundy) wysyła je za pomocą żądań HTTP POST na endpoint serwera.

### 4. Weryfikacja Działania i Wyniki Monitorowania
Testy integracyjne przeprowadzone lokalnie na systemie Arch Linux zakończyły się pełnym sukcesem, wykazując następujące parametry operacyjne:
* **Poprawność klasyfikacji:** Serwer poprawnie zidentyfikował wszystkie przesłane anomalie oraz ruch prawidłowy. Zoptymalizowany próg decyzyjny skutecznie odseparował ataki od ruchu tła, zwracając status `[MATCH]` we wszystkich testowych scenariuszach.
* **Czas odpowiedzi (Latencja API):** Czas potrzebny na odebranie żądania, konwersję danych, predykcję modelu XGBoost i zwrot odpowiedzi wyniósł średnio **od 1.5 do 3.5 milisekundy**. Wynik ten potwierdza zdolność systemu do pracy w czasie zbliżonym do rzeczywistego (real-time) i obsługi potoków danych o dużym natężeniu.

### 5. Podsumowanie Projektu
Projekt budowy systemu NIDS opartego na sztucznej inteligencji został w pełni zrealizowany w obrębie wszystkich 5 zaplanowanych kamieni milowych:
1.  **Definicja i Architektura:** Wybrano nowoczesny zbiór CICIDS2017 odzwierciedlający realistyczne zagrożenia sieciowe.
2.  **Przygotowanie danych:** Przeprowadzono pełne czyszczenie danych (usunięcie wartości pustych, nieskończoności) oraz zaawansowaną redukcję wymiarowości z 78 do 40 kluczowych cech za pomocą algorytmu Random Forest Importance.
3.  **Implementacja modeli:** Wytrenowano model bazowy (Random Forest) oraz model docelowy (XGBoost) zarządzając dysproporcją klas za pomocą wag strukturalnych (`scale_pos_weight = 4.08`).
4.  **Ocena i Optymalizacja:** Na zbiorze testowym model XGBoost okazał się bezkonkurencyjny. Poprzez Threshold Tuning (przesunięcie progu do `0.9942`) dostarczono mechanizm redukcji fałszywych alarmów (precyzja 99,90%).
5.  **Wdrożenie produkcyjne:** Stworzono stabilny i ultra-szybki mikrosegment detekcyjny w oparciu o FastAPI, gotowy do integracji z systemami klasy SIEM/SOAR w nowoczesnych centrach operacji bezpieczeństwa (SOC).
