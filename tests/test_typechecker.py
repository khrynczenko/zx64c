import pytest

from zx64c.ast import SourceContext, Identifier
from tests.ast import (
    TEST_CONTEXT,
    ProgramTC,
    PrintTC,
    AssignmentTC,
    AdditionTC,
    NegationTC,
    UnsignedintTC,
    IdentifierTC,
    BoolTC,
)
from zx64c.typechecker import (
    TypecheckerVisitor,
    Environment,
    Type,
    CombinedTypecheckErrors,
    TypeMismatch,
    UndefinedVariable,
)


def test_unsignedint_node_type():
    ast = UnsignedintTC(1)

    typecheck_result = ast.visit(TypecheckerVisitor())

    assert typecheck_result is Type.U8


def test_bool_node_type():
    ast = BoolTC(True)

    typecheck_result = ast.visit(TypecheckerVisitor())

    assert typecheck_result is Type.BOOL


def test_addition_node_type():
    ast = AdditionTC(UnsignedintTC(1), UnsignedintTC(2))

    typecheck_result = ast.visit(TypecheckerVisitor())

    assert typecheck_result is Type.U8


@pytest.mark.parametrize(
    "lhs_node, rhs_node, expected_type, got_type",
    [
        (BoolTC(True), UnsignedintTC(1), Type.U8, Type.BOOL),
        (UnsignedintTC(1), BoolTC(True), Type.U8, Type.BOOL),
    ],
)
def test_addition_node_type_mismatch(lhs_node, rhs_node, expected_type, got_type):
    ast = AdditionTC(lhs_node, rhs_node)

    typecheck_result = ast.visit(TypecheckerVisitor())

    assert typecheck_result == TypeMismatch(expected_type, got_type, TEST_CONTEXT)


@pytest.mark.parametrize(
    "lhs_node, rhs_node",
    [(IdentifierTC("x"), UnsignedintTC(1)), (UnsignedintTC(1), IdentifierTC("x"))],
)
def test_addition_node_type_error_propagates(lhs_node, rhs_node):
    ast = AdditionTC(lhs_node, rhs_node)

    typecheck_result = ast.visit(TypecheckerVisitor())

    assert typecheck_result == UndefinedVariable("x", TEST_CONTEXT)


def test_addition_node_type_mismatch_with_identifier():
    ast = ProgramTC(
        [
            AssignmentTC("x", BoolTC(True)),
            AdditionTC(IdentifierTC("x"), UnsignedintTC(1)),
        ]
    )

    typecheck_result = ast.visit(TypecheckerVisitor())

    expected_error = CombinedTypecheckErrors(
        [TypeMismatch(Type.U8, Type.BOOL, TEST_CONTEXT)]
    )
    assert typecheck_result == expected_error


def test_identifier_node_type():
    ast = IdentifierTC("x")
    environment = Environment()
    environment.add_variable("x", Type.U8)

    typecheck_result = ast.visit(TypecheckerVisitor(environment))

    assert typecheck_result is Type.U8


def test_identifier_node_type_with_undefined_variable():
    ast = IdentifierTC("x")
    empty_environment = Environment()

    typecheck_result = ast.visit(TypecheckerVisitor(empty_environment))

    assert typecheck_result == UndefinedVariable("x", TEST_CONTEXT)


def test_negation_node():
    ast = NegationTC(UnsignedintTC(1))

    typecheck_result = ast.visit(TypecheckerVisitor())

    assert typecheck_result is Type.U8


def test_negation_node_type_mismatch():
    ast = NegationTC(BoolTC(True))

    typecheck_result = ast.visit(TypecheckerVisitor())

    assert typecheck_result == TypeMismatch(Type.U8, Type.BOOL, TEST_CONTEXT)


def test_print_node_type():
    ast = PrintTC(UnsignedintTC(1))

    typecheck_result = ast.visit(TypecheckerVisitor())

    assert typecheck_result is Type.VOID


def test_assignment_node_type():
    ast = AssignmentTC("x", UnsignedintTC(1))

    typecheck_result = ast.visit(TypecheckerVisitor())

    assert typecheck_result is Type.VOID


def test_program_node_type():
    ast = ProgramTC([AssignmentTC("x", UnsignedintTC(1))])

    typecheck_result = ast.visit(TypecheckerVisitor())

    assert typecheck_result is Type.VOID


def test_program_node_type_with_errors():
    context = SourceContext(1, 5)
    identifier = Identifier("y", context)
    ast = ProgramTC([AssignmentTC("x", UnsignedintTC(1)), PrintTC(identifier)])

    typecheck_result = ast.visit(TypecheckerVisitor())

    assert typecheck_result == CombinedTypecheckErrors(
        [UndefinedVariable("y", context)]
    )
