"""
Contains modified constructors for all subclasses of the Ast. These constructors
are partially applied with an arbitrary context. They are used in tests that
do not care about node context.
"""

import functools

from zx64c.ast import (
    Program,
    Function,
    Block,
    If,
    Let,
    Return,
    Print,
    Assignment,
    Equal,
    NotEqual,
    Addition,
    Subtraction,
    Negation,
    FunctionCall,
    Unsignedint,
    Identifier,
    Bool,
)
from zx64c.ast import SourceContext

TEST_CONTEXT = SourceContext(0, 0)

# Ast nodes that have already filled context in the constructor
ProgramTC = functools.partial(Program, context=TEST_CONTEXT)
FunctionTC = functools.partial(Function, context=TEST_CONTEXT)
BlockTC = functools.partial(Block, context=TEST_CONTEXT)
IfTC = functools.partial(If, context=TEST_CONTEXT)
LetTC = functools.partial(Let, context=TEST_CONTEXT)
ReturnTC = functools.partial(Return, context=TEST_CONTEXT)
PrintTC = functools.partial(Print, context=TEST_CONTEXT)
AssignmentTC = functools.partial(Assignment, context=TEST_CONTEXT)
EqualTC = functools.partial(Equal, context=TEST_CONTEXT)
NotEqualTC = functools.partial(NotEqual, context=TEST_CONTEXT)
AdditionTC = functools.partial(Addition, context=TEST_CONTEXT)
SubtractionTC = functools.partial(Subtraction, context=TEST_CONTEXT)
NegationTC = functools.partial(Negation, context=TEST_CONTEXT)
FunctionCallTC = functools.partial(FunctionCall, context=TEST_CONTEXT)
UnsignedintTC = functools.partial(Unsignedint, context=TEST_CONTEXT)
IdentifierTC = functools.partial(Identifier, context=TEST_CONTEXT)
BoolTC = functools.partial(Bool, context=TEST_CONTEXT)
