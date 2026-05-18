## Kamień Milowy 4 - Ocena wyników modelu i optymalizacja

### 1. Końcowa ewaluacja na zbiorze testowym
* **Zbiór danych:** Do testów wykorzystano wyizolowany w fazie preprocessingu zbiór testowy, zawierający **424 182 próbki** ruchu sieciowego, którego modele wcześniej nie "widziały".
* **Porównanie modeli:** Oba wytrenowane algorytmy uzyskały skuteczność (accuracy) bliską perfekcji: Random Forest (99,90%) oraz XGBoost (99,92%).

### 2. Analiza kluczowych metryk NIDS
Ogólna dokładność nie jest miarodajna ze względu na wysoką dysproporcję klas. Szczegółowej ocenie poddano wskaźniki krytyczne dla systemów klasy IDS:
* **Random Forest (Baseline):** Wygenerował 379 fałszywych alarmów (FPR: ~0,11%) oraz przeoczył 44 ataki (FNR: ~0,05%).
* **XGBoost (Main model):** Wygenerował zaledwie **306 fałszywych alarmów** (FPR: ~0,08%) i przeoczył tylko **26 ataków** (FNR: ~0,03%), stając się bezdyskusyjnym zwycięzcą testów.

### 3. Optymalizacja progu decyzyjnego (Threshold Tuning)
* **Problem:** Zgodnie z celami projektu, konieczna jest drastyczna redukcja zjawiska *alert fatigue* (zmęczenia fałszywymi alarmami).
* **Rozwiązanie:** Wykorzystano krzywą Precision-Recall (PR Curve) do analizy predykcji i znalezienia optymalnego punktu odcięcia prawdopodobieństwa (domyślnie jest to 0.50).
* **Wynik:** Wyliczono, że osiągnięcie precyzji na wyśrubowanym poziomie **99,90%** (minimalizacja fałszywych alarmów niemal do zera) wymaga podniesienia progu decyzyjnego z `0.50` aż do **`0.9942`**. Przy tak rygorystycznej polityce model wciąż zachowuje wysoce zadowalającą czułość (Recall) wynoszącą **97,32%**.

### 4. Ważność cech (Feature Importance)
Ewaluacja wewnętrznych wag modelu XGBoost (Relative Importance Score) potwierdziła logikę algorytmu z perspektywy inżynierii sieciowej. Pięć najważniejszych cech decyzyjnych to:
1. **Bwd Packet Length Min (47,39%):** Identyfikacja małych, powtarzalnych pakietów (cecha typowa dla zautomatyzowanych skanerów i ataków brute-force).
2. **Subflow Fwd Packets (30,97%):** Detekcja anomalii wolumetrycznych w podprzepływach (wskazówka dla ataków DDoS oraz *flooding*).
3. **PSH Flag Count (7,60%):** Wykrywanie nadużyć flagi PUSH w nagłówku TCP, często wykorzystywanej przez malware wymuszający szybką obsługę pakietu.
4. **Init_Win_bytes_backward (4,31%):** Weryfikacja rozmiaru początkowego okna TCP, demaskująca unikalne sygnatury narzędzi hakerskich (np. Nmap).
5. **Packet Length Variance (1,79%):** Odchylenie standardowe długości pakietu (naturalny ruch użytkowników ma dużą wariancję, automatyczne boty - niemal zerową).

### 5. Wybór ostatecznego modelu
Ostatecznym wyborem do wdrożenia produkcyjnego jest **XGBoost**. Charakteryzuje się najwyższą skutecznością predykcji, najkrótszym czasem inferencji oraz wysoką elastycznością konfiguracyjną (Threshold Tuning). Cechy, na których opiera decyzje, dowodzą, że model uczy się faktycznych wzorców zagrożeń, a nie rynkowego szumu.