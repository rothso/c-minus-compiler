import compiler.lexer as lexer


class TestIntegers(object):

    def test_reads_integers_surrounded_by_parentheses(self):
        assert lexer.lex('(123)') == [
            ('PUNCTUATION', '('),
            ('INTEGER', '123'),
            ('PUNCTUATION', ')')
        ]


class TestFloats(object):

    # Basic floats
    def test_reads_floats_at_end_of_string(self):
        assert lexer.lex('123.12345') == [('FLOAT', '123.12345')]

    def test_doesnt_read_float_with_trailing_dot(self):
        assert lexer.lex('123.') == [('INTEGER', '123'), ('INVALID', '.')]

    def test_doesnt_read_float_without_leading_number(self):
        assert lexer.lex('.5') == [('INVALID', '.'), ('INTEGER', '5')]

    def test_skips_dangling_float_decimal(self):
        assert lexer.lex('1.)') == [('INTEGER', '1'), ('INVALID', '.'), ('PUNCTUATION', ')')]

    # Floats in scientific notation
    def test_reads_floats_in_scientific_notation(self):
        assert lexer.lex('1.2E2') == [('FLOAT', '1.2E2')]

    def test_reads_floats_in_signed_scientific_notation(self):
        assert lexer.lex('120.0E-2') == [('FLOAT', '120.0E-2')]

    def test_reads_integers_in_scientific_notation_as_floats(self):
        assert lexer.lex('1E2') == [('FLOAT', '1E2')]

    def test_reads_integers_in_signed_scientific_notation_as_floats(self):
        assert lexer.lex('1E-2') == [('FLOAT', '1E-2')]

    def test_doesnt_read_float_with_trailing_e(self):
        assert lexer.lex('4.0E') == [('FLOAT', '4.0'), ('ID', 'E')]

    def test_doesnt_read_e_as_float(self):
        assert lexer.lex('.E') == [('INVALID', '.'), ('ID', 'E')]

    def test_doesnt_read_incomplete_scientific_notation_as_float(self):
        assert lexer.lex('6.0E+') == [('FLOAT', '6.0'), ('ID', 'E'), ('MATHOP', '+')]


class TestWhitespace:

    def test_ignores_whitespace(self):
        assert lexer.lex(' 1\t1\n\r ') == [('INTEGER', '1'), ('INTEGER', '1')]


class TestIdentifiers:

    def test_recognizes_keywords(self):
        assert lexer.lex('int float void while if else return') == [
            ('KEYWORD', 'int'),
            ('KEYWORD', 'float'),
            ('KEYWORD', 'void'),
            ('KEYWORD', 'while'),
            ('KEYWORD', 'if'),
            ('KEYWORD', 'else'),
            ('KEYWORD', 'return'),
        ]

    def test_reads_identifiers(self):
        assert lexer.lex('a bba') == [('ID', 'a'), ('ID', 'bba')]

    def test_reads_identifiers_containing_capital_letters(self):
        assert lexer.lex('aBC AAA') == [('ID', 'aBC'), ('ID', 'AAA')]

    def test_reads_identifiers_followed_by_numbers(self):
        assert lexer.lex('abc99') == [('ID', 'abc'), ('INTEGER', '99')]


class TestBrackets:

    def test_reads_brackets(self):
        assert lexer.lex('[]') == [('PUNCTUATION', '['), ('PUNCTUATION', ']')]

    def test_reads_parentheses(self):
        assert lexer.lex('()') == [('PUNCTUATION', '('), ('PUNCTUATION', ')')]

    def test_reads_braces(self):
        assert lexer.lex('{}') == [('PUNCTUATION', '{'), ('PUNCTUATION', '}')]


class TestCommentStripper:

    def test_strips_comments(self):
        assert lexer.strip_comments('/*c*/') == ''

    def test_keeps_code_around_comments(self):
        assert lexer.strip_comments("a/*c*/a") == 'aa'

    def test_strips_unclosed_comments(self):
        assert lexer.strip_comments("a/*/*c*/ab") == 'a'

    def test_strips_nested_comments(self):
        assert lexer.strip_comments("a/*/*c*/*/b") == 'ab'

    def test_doesnt_interpret_multiply_divide_as_closing_comment(self):
        assert lexer.strip_comments("a/*c*/*/b") == 'a*/b'


class TestComments:

    def test_ignores_comments(self):
        assert lexer.lex('1/*comment*/1') == [('INTEGER', '11')]

    def test_ignores_nested_comments(self):
        assert lexer.lex('1/*co/*e*/nt*/1') == [('INTEGER', '11')]

    def test_ignores_comments_containing_spaces(self):
        assert lexer.lex('/**/          /*/* */   */') == []

    def test_ignores_multiline_comments(self):
        assert lexer.lex('''/**************/
                            /*************************
                            i = 333;        ******************/''') == []

    def test_ignores_line_comments(self):
        assert lexer.lex('''1
                            // ignore me
                            2''') == [('INTEGER', '1'), ('INTEGER', '2')]


class TestIntegration:

    def test_tokenizes_eggens_sample_input(self):
        assert lexer.lex('''
          /**/          /*/* */   */
          /*/*/****This**********/*/    */
          /**************/
          /*************************
          i = 333;        ******************/
    
          iiii = 3@33;
    
          int g 4 cd (int u, int v)      {
          if(v == >= 0) return/*a comment*/ u;
          else ret_urn gcd(vxxxxxxvvvvv, u-u/v*v);
                /* u-u/v*v == u mod v*/
          !
          }
    
          return void while       void main()
        ''') == [
            ('ID', 'iiii'),
            ('PUNCTUATION', '='),
            ('INTEGER', '3'),
            ('INVALID', '@'),
            ('INTEGER', '33'),
            ('PUNCTUATION', ';'),
            ('KEYWORD', 'int'),
            ('ID', 'g'),
            ('INTEGER', '4'),
            ('ID', 'cd'),
            ('PUNCTUATION', '('),
            ('KEYWORD', 'int'),
            ('ID', 'u'),
            ('PUNCTUATION', ','),
            ('KEYWORD', 'int'),
            ('ID', 'v'),
            ('PUNCTUATION', ')'),
            ('PUNCTUATION', '{'),
            ('KEYWORD', 'if'),
            ('PUNCTUATION', '('),
            ('ID', 'v'),
            ('RELOP', '=='),
            ('RELOP', '>='),
            ('INTEGER', '0'),
            ('PUNCTUATION', ')'),
            ('KEYWORD', 'return'),
            ('ID', 'u'),
            ('PUNCTUATION', ';'),
            ('KEYWORD', 'else'),
            ('ID', 'ret'),
            ('INVALID', '_'),
            ('ID', 'urn'),
            ('ID', 'gcd'),
            ('PUNCTUATION', '('),
            ('ID', 'vxxxxxxvvvvv'),
            ('PUNCTUATION', ','),
            ('ID', 'u'),
            ('MATHOP', '-'),
            ('ID', 'u'),
            ('MATHOP', '/'),
            ('ID', 'v'),
            ('MATHOP', '*'),
            ('ID', 'v'),
            ('PUNCTUATION', ')'),
            ('PUNCTUATION', ';'),
            ('INVALID', '!'),
            ('PUNCTUATION', '}'),
            ('KEYWORD', 'return'),
            ('KEYWORD', 'void'),
            ('KEYWORD', 'while'),
            ('KEYWORD', 'void'),
            ('ID', 'main'),
            ('PUNCTUATION', '('),
            ('PUNCTUATION', ')'),
        ]
