from __future__ import annotations

from z64c.ast import (
    Program,
    Print,
    Assignment,
    Addition,
    Negation,
    Identifier,
    Unsignedint,
    Bool,
)
from z64c.ast import AstVisitor, T

INDENTATION = "    "


class Environment:
    def __init__(self):
        self._variable_offsets = {}

    def add_variable(self, name: str):
        self._variable_offsets[name] = -2
        self._variable_offsets = {
            key: offset + 2 for key, offset in self._variable_offsets.items()
        }

    def get_variable_offset(self, name: str) -> int:
        return self._variable_offsets[name]


class SjasmplusSnapshotVisitor(AstVisitor[None]):
    def __init__(self, codegen: Z80CodegenVisitor, source_name: str):
        self._codegen = codegen
        self._source_name = source_name

    def visit_program(self, node: Program) -> None:
        print(f"{INDENTATION}DEVICE ZXSPECTRUM48")
        self._codegen.visit_program(node)
        print("")
        print(f'{INDENTATION}SAVESNA "{self._source_name}.sna", start')

    def visit_print(self, node: Print) -> None:
        self._codegen.visit_print(node)

    def visit_assignment(self, node: Assignment) -> None:
        pass
        self._codegen.visit_assignment(node)

    def visit_addition(self, node: Addition) -> None:
        pass
        self._codegen.visit_addition(node)

    def visit_negation(self, node: Negation) -> None:
        pass
        self._codegen.visit_negation(node)

    def visit_identifier(self, node: Identifier) -> None:
        pass
        self._codegen.visit_identifier(node)

    def visit_unsignedint(self, node: Unsignedint) -> None:
        self._codegen.visit_unsignedint(node)


class Z80CodegenVisitor(AstVisitor[None]):
    def __init__(self, environment: Environment):
        self._environment = environment

    def visit_program(self, node: Program) -> None:
        print(f"{INDENTATION}org $8000")
        print("")
        print("start:")
        for statement in node._statements:
            statement.visit(self)
        print(f"{INDENTATION}ret")

    def visit_print(self, node: Print) -> T:
        node._expression.visit(self)
        print(f"{INDENTATION}rst $10")

    def visit_assignment(self, node: Assignment) -> None:
        node._rhs.visit(self)
        self._environment.add_variable(node._name)
        print(f"{INDENTATION}push af")

    def visit_addition(self, node: Addition) -> None:
        node._lhs.visit(self)
        print(f"{INDENTATION}ld b, a")
        node._rhs.visit(self)
        print(f"{INDENTATION}adc a, b")

    def visit_negation(self, node: Negation) -> None:
        node._expression.visit(self)
        print(f"{INDENTATION}neg")

    def visit_identifier(self, node: Identifier) -> None:
        offset = self._environment.get_variable_offset(node._value)
        print(f"{INDENTATION}ld hl, $00")
        print(f"{INDENTATION}add hl, sp")
        print(f"{INDENTATION}ld ix, hl")
        print(f"{INDENTATION}ld a, (ix + {offset + 1})")

    def visit_unsignedint(self, node: Unsignedint) -> None:
        print(f"{INDENTATION}ld a, {node._value}")

    def visit_bool(self, node: Bool) -> None:
        value = 1 if node._value else 0
        print(f"{INDENTATION}ld a, {value}")
