import pytest

@pytest.mark.parametrize("op1, op2, op, expected", [
    (10, 5, "+", 15),
    (10, 5, "-", 5),
    (10, 5, "*", 50),
    (10, 5, "/", 2),
])
def test_basic_operations(op1, op2, op, expected):
    if op == "+":
        result = op1 + op2
    elif op == "-":
        result = op1 - op2
    elif op == "*":
        result = op1 * op2
    elif op == "/":
        result = op1 / op2
    else:
        pytest.fail("Invalid operation")

    assert result == expected
