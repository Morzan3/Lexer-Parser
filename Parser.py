import sys
from lexer import *

class Parser:
    def __init__(self, lexer, malware_family_filter, server_role_filter):
        self.lexer = lexer
        self.current_token = None
        self.recent_tokens = []
        self.servers = []
        self.malware_family = malware_family_filter
        self.server_role = server_role_filter

    def start(self):
        self.current_token = self.lexer.return_next_token
        self.add_token_to_token_list(self.current_token)
        if not(self.checkIfTokenExpected(TokenType.doctype)):
            raise SystemExit
        self.current_token = self.lexer.return_next_token
        while self.current_token.type != TokenType.end_of_file:
            self.tag()

    def tag(self):
        self.check_to_clear()
        self.check_token_order()
        if self.current_token.type == TokenType.opening_end_tag:
            self.add_token_to_token_list(self.current_token)
            self.current_token = self.lexer.return_next_token
            self.add_token_to_token_list(self.current_token)
            if not(self.checkIfTokenExpected(TokenType.text)):
                raise SystemExit
            self.current_token = self.lexer.return_next_token
            self.add_token_to_token_list(self.current_token)
            if not (self.checkIfTokenExpected(TokenType.close_tag)):
                raise SystemExit
            self.tag_closure()
            return
        elif self.checkIfTokenExpected(TokenType.opening_tag, " or opening end_tag_expected"):
            self.add_token_to_token_list(self.current_token)
            self.current_token = self.lexer.return_next_token
            self.add_token_to_token_list(self.current_token)
            if not(self.checkIfTokenExpected(TokenType.text)):
                raise SystemExit
            self.current_token = self.lexer.return_next_token
            self.add_token_to_token_list(self.current_token)
            self.attributes()
            self.tag_closure()
            return
        print("Unexpected token occured. Token occured: ", self.current_token.type, "Token expected: opening_end_tag or opening_tag")
        sys.exit()

    def tag_closure(self):
        if self.current_token.type == TokenType.close_tag or self.current_token.type == TokenType.close_end_tag:
            self.current_token = self.lexer.return_next_token
            if self.current_token.type == TokenType.text:
                self.add_token_to_token_list(self.current_token)
                self.current_token = self.lexer.return_next_token
                return
            elif self.current_token.type == TokenType.opening_tag or self.current_token.type == TokenType.opening_end_tag:
                return
            elif self.current_token.type == TokenType.end_of_file:
                self.check_token_order()
                print("Natrafiono na koniec pliku, parsowanie zakończono powodzeniem")
                return
            print("Unexpected token occured. Token occured: ", self.current_token.type.name, "Token expected: text or opening tag or opening end_tag")
            sys.exit()
        print("Unexpected token occured. Token occured: ", self.current_token.type.name, "Token expected: close_tag")
        sys.exit()


    def attributes(self):
        while self.current_token.type == TokenType.text:
            self.attribute()

    def attribute(self):
        if self.checkIfTokenExpected(TokenType.text):
            self.current_token = self.lexer.return_next_token
            self.add_token_to_token_list(self.current_token)
            self.checkIfTokenExpected(TokenType.equal_sign)
            self.current_token = self.lexer.return_next_token
            self.add_token_to_token_list(self.current_token)
            self.checkIfTokenExpected(TokenType.quotation_mark)
            self.current_token = self.lexer.return_next_token
            self.add_token_to_token_list(self.current_token)
            self.checkIfTokenExpected(TokenType.text)
            self.current_token = self.lexer.return_next_token
            self.add_token_to_token_list(self.current_token)
            self.checkIfTokenExpected(TokenType.quotation_mark)
            self.current_token = self.lexer.return_next_token
            self.add_token_to_token_list(self.current_token)


    def checkIfTokenExpected(self, expected_token_type, optional_message=''):
         if self.current_token.type != expected_token_type:
             error_message = "Unexpected token occured"
             error_message = error_message + " Token occured: " + self.current_token.type.name
             error_message = error_message + " Token expected: " + expected_token_type.name
             error_message = error_message + optional_message
             error_message = error_message + "\nFile line number: " + str(self.current_token.line_number + 1) + " Token char number: " + str(self.current_token.line_char_number + 1)
             print(error_message)
             raise SystemExit
         return True


    def check_to_clear(self):
        if self.recent_tokens[-1].type == TokenType.close_tag and self.recent_tokens[-2].value == 'tr' and self.recent_tokens[-3].type == TokenType.opening_end_tag:
            if self.recent_tokens[-4].type == TokenType.close_tag and self.recent_tokens[-5].value == 'th' and self.recent_tokens[-6].type == TokenType.opening_end_tag:
                self.recent_tokens = []

    def add_token_to_token_list(self, token):
        if len(self.recent_tokens) == 512:
            self.recent_tokens.pop(0)
            self.recent_tokens.append(token)
        else:
            self.recent_tokens.append(token)

    def check_token_order(self):
        if len(self.recent_tokens) > 4:
            if self.recent_tokens[0].type == TokenType.opening_tag and self.recent_tokens[1].value == 'tr' and self.recent_tokens[2].type == TokenType.close_tag:
                if self.recent_tokens[4].value != 'th':
                    if self.recent_tokens[-1].type == TokenType.close_tag and self.recent_tokens[-2].value == 'tr' and self.recent_tokens[-3].type == TokenType.opening_end_tag:
                        new_server = self.extract_information()
                        if new_server != None:
                            self.servers.append(new_server)
                        self.recent_tokens = []


    def extract_information(self):
        token_number = len(self.recent_tokens)
        i = 0
        current_column = 1
        tokens_with_information = []
        while i < token_number:
            if self.recent_tokens[i].type == TokenType.opening_tag and self.recent_tokens[i+1].value == 'td' and self.recent_tokens[i+2].type == TokenType.close_tag:
                if current_column == 1:
                    tokens_with_information.append(self.recent_tokens[i+3])
                    i = i + 4
                    current_column += 1
                    continue
                if current_column == 2:
                    for j in range(i+4, len(self.recent_tokens)):
                        if self.recent_tokens[j].type == TokenType.close_tag:
                            if self.server_role == "":
                                tokens_with_information.append(self.recent_tokens[j+1])
                                i = j + 2
                                current_column += 1
                                break
                            elif self.recent_tokens[j+1].value == self.server_role:
                                tokens_with_information.append(self.recent_tokens[j+1])
                                i = j + 2
                                current_column += 1
                                break
                            else:
                                return None
                    continue
                if current_column == 3:
                    for j in range(i+4, len(self.recent_tokens)):
                        if self.recent_tokens[j].type == TokenType.close_tag:
                            if self.malware_family == "":
                                tokens_with_information.append(self.recent_tokens[j + 1])
                                i = j + 2
                                current_column += 1
                                break
                            elif self.recent_tokens[j + 1].value == self.malware_family:
                                tokens_with_information.append(self.recent_tokens[j + 1])
                                i = j + 2
                                current_column += 1
                                break
                            else:
                                return None
                    continue
                if current_column == 4:
                    for j in range(i+4, len(self.recent_tokens)):
                        if self.recent_tokens[j].value == 'href':
                            tokens_with_information.append(self.recent_tokens[j + 3])
                            i = j + 4
                            current_column += 1
                            break
                    continue
                if current_column == 5:
                    current_column += 1
                    i +=1
                    continue
                if current_column == 6:
                    tokens_with_information.append(self.recent_tokens[i + 3])
                    return Server(tokens_with_information)
            i += 1


class Server:
    def __init__(self, tokens):
        self.date = tokens[0].value
        self.server_role = tokens[1].value
        self.malware_family = tokens[2].value
        self.host_adress = tokens[3].value
        self.ip_adress = tokens[4].value
        if self.ip_adress[-1] == '(':
            self.ip_adress = self.ip_adress[0:len(self.ip_adress)-1]
        if self.ip_adress[-1] == ' ':
            self.ip_adress = self.ip_adress[0:len(self.ip_adress)-1]


