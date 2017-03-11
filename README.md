# Lexer/Parser
Program written for "Compilation techniques" subject which taks is to make leixcal analysis and parsing of the html file found on the page:
http://ransomwaretracker.abuse.ch/tracker/

After analysis program is saves information about selected servers to a file in JSON format.


## Getting Started

```
$ git clone https://github.com/Morzan3/Lexer-Parser
$ cd Lexer-Parser
```

## Running the program
Program runn without any parameters will download all of the information from the mentioned website.

```
python3 Main.py
```

It is also possible to filter the result using selected flags.

Filtering based on the malware family by using "-m" flag

```
-m "<malware family>"
```

In case of false name no information will be saved.
Only one family at the time can be filtered.

List of possible malware families:
"TeslaCrypt"
"CryptoWall"
"TorrentLocker"
"PadCrypt"
"Locky"
"CTB-Locker"
"FAKBEN"
"PayCrypt"

```
python3 Main.py -m "Locky"
```

Filtering based on the server role by using "-r" flag

```
-r "<server role>"
```
List of possible server roles :

"Distribution Sites"
"Botnet C&C"
"Payment Sites"

```
python3 Main.py -r "PaymentSite"
```

It is possible to filter by the malware family and server role at the same time:

```
python3 Main.py -m "Locky" -r "Distribution Site"
```

It is possible to change the nape of the output file by using "-o" flag:

```
python3 Main.py -o "Output file"
```

## Authors

* **Ignacy Ślusarczyk** - [Morzan3](https://github.com/Morzan3)


## Notes

The project is no longer updated.
