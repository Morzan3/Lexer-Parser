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
Filtrowanie tylko po jednej rodzinie złośliwego oprogramowania naraz jest możliwe.

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
-r "<rola serwera>"   

Możliwe parametry (te, które znajdują się na stronie, w przypadku dodania nowych filtrowanie po nich jest również możliwe):
"Distribution Sites"
"Botnet C&C"
"Payment Sites"

Przykład użycia: python3 Main.py -r "PaymentSite"

Możliwe jest jednoczesne filtrowanie po rodzinie zagrożenia oraz roli serwera.
Przykład użycia: python3 Main.py -m "Locky" -r "Distribution Site"


Update 29.05.2016
Początkowa strona zawierająca jedną tabelę ze wszystkimi serwerami została podzielona na 11 pod-stron.
W celu pobrania N-tej strony należy zmodyfikować 9 linię pliku Main.py:
    url = "http://ransomwaretracker.abuse.ch/tracker/page/N/" gdzie N to numer naszej żądanej strony.

Update 1.06.2016
Program pobiera i parsuje 12 oddzielnych plików HTML, które składają się na całość tabeli.
Z powodu ilości stron zajmuje to jednak trochę czasu.

Update 04.06.2016
Program pobiera określoną przez użytkownika liczbę stron tabeli + pierwszą domyślną nie uwzględnioną na stronie internetowej przy numeracji tabeli.
