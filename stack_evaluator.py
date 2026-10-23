"""Stack-based expression evaluator for DCOMP320.

This program reads mathematical expressions from input.txt, evaluates each one using
stack-based expression parsing, and writes the results to output.txt. It preserves the
input format by writing one result per expression and inserting the same separator line
between results.

Supported operators:
    +, -, *, /
    Parentheses: (, )

Notes:
    - Integer and decimal numbers are supported.
    - Multiplication and division have higher precedence than addition and subtraction.
    - Operators with the same precedence are evaluated left-to-right.
    - Unary minus is supported for expressions like -5 or 3 * -2.
"""

from __future__ import annotations

import os
from typing import List, Union


class Stack:
    """A simple stack implementation using a Python list."""

    def __init__(self):
        self._items: List[Union[int, float, str]] = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item from the stack."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("Stack is empty.")
        return self._items[-1]

    def is_empty(self):
        """Return True when the stack has no items."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self._items)


def tokenize(expression: str):
    """Break a mathematical expression into tokens.

    Tokens can be numbers, operators, parentheses, or the unary minus marker.
    """
    tokens = []
    i = 0

    while i < len(expression):
        ch = expression[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit() or ch == '.':
            start = i
            has_decimal = False

            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                if expression[i] == '.':
                    if has_decimal:
                        raise ValueError(f"Malformed number in expression: {expression[start:i + 1]}")
                    has_decimal = True
                i += 1

            number_text = expression[start:i]
            if number_text == '.' or number_text.count('.') > 1:
                raise ValueError(f"Malformed number in expression: {number_text}")

            tokens.append(float(number_text) if '.' in number_text else int(number_text))
            continue

        if ch in '+-*/()':
            if ch == '-' and (not tokens or tokens[-1] in ('(', '+', '-', '*', '/')):
                tokens.append('u-')
            else:
                tokens.append(ch)
            i += 1
            continue

        raise ValueError(f"Invalid character '{ch}' found in expression.")

    return tokens


def precedence(operator: str) -> int:
    """Return the precedence level for an operator."""
    if operator in ('*', '/'):
        return 2
    if operator in ('+', '-'):
        return 1
    if operator == 'u-':
        return 3
    raise ValueError(f"Unknown operator '{operator}'")


def to_postfix(tokens):
    """Convert an infix expression into postfix form using the shunting-yard algorithm."""
    output = []
    operators = []

    for token in tokens:
        if isinstance(token, (int, float)):
            output.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if not operators:
                raise ValueError("Mismatched parentheses.")
            operators.pop()
        elif token in ('+', '-', '*', '/', 'u-'):
            while (
                operators
                and operators[-1] != '('
                and (
                    precedence(operators[-1]) > precedence(token)
                    or (
                        precedence(operators[-1]) == precedence(token)
                        and token != 'u-'
                    )
                )
            ):
                output.append(operators.pop())
            operators.append(token)
        else:
            raise ValueError(f"Unexpected token: {token}")

    while operators:
        operator = operators.pop()
        if operator == '(':
            raise ValueError("Mismatched parentheses.")
        output.append(operator)

    return output


def evaluate_postfix(postfix_tokens, show_steps: bool = False):
    """Evaluate a postfix expression using a stack.

    If show_steps is True, the stack operations and intermediate results are printed
    to the console so the calculation can be seen when the program runs.
    """
    values = Stack()

    for token in postfix_tokens:
        if isinstance(token, (int, float)):
            values.push(token)
            if show_steps:
                print(f"  Push {token} -> stack: {list(values._items)}")
        elif token == 'u-':
            if values.is_empty():
                raise ValueError("Malformed expression.")
            operand = values.pop()
            result = -operand
            values.push(result)
            if show_steps:
                print(f"  Unary minus: -{operand} = {result} -> stack: {list(values._items)}")
        elif token in ('+', '-', '*', '/'):
            if values.size() < 2:
                raise ValueError("Malformed expression.")

            right = values.pop()
            left = values.pop()

            if token == '+':
                result = left + right
            elif token == '-':
                result = left - right
            elif token == '*':
                result = left * right
            elif token == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero.")
                result = left / right
            else:
                raise ValueError(f"Unknown operator '{token}'")

            values.push(result)
            if show_steps:
                print(f"  Apply {left} {token} {right} = {result} -> stack: {list(values._items)}")
        else:
            raise ValueError(f"Unexpected postfix token: {token}")

    if values.size() != 1:
        raise ValueError("Malformed expression.")

    final_result = values.pop()
    if show_steps:
        print(f"  Final result: {final_result}")
    return final_result


def evaluate_expression(expression: str, show_steps: bool = False):
    """Evaluate one expression and return the numeric result."""
    if expression is None or not expression.strip():
        raise ValueError("Blank expression.")

    tokens = tokenize(expression)
    postfix_tokens = to_postfix(tokens)

    if show_steps:
        print(f"\nExpression: {expression}")
        print(f"Tokens: {tokens}")
        print(f"Postfix: {postfix_tokens}")

    result = evaluate_postfix(postfix_tokens, show_steps=show_steps)

    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


def read_expressions(file_path: str):
    """Read expressions from the file while ignoring blank lines and separators.

    Each expression is expected to be one line. Separators are lines containing only dashes.
    """
    expressions = []
    current_expression = []

    with open(file_path, 'r', encoding='utf-8') as input_file:
        for raw_line in input_file:
            line = raw_line.strip()

            if not line:
                continue

            if line == '-----':
                if current_expression:
                    expressions.append(' '.join(current_expression).strip())
                    current_expression = []
                continue

            current_expression.append(line)

    if current_expression:
        expressions.append(' '.join(current_expression).strip())

    return expressions


def format_result(value):
    """Convert a numeric result to tidy output text."""
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return format(value, '.10g')
    return str(value)


def process_file(input_path: str, output_path: str):
    """Read all expressions, evaluate them, and write output in the same format."""
    expressions = read_expressions(input_path)
    results = []

    print("=== Evaluating expressions ===")
    for expression in expressions:
        print(f"\n--- Expression: {expression} ---")
        try:
            value = evaluate_expression(expression, show_steps=True)
            formatted_value = format_result(value)
            results.append(formatted_value)
            print(f"Final computed value: {formatted_value}")
        except ZeroDivisionError:
            message = 'ERROR: Division by zero.'
            results.append(message)
            print(message)
        except ValueError as error:
            message = f'ERROR: {error}'
            results.append(message)
            print(message)
        except Exception as error:  # pragma: no cover - defensive fallback
            message = f'ERROR: {error}'
            results.append(message)
            print(message)

    if results:
        output_text = '\n-----\n'.join(results)
    else:
        output_text = ''

    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.write(output_text)

    print("\n=== Finished ===")
    print(f"Results written to {output_path}")


def main():
    """Main entry point for the program."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, 'input.txt')
    output_file = os.path.join(base_dir, 'output.txt')

    process_file(input_file, output_file)


if __name__ == '__main__':
    main()
