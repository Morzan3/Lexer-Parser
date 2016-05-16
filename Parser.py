import lexer


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        print(lexer.return_next_token.type)