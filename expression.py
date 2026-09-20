"""
ITECC04 Laboratory 4, Parts B and C:
the converter and the evaluator.

Part B turns infix into postfix using the Shunting Yard algorithm.
Part C evaluates a postfix expression.

Tokens must be separated by spaces.
Example: 3 + 4
"""

class ArrayStack:

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)




PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3
}

RIGHT_ASSOCIATIVE = {"^"}


def tokenize(expression):
    """Split expression using spaces."""
    return expression.split()


def _fmt(value):
    """Format values for trace output."""
    return str(value)


def infix_to_postfix(expression, trace=None):
    """Convert infix expression to postfix."""

    output = []
    operators = ArrayStack()

    for token in tokenize(expression):

        # If token is an operator
        if token in PRECEDENCE:

            while (
                not operators.is_empty()
                and operators.peek() != "("
                and (
                    PRECEDENCE[operators.peek()] > PRECEDENCE[token]
                    or (
                        PRECEDENCE[operators.peek()]
                        == PRECEDENCE[token]
                        and token not in RIGHT_ASSOCIATIVE
                    )
                )
            ):
                output.append(operators.pop())

            operators.push(token)
            action = "push operator"

        # Opening parenthesis
        elif token == "(":

            operators.push(token)
            action = "push ("

        # Closing parenthesis
        elif token == ")":

            while (
                not operators.is_empty()
                and operators.peek() != "("
            ):
                output.append(operators.pop())

            if operators.is_empty():
                raise ValueError(
                    "unbalanced parentheses: no matching ("
                )

            operators.pop()
            action = "pop to ("

        # Operand
        else:

            output.append(token)
            action = "operand to output"

        # Trace
        if trace is not None:
            trace.append(
                (
                    token,
                    action,
                    " ".join(output),
                    " ".join(operators._items)
                )
            )

    # Drain remaining operators
    while not operators.is_empty():

        top = operators.pop()

        if top == "(":
            raise ValueError(
                "unbalanced parentheses: no matching )"
            )

        output.append(top)

    if trace is not None:
        trace.append(
            (
                "end",
                "drain stack",
                " ".join(output),
                ""
            )
        )

    return " ".join(output)



def evaluate_postfix(expression, trace=None):
    """Evaluate a postfix expression."""

    values = ArrayStack()

    for token in tokenize(expression):

        # Operator
        if token in PRECEDENCE:

            if values.size() < 2:
                raise ValueError(
                    f"not enough operands for operator {token}"
                )

            # First pop = RIGHT operand
            right = values.pop()

            # Second pop = LEFT operand
            left = values.pop()

            result = apply_operator(
                token,
                left,
                right
            )

            values.push(result)

        # Operand
        else:
            values.push(float(token))

        # Trace
        if trace is not None:
            trace.append(
                (
                    token,
                    " ".join(
                        _fmt(value)
                        for value in values._items
                    )
                )
            )

    # There must be exactly one value
    if values.size() != 1:
        raise ValueError(
            "malformed expression: operands left over"
        )

    return values.pop()




def apply_operator(operator, left, right):

    if operator == "+":
        return left + right

    if operator == "-":
        return left - right

    if operator == "*":
        return left * right

    if operator == "/":

        if right == 0:
            raise ZeroDivisionError(
                "division by zero in expression"
            )

        return left / right

    if operator == "%":

        if right == 0:
            raise ZeroDivisionError(
                "modulo by zero in the expression"
            )

        return left % right

    if operator == "^":
        return left ** right

    raise ValueError(
        f"unknown operator {operator}"
    )




def convert_and_evaluate(expression):

    postfix = infix_to_postfix(expression)

    return postfix, evaluate_postfix(postfix)




if __name__ == "__main__":

    try:

        postfix, value = convert_and_evaluate(
            "3 + 4 * 2"
        )

        print("infix   : 3 + 4 * 2")
        print("postfix :", postfix)
        print("value   :", value)

    except NotImplementedError as unfinished:

        print(
            "Not written yet ->",
            unfinished
        )