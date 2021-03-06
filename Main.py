import requests
from lexer import *
from Parser import *

malware_family_filter = ""
server_role_filter = ""
number_of_pages = 0
output_file_name = "Lista serwerow.txt"

def check_filtration():
    global malware_family_filter , server_role_filter, number_of_pages, output_file_name
    arguments = []

    for arg in sys.argv:
        arguments.append(arg)

    if len(arguments) > 1:
        i = 0
        try :
            while i < len(arguments):
                if arguments[i] == '-m':
                    malware_family_filter = arguments[i+1]
                    i += 2
                    continue
                if arguments[i] == '-r':
                    server_role_filter = arguments[i+1]
                    i += 2
                    continue
                if arguments[i] == '-n':
                    number_of_pages = int(arguments[i+1])
                    i += 2
                    continue
                if arguments[i] == '-o':
                    output_file_name = arguments[i+1]
                    i += 2
                    continue
                i += 1
        except IndexError:
            print("Podano bledne parametry wywolania programu")
            sys.exit()


def convert_role(server_role):
    if server_role == "":
        return server_role
    if server_role == "Botnet C&C":
        server_role = "Botnet C&amp;C"
        return server_role
    else:
        return server_role


def get_web_content(url):
    r = requests.get(url)
    file_lines = []
    string = ""

    for line in r.text:
        string = string + line
        if line == chr(10):
            file_lines.append(string)
            string = ""
    return file_lines


def get_specific_number_of_pages():
    global server_role_filter
    global malware_family_filter
    servers = []
    check_filtration()

    for page_number in range(0,int(number_of_pages) + 1):

        if page_number == 0:
            url = "http://ransomwaretracker.abuse.ch/tracker/"
        else:
            url = "http://ransomwaretracker.abuse.ch/tracker/page/"
            url = url + str(page_number) + "/"
        file = get_web_content(url)
        lexer = Lexer(file)

        server_role_filter = convert_role(server_role_filter)

        parser = Parser(lexer, malware_family_filter, server_role_filter)
        parser.start()

        if page_number == 0:
            servers = parser.servers
        else:
            servers = servers + parser.servers

    output_file = open(output_file_name, 'w')
    output_file.write('{"Serwers":[\n')
    for n, line in enumerate(servers):
        if n == len(servers) - 1:
            output_file.write(
                '{"addingDate":"' + line.date + '","serverRole":"' + line.server_role + '","malwareFamily":"' + line.malware_family + '","hostAdress":"' + line.host_adress + '","ipAdress":"' + line.ip_adress + '"}\n')
        else:
            output_file.write(
                '{"addingDate":"' + line.date + '","serverRole":"' + line.server_role + '","malwareFamily":"' + line.malware_family + '","hostAdress":"' + line.host_adress + '","ipAdress":"' + line.ip_adress + '"},\n')
    output_file.write(']}')
    output_file.close()


def get_file_content():
    arguments = []
    for arg in sys.argv:
        arguments.append(arg)


    file_path = arguments[1]
    html_file = open(file_path, 'r')

    file_lines = []
    for line in html_file:
        file_lines.append(line)

    return file_lines



get_specific_number_of_pages()

