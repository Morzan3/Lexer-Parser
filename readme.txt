Program dokonujący analizy lexykalner oraz składniowej pliku html strony http://ransomwaretracker.abuse.ch/tracker/.
Po dokonaniu analizy program zapisuje informacje (datę dodania, rolę serwera, rodzinę malwaru, adres hosta oraz adres ip)
o wybranych serwerach do pliku w formacie JSON.

Uruchomienie:
Program uruchamiany bez podania żadnych parametrów (komenda: python3 Main.py) ściąga wszystkie informację ze wspomnianej
wcześniej strony bez ich filtrowania.

Możliwe jest również filtrowanie wyników przy użyciu odpowiednej flagi.

Filtrowanie po rodzinie złośliwego oprogramowania:
-m "<Nazwa rodziny>"

W przypadku błędnego podania nazwy lub podania nazwy, która nie występuje na stronie żadne informacje nie zostaną zapisane do pliku.
Filtrowanie tylko po jednej nazwie naraz jest możliwe.

Poglądowa lista obecnie możliwych nazw (tych, które znajdują się na stronie, w przypadku dodania nowych filtrowanie po nich jest również możliwe):
"TeslaCrypt"
"CryptoWall"
"TorrentLocker"
"PadCrypt"
"Locky"
"CTB-Locker"
"FAKBEN"
"PayCrypt"

Przykład użycia: python3 Main.py -m "Locky"

Filtrowanie po roli serwera:
-r "<rola serwera>"   //Rola serwera powinna zostać zapisana dokładnie tak jak na stronie internetowej.

Możliwe parametry:
"Distribution Sites"
"Botnet C&C"
"Payment Sites"

Przykład użycia: python3 Main.py -r "PaymentSite"


Możliwe jest jednoczesne filtrowanie po rodzinie zagrożenia oraz roli serwera.
Przykład użycia: python3 Main.py -m "Locky" -r "Distribution Site"

Zmiana nazwy pliku wynikowego:

Dodano możliwość zmiany nazwy pliku wynikowego po użyciu flagi -o (od output file), po której wpisujemy wybraną
przez nas nazwę pliku wynikowego w taki sposób w jaki wcześniej pisaliśmy rolę serwera lub rodzinę malware'u.
W przypadku nie użycia flagi wynik zostanie zapisany w domyślnym pliku "Lista serwerow.txt"

Przykład użycia: python3 Main.py -o "Output file"


Liczba pobieranych stron:
Domyślnie pobierana jest jedynie zerowa strona tabeli znajdująca się na stronie "https://ransomwaretracker.abuse.ch/tracker/"
posiadająca najnowsze serwery. Strona ta nie jest uwzględniona w numeracji tabli znajdującej się na dole strony.
W przypadku gdy chcemy pobrać starsze strony należy użyć flagi -n a następnie podać liczbę stron wg. numeracji na dole strony.
Tak więc w przypadku użycia flagi z parametrem 1 pobrana zostanie strona 0 (pobierana zawsze) oraz pierwsza strona tabeli.

Przykład użycia: python3 Main.py -n 11 -m "Locky" -r "Botnet C&C"


Uwaga:
Użycie flagi bez późniejszego podania parametru prowadzi do błędnych wyników programu lub wygenerowania odpowiedniej wiadomości
o błędzie.



Update 29.05.2016
Początkowa strona zawierająca jedną tabelę ze wszystkimi serwerami została podzielona na 11 pod-stron.
W celu pobrania N-tej strony należy zmodyfikować 9 linię pliku Main.py:
    url = "http://ransomwaretracker.abuse.ch/tracker/page/N/" gdzie N to numer naszej żądanej strony.

Update 1.06.2016
Program pobiera i parsuje 12 oddzielnych plików HTML, które składają się na całość tabeli.
Z powodu ilości stron zajmuje to jednak trochę czasu.

Update 04.06.2016
Program pobiera określoną przez użytkownika liczbę stron tabeli + pierwszą domyślną nie uwzględnioną na stronie internetowej przy numeracji tabeli.

Update 09.06.2016
Dodano opcjonalne flagi. Patrz sekcja uruchomienie.