# Token types
# EOF (end-of-file) token is used to indicate that 
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS','MINUS', 'EOF'

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+' or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
        Token(INTEGER, 3)
        Token(PLUS, '+')
        """
        return 'Token({}, {})'.format(self.type, repr(self.value))

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')
        
    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue
        
            if self.current_char.isdigit():
                return Token(INTEGER,self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            self.error()
    
        return Token(EOF, None)

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multiple) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len (self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            
    def eat(self, token_type):
        """Compare the current token type with the passed token type.
        If they match, then "eat" the current token and assign
        the next token to self.current_token, otherwise raise an exception.
        """
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()


    def term(self):
        """Return INTEGER Token value"""
        Token = self.current_token
        self.eat(INTEGER)
        return Token.value        

    def expr(self):
        """Parser / Interpreter"""
        """expr -> INTEGER PLUS INTEGER"""
        """expr -> INTEGER MINUS INTEGER"""
        # set current token to the first taken from the input
        self.current_token = self.get_next_token()
        
        result =  self.term()
        while self.current_token.type in (PLUS,MINUS):
            Token = self.current_token
            if Token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif Token.type == MINUS:
                self.eat(MINUS)
                result = result-self.term()

        return result
    
def main():
    while True:
        try:
            # to run under Python 3, replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
