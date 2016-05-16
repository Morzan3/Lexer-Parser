from lexer import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token



    def parseDocument(self):


        if self.checkIfTokenExpected(TokenType.doctype):
            self.current_token = self.lexer.return_next_token
            if self.checkIfTokenExpected(TokenType.opening_tag):
                self.current_token = self.lexer.return_next_token
                self.checkIfTokenExpected()

    def start(self):
        self.current_token = self.lexer.return_next_token
        if not(self.checkIfTokenExpected(TokenType.doctype)):
            raise SystemExit
        self.current_token = self.lexer.return_next_token
        self.tag()

    def tag(self):
        if not(self.checkIfTokenExpected(TokenType.opening_tag)):
            raise SystemExit
        self.current_token = self.lexer.return_next_token
        if not(self.checkIfTokenExpected(TokenType.text)):
            raise SystemExit
        self.attributes()

    def tag_closure(self):
        if self.checkIfTokenExpected(TokenType.close_end_tag):
            self.self_closure_tag()


    def self_closure_tag(self):
        self.current_token = self.lexer.return_next_token
        if self.current_token == TokenType.text:
            self.current_token = self.lexer.return_next_token
            self.tag()

        if self.checkIfTokenExpected(TokenType.opening_tag, "or TokenType.text"):
            self.tag()

    def attributes(self):
        self.current_token = self.lexer.return_next_token

        while self.current_token == TokenType.text:
            self.attribute()

    def attribute(self):
        if self.current_token == TokenType.text:
            self.current_token = self.lexer.return_next_token
            self.checkIfTokenExpected(TokenType.equal_sign)
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
             error_message = error_message + "Token occured: " + self.current_token.type.name
             error_message = error_message + "Token expected: " + expected_token_type.name
             error_message = error_message + optional_message
             print(error_message)
             return False
         return True




