import sys
from lexer import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def start(self):
        self.current_token = self.lexer.return_next_token
        if not(self.checkIfTokenExpected(TokenType.doctype)):
            raise SystemExit
        self.current_token = self.lexer.return_next_token
        while self.current_token.type != TokenType.end_of_file:
            self.tag()

    def tag(self):
        if self.current_token.type == TokenType.opening_end_tag:
            self.current_token = self.lexer.return_next_token
            if not(self.checkIfTokenExpected(TokenType.text)):
                raise SystemExit
            self.current_token = self.lexer.return_next_token
            if not (self.checkIfTokenExpected(TokenType.close_tag)):
                raise SystemExit
            self.tag_closure()
            return
        elif self.checkIfTokenExpected(TokenType.opening_tag, " or opening end_tag_expected"):
            self.current_token = self.lexer.return_next_token
            if not(self.checkIfTokenExpected(TokenType.text)):
                raise SystemExit
            self.current_token = self.lexer.return_next_token
            self.attributes()
            self.tag_closure()
            return
        print("Unexpected token occured. Token occured: ", self.current_token.type, "Token expected: opening_end_tag or opening_tag")
        sys.exit()

    def tag_closure(self):
        if self.current_token.type == TokenType.close_tag or self.current_token.type == TokenType.close_end_tag:
            self.current_token = self.lexer.return_next_token
            if self.current_token.type == TokenType.text:
                self.current_token = self.lexer.return_next_token
                return
            elif self.current_token.type == TokenType.opening_tag or self.current_token.type == TokenType.opening_end_tag:
                return
            elif self.current_token.type == TokenType.end_of_file:
                print("Natrafiono na koniec pliku, parsowanie zaończono powodzeniem")
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
            self.checkIfTokenExpected(TokenType.equal_sign, 'tuutaj')
            self.current_token = self.lexer.return_next_token
            self.checkIfTokenExpected(TokenType.quotation_mark)
            self.current_token = self.lexer.return_next_token
            self.checkIfTokenExpected(TokenType.text)
            self.current_token = self.lexer.return_next_token
            self.checkIfTokenExpected(TokenType.quotation_mark)
            self.current_token = self.lexer.return_next_token


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




