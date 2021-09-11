from typing import List

from tests.ast import (
    ProgramTC,
    FunctionTC,
    BlockTC,
    IfTC,
    PrintTC,
    LetTC,
    AssignmentTC,
    AdditionTC,
    NegationTC,
    UnsignedintTC,
    IdentifierTC,
    BoolTC,
    TEST_CONTEXT,
)
from zx64c.ast import Parameter
from zx64c.scanner import Token, TokenCategory
from zx64c.parser import Parser, UnexpectedTokenError
from zx64c.types import Type, VOID, U8, BOOL


def build_test_tokens_from_categories(categories: List[TokenCategory]):
    return [Token(0, 0, category, "") for category in categories]


def make_token_with_lexeme(category: TokenCategory, lexeme: str) -> Token:
    return Token(0, 0, category, lexeme)


def make_arbitrary_token(category: TokenCategory) -> Token:
    return Token(0, 0, category, "")


def make_tokens_inside_main(*args):
    tokens = [
        make_arbitrary_token(TokenCategory.DEF),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "main"),
        make_arbitrary_token(TokenCategory.LEFT_PAREN),
        make_arbitrary_token(TokenCategory.RIGHT_PAREN),
        make_arbitrary_token(TokenCategory.ARROW),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "void"),
        make_arbitrary_token(TokenCategory.COLON),
        make_arbitrary_token(TokenCategory.NEWLINE),
        make_arbitrary_token(TokenCategory.INDENT),
        *args,
        make_arbitrary_token(TokenCategory.DEDENT),
        make_arbitrary_token(TokenCategory.EOF),
    ]
    return tokens


def make_ast_inside_main(*args):
    return ProgramTC([FunctionTC("main", [], VOID, BlockTC([*args]))])


def test_testing_utilities():
    parser = Parser(make_tokens_inside_main())
    ast = parser.parse()

    assert ast == make_ast_inside_main()


def test_parsing_print_identifier():
    tokens = make_tokens_inside_main(
        make_arbitrary_token(TokenCategory.PRINT),
        make_arbitrary_token(TokenCategory.LEFT_PAREN),
        make_token_with_lexeme(TokenCategory.UNSIGNEDINT, "10"),
        make_arbitrary_token(TokenCategory.RIGHT_PAREN),
        make_arbitrary_token(TokenCategory.NEWLINE),
    )

    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = make_ast_inside_main(PrintTC(UnsignedintTC(10)))
    assert ast == expected_ast


def test_parsing_function_with_not_arguments():
    tokens = [
        make_arbitrary_token(TokenCategory.DEF),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "main"),
        make_arbitrary_token(TokenCategory.LEFT_PAREN),
        make_arbitrary_token(TokenCategory.RIGHT_PAREN),
        make_arbitrary_token(TokenCategory.ARROW),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "void"),
        make_arbitrary_token(TokenCategory.COLON),
        make_arbitrary_token(TokenCategory.NEWLINE),
        make_arbitrary_token(TokenCategory.INDENT),
        make_token_with_lexeme(TokenCategory.UNSIGNEDINT, "1"),
        make_arbitrary_token(TokenCategory.NEWLINE),
        make_arbitrary_token(TokenCategory.DEDENT),
        make_arbitrary_token(TokenCategory.EOF),
    ]

    ast = Parser(tokens).parse()

    name = "main"
    parameters = []
    return_type = VOID
    code_block = BlockTC([UnsignedintTC(1)])
    assert ast == ProgramTC([FunctionTC(name, parameters, return_type, code_block)])


def test_parsing_function_with_one_arguments():
    tokens = [
        make_arbitrary_token(TokenCategory.DEF),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "main"),
        make_arbitrary_token(TokenCategory.LEFT_PAREN),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "x"),
        make_arbitrary_token(TokenCategory.COLON),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "u8"),
        make_arbitrary_token(TokenCategory.RIGHT_PAREN),
        make_arbitrary_token(TokenCategory.ARROW),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "void"),
        make_arbitrary_token(TokenCategory.COLON),
        make_arbitrary_token(TokenCategory.NEWLINE),
        make_arbitrary_token(TokenCategory.INDENT),
        make_token_with_lexeme(TokenCategory.UNSIGNEDINT, "1"),
        make_arbitrary_token(TokenCategory.NEWLINE),
        make_arbitrary_token(TokenCategory.DEDENT),
        make_arbitrary_token(TokenCategory.EOF),
    ]

    ast = Parser(tokens).parse()

    name = "main"
    parameters = [Parameter("x", U8)]
    return_type = VOID
    code_block = BlockTC([UnsignedintTC(1)])
    assert ast == ProgramTC([FunctionTC(name, parameters, return_type, code_block)])


def test_parsing_function_with_two_arguments():
    tokens = [
        make_arbitrary_token(TokenCategory.DEF),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "main"),
        make_arbitrary_token(TokenCategory.LEFT_PAREN),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "x"),
        make_arbitrary_token(TokenCategory.COLON),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "u8"),
        make_arbitrary_token(TokenCategory.COMMA),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "y"),
        make_arbitrary_token(TokenCategory.COLON),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "bool"),
        make_arbitrary_token(TokenCategory.RIGHT_PAREN),
        make_arbitrary_token(TokenCategory.ARROW),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "void"),
        make_arbitrary_token(TokenCategory.COLON),
        make_arbitrary_token(TokenCategory.NEWLINE),
        make_arbitrary_token(TokenCategory.INDENT),
        make_token_with_lexeme(TokenCategory.UNSIGNEDINT, "1"),
        make_arbitrary_token(TokenCategory.NEWLINE),
        make_arbitrary_token(TokenCategory.DEDENT),
        make_arbitrary_token(TokenCategory.EOF),
    ]

    ast = Parser(tokens).parse()

    name = "main"
    parameters = [Parameter("x", U8), Parameter("y", BOOL)]
    return_type = VOID
    code_block = BlockTC([UnsignedintTC(1)])
    assert ast == ProgramTC([FunctionTC(name, parameters, return_type, code_block)])


def test_parsing_let_unsigned_int():
    tokens = make_tokens_inside_main(
        make_arbitrary_token(TokenCategory.LET),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "x"),
        make_arbitrary_token(TokenCategory.COLON),
        make_token_with_lexeme(TokenCategory.U8, "u8"),
        make_arbitrary_token(TokenCategory.ASSIGN),
        make_token_with_lexeme(TokenCategory.UNSIGNEDINT, "10"),
        make_arbitrary_token(TokenCategory.NEWLINE),
    )

    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = make_ast_inside_main(LetTC("x", Type("u8"), UnsignedintTC(10)))
    assert ast == expected_ast


def test_parsing_assignment_unsignedint():
    tokens = make_tokens_inside_main(
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "x"),
        make_arbitrary_token(TokenCategory.ASSIGN),
        make_token_with_lexeme(TokenCategory.UNSIGNEDINT, "10"),
        make_arbitrary_token(TokenCategory.NEWLINE),
    )

    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = make_ast_inside_main(AssignmentTC("x", UnsignedintTC(10)))
    assert ast == expected_ast


def test_parsing_assignment_bool_true():
    tokens = make_tokens_inside_main(
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "x"),
        make_arbitrary_token(TokenCategory.ASSIGN),
        make_arbitrary_token(TokenCategory.TRUE),
        make_arbitrary_token(TokenCategory.NEWLINE),
    )

    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = make_ast_inside_main(AssignmentTC("x", BoolTC(True)))
    assert ast == expected_ast


def test_parsing_assignment_bool_false():
    tokens = make_tokens_inside_main(
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "x"),
        make_arbitrary_token(TokenCategory.ASSIGN),
        make_arbitrary_token(TokenCategory.FALSE),
        make_arbitrary_token(TokenCategory.NEWLINE),
    )

    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = make_ast_inside_main(AssignmentTC("x", BoolTC(False)))
    assert ast == expected_ast


def test_parsing_assignment_negated_unsignedint():
    tokens = make_tokens_inside_main(
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "x"),
        make_arbitrary_token(TokenCategory.ASSIGN),
        make_arbitrary_token(TokenCategory.MINUS),
        make_token_with_lexeme(TokenCategory.UNSIGNEDINT, "10"),
        make_arbitrary_token(TokenCategory.NEWLINE),
    )

    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = make_ast_inside_main(
        AssignmentTC("x", NegationTC(UnsignedintTC(10)))
    )
    assert ast == expected_ast


def test_parsing_assignment_identifier():
    tokens = make_tokens_inside_main(
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "x"),
        make_arbitrary_token(TokenCategory.ASSIGN),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "y"),
        make_arbitrary_token(TokenCategory.NEWLINE),
    )

    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = make_ast_inside_main(AssignmentTC("x", IdentifierTC("y")))
    assert ast == expected_ast


def test_parsing_assignment_arithmetic_expression():
    tokens = make_tokens_inside_main(
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "x"),
        make_arbitrary_token(TokenCategory.ASSIGN),
        make_token_with_lexeme(TokenCategory.UNSIGNEDINT, "10"),
        make_arbitrary_token(TokenCategory.PLUS),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "y"),
        make_arbitrary_token(TokenCategory.NEWLINE),
    )

    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = make_ast_inside_main(
        AssignmentTC("x", AdditionTC(UnsignedintTC(10), IdentifierTC("y")))
    )
    assert ast == expected_ast


def test_parsing_assignment_complex_arithmetic_expression():
    tokens = make_tokens_inside_main(
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "x"),
        make_arbitrary_token(TokenCategory.ASSIGN),
        make_token_with_lexeme(TokenCategory.UNSIGNEDINT, "10"),
        make_arbitrary_token(TokenCategory.PLUS),
        make_arbitrary_token(TokenCategory.LEFT_PAREN),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "y"),
        make_arbitrary_token(TokenCategory.PLUS),
        make_token_with_lexeme(TokenCategory.UNSIGNEDINT, "20"),
        make_arbitrary_token(TokenCategory.RIGHT_PAREN),
        make_arbitrary_token(TokenCategory.NEWLINE),
    )

    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = make_ast_inside_main(
        AssignmentTC(
            "x",
            AdditionTC(
                UnsignedintTC(10), AdditionTC(IdentifierTC("y"), UnsignedintTC(20))
            ),
        )
    )
    assert ast == expected_ast


def test_parsing_if_statement():
    tokens = make_tokens_inside_main(
        make_arbitrary_token(TokenCategory.IF),
        make_arbitrary_token(TokenCategory.TRUE),
        make_arbitrary_token(TokenCategory.COLON),
        make_arbitrary_token(TokenCategory.NEWLINE),
        make_arbitrary_token(TokenCategory.INDENT),
        make_token_with_lexeme(TokenCategory.IDENTIFIER, "y"),
        make_arbitrary_token(TokenCategory.NEWLINE),
        make_arbitrary_token(TokenCategory.DEDENT),
    )

    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = make_ast_inside_main(
        IfTC(BoolTC(True), BlockTC([IdentifierTC("y")]))
    )
    assert ast == expected_ast


def test_parser_raises_on_unexpected_token():
    tokens = make_tokens_inside_main(
        make_arbitrary_token(TokenCategory.IF),
        make_arbitrary_token(TokenCategory.TRUE),
        make_arbitrary_token(TokenCategory.COLON),
        make_arbitrary_token(TokenCategory.NEWLINE),
        make_arbitrary_token(TokenCategory.IDENTIFIER),
    )

    parser = Parser(tokens)
    try:
        parser.parse()
    except UnexpectedTokenError as e:
        assert e == UnexpectedTokenError(
            [TokenCategory.INDENT], TokenCategory.IDENTIFIER, TEST_CONTEXT
        )
        return

    assert False, "Expected exception not raised"
