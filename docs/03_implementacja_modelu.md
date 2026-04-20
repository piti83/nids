## Kamień Milowy 3 - Wybór i implementacja modelu AI

### 1. Przygotowanie środowiska i danych
* **Dane wejściowe:** Wykorzystano zbiory przetworzone w poprzednim etapie: treningowy (1 979 513 próbek) oraz walidacyjny (424 181 próbek).
* **Cechy:** Modele trenowano na zredukowanym zestawie 40 kluczowych cech wyselekcjonowanych algorytmem Random Forest Importance.

### 2. Model bazowy (Baseline) - Random Forest
* **Konfiguracja:** Zastosowano klasyfikator lasów losowych z 100 drzewami decyzyjnymi i parametrem `class_weight='balanced'`, aby zneutralizować wpływ dysproporcji klas.
* **Wydajność:** Proces trenowania trwał **171,70 sekundy**.
* **Wyniki:** Model uzyskał niemal idealne wyniki w raporcie klasyfikacji (F1-score: 1.00), stanowiąc solidny punkt odniesienia dla dalszych prac.

### 3. Model docelowy - XGBoost
* **Konfiguracja:** Wykorzystano algorytm gradientowego wzmacniania drzew (XGBoost) z 200 estymatorami i maksymalną głębokością drzewa wynoszącą 10.
* **Optymalizacja czasu:** Mimo większej złożoności, XGBoost uczył się szybciej od modelu bazowego, kończąc proces w **133,79 sekundy**.
* **Zarządzanie dysproporcją:** Zastosowano parametr `scale_pos_weight = 4.08`, wyliczony automatycznie jako stosunek liczby próbek bezpiecznych do złośliwych.

### 4. Wstępna ocena wyników (Zbiór walidacyjny)
Podczas wstępnej ewaluacji modelu XGBoost skupiono się na dwóch kluczowych metrykach dla systemów NIDS:
* **Czułość (Recall): 99,98%** – model wykrył niemal wszystkie ataki obecne w zbiorze walidacyjnym, minimalizując ryzyko przeoczenia zagrożenia.
* **Precyzja (Precision): 99,56%** – system charakteryzuje się bardzo niskim odsetkiem fałszywych alarmów, co było jednym z głównych celów projektu.

### 5. Persystencja modeli
* **Zapis binarny:** Model Random Forest został zarchiwizowany przy użyciu biblioteki `joblib` jako `random_forest_v1.joblib`.
* **Format natywny:** Model XGBoost zapisano w wydajnym formacie JSON (`xgboost_v1.json`), co umożliwi jego szybkie ładowanie w środowisku produkcyjnym (API).