# nids

## Kamienie milowe

### 1. Określenie tematu i celu projektu, analiza wymagań
* **Opis:** Zdefiniowanie celu projektu, którym jest stworzenie systemu NIDS (Network Intrusion Detection System) opartego na sztucznej inteligencji. System ma klasyfikować ruch sieciowy jako "normalny" lub "atak" na podstawie metadanych połączeń. Określenie wymagań technologicznych (Python, biblioteki ML, opcjonalnie klient w C++) oraz zdefiniowanie problemu wysokiego odsetka fałszywych alarmów (False Positives) w cyberbezpieczeństwie.
* **Oczekiwany wynik:** Dokumentacja początkowa projektu, zdefiniowanie architektury systemu, wybór i uzasadnienie użycia publicznego zbioru danych o ruchu sieciowym (np. CICIDS2017).

### 2. Zbiór danych i ich przygotowanie
* **Opis:** Pozyskanie wybranego zbioru danych. Przeprowadzenie analizy eksploracyjnej (EDA). Czyszczenie danych (usunięcie wartości pustych i nieskończoności), normalizacja danych numerycznych (np. rozmiarów pakietów) oraz kodowanie wartości kategorialnych (np. protokołów sieciowych). Wybór najważniejszych cech (Feature Selection), które mają największy wpływ na detekcję ataków.
* **Oczekiwany wynik:** Przygotowany, wyczyszczony i zoptymalizowany zbiór danych, podzielony na zestaw treningowy, walidacyjny i testowy, gotowy do zasilenia modeli AI.

### 3. Wybór i implementacja modelu AI
* **Opis:** Implementacja co najmniej dwóch różnych podejść do klasyfikacji: klasycznego algorytmu uczenia maszynowego (np. Random Forest lub XGBoost). Prototypowanie i trenowanie modeli na przygotowanych danych treningowych.
* **Oczekiwany wynik:** Zbudowane, wytrenowane i zapisane modele AI (pliki z wagami modeli) gotowe do procesu ewaluacji.

### 4. Ocena wyników modelu i optymalizacja
* **Opis:** Przetestowanie modeli na zbiorze testowym. Porównanie wyników przy użyciu metryk kluczowych w cyberbezpieczeństwie. Optymalizacja najlepszego modelu poprzez dostosowanie hiperparametrów, aby zmaksymalizować wykrywalność ataków przy minimalizacji fałszywych alarmów.
* **Oczekiwany wynik:** Raport z wynikami badawczymi, porównanie skuteczności i wydajności modeli oraz wybór jednego, najbardziej optymalnego modelu AI.

### 5. Wdrożenie modelu i monitorowanie
* **Opis:** Przeniesienie wybranego modelu do środowiska uruchomieniowego poprzez stworzenie prostego interfejsu API (np. z użyciem biblioteki FastAPI). Stworzenie skryptu lub klienta (np. w C++), który symuluje wysyłanie parametrów pojedynczego połączenia sieciowego do API i odbiera werdykt systemu (predykcję modelu).
* **Oczekiwany wynik:** Działający lokalnie prototyp systemu detekcji, zdolny do przyjmowania zapytań i klasyfikowania ruchu sieciowego przy wykorzystaniu wytrenowanego modelu AI w czasie zbliżonym do rzeczywistego.
