import sys
import requests
from lexer import *
from Parser import *
sys.setrecursionlimit(28500)


def get_web_content():
    url = "http://ransomwaretracker.abuse.ch/tracker/"
    r = requests.get(url)
    file_lines = []
    string = ""

    for line in r.text:
        string = string + line
        if line == chr(10):
            file_lines.append(string)
            string = ""
    return file_lines

def get_file_content():
    arguments = []
    for arg in sys.argv:
        arguments.append(arg)


    # if len(arguments) != 2:
    #     sys.exit("Nie została podana sciezka do pliku lub zostala podana niepoprawnie")

    #file_path = arguments[1]
    file_path = 'html_file2.html'
    html_file = open(file_path, 'r')

    file_lines = []
    for line in html_file:
        file_lines.append(line)

    return file_lines

output_file = open('outputfile.txt', 'w')


file = get_file_content()
#file = get_web_content()

lexer = Lexer(file)

parser = Parser(lexer)
parser.start()

# #while True:
# for i in range(0, 207):
#   if lexer.return_next_token.type == TokenType.end_of_file:
#       break

lexer.print_tags()
for line in lexer.token_list:
    output_file.write(line.type.name + ' ' + line.value + '\n')

output_file.close()