## Kamień Milowy 2 - Przygotowanie danych

### 1. Pozyskanie i wstępne ładowanie danych
* **Źródło:** Zbiór danych CICIDS2017 (8 plików CSV).
* **Metoda:** Automatyczne połączenie wszystkich dzienników ruchu sieciowego przy użyciu bibliotek `glob` i `pandas`.
* **Wynik:** Skonsolidowana ramka danych zawierająca **2 827 876 wierszy** i **79 kolumn**.

### 2. Czyszczenie danych
* **Usuwanie spacji:** Nazwy wszystkich cech zostały oczyszczone ze zbędnych spacji (np. zamiana `' Destination Port'` na `'Destination Port'`), co zapobiega błędom odwołań w kodzie.
* **Wartości puste (NaN):** Zidentyfikowano i usunięto 1358 wierszy zawierających brakujące dane.
* **Wartości nieskończone (Inf):** 4376 wierszy z wartościami `Infinity` (powstałymi głównie przez dzielenie przez zero w statystykach przepływu) zastąpiono wartościami `NaN`, a następnie usunięto.
* **Ostateczny zbiór:** **2 827 876 próbek** z poprawnymi danymi numerycznymi.

### 3. Eksploracyjna Analiza Danych
* **Rozkład klas:** Analiza wykazała znaczną dysproporcję klas (Class Imbalance):
    * **Ruch bezpieczny (Benign):** ok. 2.27 mln próbek (80.4%).
    * **Ruch złośliwy (Attack):** ok. 0.56 mln próbek (19.6%).
* **Inżynieria etykiet:** Wieloklasowe etykiety ataków zostały zmapowane na klasyfikację binarną: `0` dla ruchu bezpiecznego i `1` dla wszystkich rodzajów ataków.

### 4. Podział i Przetwarzanie Danych
* **Proporcje podziału:** Dane podzielono na zbiory: **Treningowy (70%)**, **Walidacyjny (15%)** oraz **Testowy (15%)**.
* **Stratyfikacja:** Zastosowano parametr `stratify`, aby zachować proporcję 19.6% ataków w każdym z trzech podzbiorów.
* **Normalizacja:** Wykorzystano `StandardScaler` do standaryzacji cech numerycznych. Skaler został dopasowany (fit) wyłącznie do zbioru treningowego, aby uniknąć wycieku danych (Data Leakage).

### 5. Wybór cech
* **Algorytm:** Zastosowano model Random Forest Importance z 500 drzewami decyzyjnymi o maksymalnej głębokości 30.
* **Kluczowe zidentyfikowane cechy:**
    1.  `Destination Port` (kluczowe dla wykrywania usług, w które celuje atak).
    2.  `Average Packet Size` (wskaźnik typowy dla ataków wolumetrycznych DDoS).
    3.  `Init_Win_bytes_forward/backward` (analiza okna TCP pozwalająca wykryć specyficzne narzędzia hakerskie).
* **Optymalizacja:** Zredukowano przestrzeń cech z 78 do **40 najważniejszych kolumn**, co przyspieszy trenowanie i poprawi zdolność modelu do generalizacji.

### 6. Persystencja danych
* **Format zapisu:** Gotowe zbiory danych zostały zarchiwizowane w formacie binarnym przy użyciu biblioteki `joblib`.
* **Lokalizacja:** `data/processed/`.