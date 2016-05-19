from enum import Enum


class TokenType(Enum):
    opening_tag = 1
    close_tag = 2
    opening_end_tag = 3
    close_end_tag = 4
    quotation_mark = 5
    equal_sign = 6
    text = 7
    doctype = 8
    end_of_file = 9


def is_correct(regexp_def, correct_end_states, value):
    """
    Method checking whether given string is correct according
    to the given regular expression definition.
    :param regexp_def definition of a specific regular expression
    :param correct_end_states table of correct end states
    :value string to check
    """

    state = 0
    for i in value:  # Going through the string checking each char
        try:
            state = regexp_def[state][i]
        except KeyError:
            return False

    if state in correct_end_states:
        return True
    return False


def is_opening_tag(value):
    return value == '<'


def is_close_tag(value):
    return value == '>'


def is_opening_end_tag(value):
    return value == '</'


def is_close_end_tag(value):
    return value == '/>'


def is_quotation_mark(value):
    return value == '"'


def is_equal_sign(value):
    return value == '='


def is_text(value):
    """
    Function can take various sign depending on the occasion, another part of Lexer
    is taking care for the proper value parameter.
    """
    return True


def is_doctype(value):
    """
    Function checking whether a given string matches an text_between_tags
    regexp : any keyboard character without ";<;>
    :param value: string
    """

    state_3 = {}

    for char in range(32, 126 + 1):  # all keyboard chars without "
        if char != 62:
            state_3[chr(char)] = 3
    state_3['>'] = 4

    regexp_def = [
        {'<': 1},
        {'!': 2},
        {'D': 2, 'O': 2, 'C': 2, 'T': 2, 'Y': 2, 'P': 2, 'E': 3},
        state_3,
        {}
    ]

    correct_end_states = {4}
    return is_correct(regexp_def, correct_end_states, value)

def file_end(value):
    return True

class ErrorMessage(Exception):
    def __init__(self, line_number, line_char_number, value):
        self.line_number = line_number
        self.line_char_number = line_char_number
        self.errmsg = 'Lexer exception ' + value


class Token:
    __token_values = {
        TokenType.opening_tag: is_opening_tag,
        TokenType.close_tag: is_close_tag,
        TokenType.opening_end_tag: is_opening_end_tag,
        TokenType.close_end_tag: is_close_end_tag,
        TokenType.quotation_mark: is_quotation_mark,
        TokenType.equal_sign: is_equal_sign,
        TokenType.text: is_text,
        TokenType.doctype: is_doctype,
        TokenType.end_of_file: file_end,
    }

    def __init__(self, value, line_number, line_char_number, force_token=False
                 , force_token_value=0):
        self.type = None
        self.value = value
        self.line_number = line_number
        self.line_char_number = line_char_number

        if force_token:
            checking_function = self.__token_values[TokenType(force_token_value)]
            if checking_function(value):
                self.type = TokenType(force_token_value)
                return
            else:
                raise ErrorMessage(line_number, line_char_number, value)
        else:
            for token_value in range(1, 8):
                checking_function2 = self.__token_values[TokenType(token_value)]
                token_type = TokenType(token_value)
                if checking_function2(value):
                    self.type = token_type
                    break

        if self.type is None:
            raise ErrorMessage(line_number, line_char_number, value)


class Lexer:
    def __init__(self, file):
        self.file = file
        self.token_list = []
        self.current_line_number = 0
        self.start_of_token = 1
        self.current_line_char_number = 0

    @property
    def return_next_token(self):
        if (self.current_line_number == len(self.file)) or (
                        self.current_line_number == len(self.file) - 1 and self.current_line_char_number == len(
                    self.file[self.current_line_number])):
            return Token(self.file[self.current_line_number - 1], self.current_line_number, self.current_line_char_number, True, 9)

        line_char_number = self.current_line_char_number
        line = self.file[self.current_line_number]
        line_number = self.current_line_number

        if is_opening_tag(line[line_char_number]):
            if (line[line_char_number:line_char_number + 2]) == '<!':
                start_of_token = line_char_number
                var = line_char_number
                for var in range(line_char_number, len(line)):
                    if line[var] == '>':
                        self.token_list.append(
                            Token(line[start_of_token:var + 1], line_number, start_of_token, True, 8))
                        self.current_line_char_number = var + 1
                        return self.token_list[-1]
                    elif line_char_number == len(line):
                        print('Nie znaleziono nawiasu domknięcia DOCTYPE')
            elif is_opening_end_tag(line[line_char_number:line_char_number + 2]):
                self.token_list.append(
                    Token(line[line_char_number:line_char_number + 2], line_number, line_char_number))
                self.current_line_char_number = line_char_number + 2
                return self.token_list[-1]
            else:
                self.token_list.append(Token(line[line_char_number], line_number, line_char_number))
                self.current_line_char_number += 1
                return self.token_list[-1]
        elif ord(line[line_char_number]) == 32:
            self.current_line_char_number += 1
            return self.return_next_token
        elif ord(line[line_char_number]) == 10:
            self.current_line_number += 1
            self.current_line_char_number = 0
            return self.return_next_token
        elif is_equal_sign(line[line_char_number]):  # znak równości
            self.token_list.append(Token(line[line_char_number], line_number, line_char_number))
            self.current_line_char_number += 1
            return self.token_list[-1]
        elif is_quotation_mark(line[line_char_number]):
            self.token_list.append(Token(line[line_char_number], line_number, line_char_number))
            self.current_line_char_number += 1
            return self.token_list[-1]
        elif line[line_char_number] == '/' and line[line_char_number - 1] != '"':
            if (line[line_char_number:line_char_number + 2]) == '/>':
                self.token_list.append(
                    Token(line[line_char_number:line_char_number + 2], line_number, line_char_number, True, 4))
                self.current_line_char_number = line_char_number + 2
                return self.token_list[-1]
        elif is_close_tag(line[line_char_number]):
            self.token_list.append(Token(line[line_char_number], line_number, line_char_number))
            self.current_line_char_number = line_char_number + 1
            return self.token_list[-1]
        else:
            start_of_token = self.current_line_char_number
            if ((line[line_char_number - 1]) == '<') or (
                            line[line_char_number - 1] == '/' and line[line_char_number - 2] == '<'):
                for var in range(line_char_number, len(line)):
                    if (line[var]) == ' ' or (line[var]) == '>' or (line[var]) == '/':
                        self.token_list.append(Token(line[start_of_token:var], line_number, start_of_token, True, 7))
                        self.current_line_char_number = var
                        return self.token_list[-1]
            if ((line[self.current_line_char_number - 1] == ' ') and (line[
                                                                              self.current_line_char_number - 2] != '>') and self.current_line_char_number != 1):  # html_attribute
                go_back_index = self.current_line_char_number - 1
                while go_back_index >= 0:
                    if line[go_back_index] != ' ':
                        break
                    go_back_index -= 1
                if ord('a') - 1 < ord(line[go_back_index]) < ord('z') + 1 or line[go_back_index] == '"':
                    for var in range(self.current_line_char_number, len(line)):
                        if not((line[var]) == '-' or (ord('a') - 1 < ord(line[var]) < ord('z') + 1)):
                            self.token_list.append(
                                Token(line[start_of_token:var], line_number, start_of_token, True, 7))
                            self.current_line_char_number = var
                            return self.token_list[-1]
            if line[line_char_number - 1] == '"' or line[line_char_number - 1] == ' ':
                go_back_index = self.current_line_char_number - 1
                while go_back_index >= 0:
                    if line[go_back_index] != ' ':
                        break
                    go_back_index -= 1
                if line[go_back_index] == '"':
                    for var in range(line_char_number, len(line)):
                        if (line[var]) == '"':
                            self.token_list.append(
                                Token(line[start_of_token:var], line_number, start_of_token, True, 7))
                            self.current_line_char_number = var
                            return self.token_list[-1]
            if (line[self.current_line_char_number - 1] == ' ') or (line[self.current_line_char_number - 1] == '>'):
                go_back_index = self.current_line_char_number - 1
                while go_back_index >= 0:
                    if line[go_back_index] != ' ':
                        break
                    go_back_index -= 1
                if go_back_index == -1:
                    previous_line_index = 1
                    finish = False
                    while True:
                        previous_line = self.file[self.current_line_number - previous_line_index]
                        previous_line_go_back_index = len(previous_line) - 1
                        while previous_line_go_back_index >= 0:
                            if not (previous_line[go_back_index] == ' ' or ord(
                                    previous_line[previous_line_go_back_index]) == 10):
                                finish = True
                                break
                            previous_line_go_back_index -= 1
                        if finish:
                            break
                        previous_line_index -= 1
                if (line[go_back_index] == '>') or (previous_line[previous_line_go_back_index] == '>'):
                    ending_string = ""
                    var = self.current_line_char_number
                    while var < len(line):
                        if ord(line[var]) == 10:
                            ending_string = ending_string + line[start_of_token:var]
                            self.current_line_number += 1
                            line = self.file[self.current_line_number]
                            self.current_line_char_number = 0
                            var = 0
                            start_of_token = 0
                        if (line[var]) == '<':
                            ending_string = ending_string + line[start_of_token:var]
                            self.token_list.append(Token(ending_string, line_number, start_of_token, True, 7))
                            self.current_line_char_number = var
                            return self.token_list[-1]
                        var += 1
        print('Lexetr nie znalazł żadnego pasującego tokenu w linii:', self.current_line_number + 1, 'znak:',
              self.current_line_char_number + 1)


    def print_lines(self):
        for line in self.file:
            print(line)

    def print_tags(self):
        for tag in self.token_list:
            print(tag.type, tag.value)
