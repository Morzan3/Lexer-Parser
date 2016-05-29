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

Lista możliwych nazw:
TeslaCrypt
CryptoWall
TorrentLocker
PadCrypt
Locky
CTB-Locker
FAKBEN
PayCrypt

Przykład użycia: python3 Main.py -m "Locky"

Filtrowanie po roli serwera:
-r "<rola serwera>"   //Rola serwera powinna zostać zapisana bez użycia spacji.

Możliwe parametry:
DistributionSites
BotnetC&Cs
PaymentSites

Przykład użycia: python3 Main.py -r "PaymentSite"


Możliwe jest jednoczesne filtrowanie po rodzinie zagrożenia oraz roli serwera.
Przykład użycia: python3 Main.py -m "Locky" -r "DistributionSite"



Update 29.05.2016
Początkowa strona zawierająca jedną tabelę ze wszystkimi serwerami została podzielona na 11 pod-stron.
W celu pobrania N-tej strony należy zmodyfikować 9 linię pliku Main.py:
    url = "http://ransomwaretracker.abuse.ch/tracker/page/N/" gdzie N to numer naszej żądanej strony.
