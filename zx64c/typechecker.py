from __future__ import annotations

import abc
from abc import ABC
from typing import Union

from zx64c.ast import (
    SourceContext,
    Program,
    Print,
    Assignment,
    Addition,
    Negation,
    Identifier,
    Unsignedint,
    Bool,
)
from zx64c.ast import AstVisitor
from zx64c.types import Type


class Environment:
    def __init__(self):
        self._variable_types = {}

    def add_variable(self, name: str, variable_type: Type):
        self._variable_types[name] = variable_type

    def get_variable_type(
        self, name: str, context: SourceContext
    ) -> Union[Type, TypecheckError]:
        """
        :param context: used to create error in case the variable is not defined
        """
        return self._variable_types.get(name, UndefinedVariable(name, context))


class TypecheckError(ABC):
    @abc.abstractmethod
    def make_error_message(self) -> str:
        pass

    def __eq__(self, rhs: TypecheckError):
        return self.make_error_message() == rhs.make_error_message()


class CombinedTypecheckErrors(TypecheckError):
    def __init__(self, errors: [TypecheckError]):
        self._errors = errors

    def make_error_message(self) -> str:
        return "".join(
            [error.make_error_message() + "\n" for error in self._errors]
        ).rstrip("\n")


class TypeMismatch(TypecheckError):
    def __init__(
        self, expected_type: Type, received_type: Type, context: SourceContext
    ):
        self._context = context
        self._expected_type = expected_type
        self._received_type = received_type

    def make_error_message(self) -> str:
        return (
            f"At line {self._context.line}, column {self._context.column}: "
            f"Expected type {self._expected_type}. Received type {self._received_type}."
        )


class UndefinedVariable(TypecheckError):
    def __init__(self, variable_name: str, context: SourceContext):
        self._context = context
        self._variable_name = variable_name

    def make_error_message(self) -> str:
        return (
            f"At line {self._context.line}, column {self._context.column}: "
            f"Undefined variable {self._variable_name}."
        )


TypecheckResult = Union[Type, TypecheckError]


class TypecheckerVisitor(AstVisitor[TypecheckResult]):
    def __init__(self, environment: Environment = None):
        if environment is None:
            environment = Environment()
        self._environment = environment

    def visit_program(self, node: Program) -> TypecheckResult:
        checks: TypecheckResult = []
        for statement in node.statements:
            checks.append(statement.visit(self))

        errors = [error for error in checks if isinstance(error, TypecheckError)]
        if errors:
            return CombinedTypecheckErrors(errors)

        return Type.VOID

    def visit_print(self, node: Print) -> TypecheckResult:
        check_result = node.expression.visit(self)
        if isinstance(check_result, TypecheckError):
            return check_result

        return Type.VOID

    def visit_assignment(self, node: Assignment) -> TypecheckResult:
        rhs_check_result = node.rhs.visit(self)
        if isinstance(rhs_check_result, TypecheckError):
            return rhs_check_result

        self._environment.add_variable(node.name, rhs_check_result)
        return Type.VOID

    def visit_addition(self, node: Addition) -> TypecheckResult:
        lhs_check_result = node.lhs.visit(self)
        rhs_check_result = node.rhs.visit(self)

        if isinstance(lhs_check_result, TypecheckError):
            return lhs_check_result

        if isinstance(rhs_check_result, TypecheckError):
            return rhs_check_result

        if lhs_check_result is not Type.U8:
            return TypeMismatch(Type.U8, lhs_check_result, node.lhs.context)

        if rhs_check_result is not Type.U8:
            return TypeMismatch(Type.U8, rhs_check_result, node.rhs.context)

        return Type.U8

    def visit_negation(self, node: Negation) -> TypecheckResult:
        check_result = node.expression.visit(self)

        if isinstance(check_result, TypecheckError):
            return check_result

        if check_result is not Type.U8:
            return TypeMismatch(Type.U8, check_result, node.context)

        return check_result

    def visit_identifier(self, node: Identifier) -> TypecheckResult:
        return self._environment.get_variable_type(node.value, node.context)

    def visit_unsignedint(self, node: Unsignedint) -> TypecheckResult:
        return Type.U8

    def visit_bool(self, node: Bool) -> TypecheckResult:
        return Type.BOOL