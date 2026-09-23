import argparse
import math
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
HISTORY_FILE = PROJECT_ROOT / ".calculator_history"


def read_history(history_path: Path = HISTORY_FILE) -> list[str]:
    if not history_path.exists():
        return []
    return history_path.read_text(encoding="utf-8").splitlines()


def record_history(
    operation: str,
    left: float,
    right: float | None,
    result: float,
    history_path: Path = HISTORY_FILE,
) -> None:
    if right is None:
        entry = f"{operation} {left:g} = {result:g}\n"
    else:
        entry = f"{operation} {left:g} {right:g} = {result:g}\n"
    with history_path.open("a", encoding="utf-8") as history_file:
        history_file.write(entry)


def add(left: float, right: float) -> float:
    return left + right


def subtract(left: float, right: float) -> float:
    return left - right


def multiply(left: float, right: float) -> float:
    return left * right


def divide(left: float, right: float) -> float:
    if right == 0:
        raise ValueError("Cannot divide by zero.")
    return left / right


def modulo(left: float, right: float) -> float:
    if right == 0:
        raise ValueError("Cannot modulo by zero.")
    return left % right


def power(left: float, right: float) -> float:
    return left**right


def square_root(value: float) -> float:
    if value < 0:
        raise ValueError("Cannot calculate square root of a negative number.")
    return math.sqrt(value)


def main() -> int:
    parser = argparse.ArgumentParser(description="Perform a basic calculation.")
    parser.add_argument(
        "operation",
        choices=(
            "add",
            "subtract",
            "multiply",
            "divide",
            "modulo",
            "power",
            "sqrt",
            "history",
        ),
    )
    parser.add_argument("left", type=float, nargs="?")
    parser.add_argument("right", type=float, nargs="?")
    arguments = parser.parse_args()
    history_path = Path(
        os.environ.get("CALCULATOR_HISTORY_FILE", str(HISTORY_FILE))
    )

    if arguments.operation == "history":
        if arguments.left is not None or arguments.right is not None:
            parser.error("history does not accept operands.")
        for entry in read_history(history_path):
            print(entry)
        return 0

    if arguments.operation == "sqrt":
        if arguments.left is None:
            parser.error("sqrt requires one operand.")
        if arguments.right is not None:
            parser.error("sqrt accepts exactly one operand.")
        try:
            result = square_root(arguments.left)
        except ValueError as error:
            parser.error(str(error))
        record_history("sqrt", arguments.left, None, result, history_path)
        print(f"{result:g}")
        return 0

    if arguments.left is None or arguments.right is None:
        parser.error("left and right operands are required.")

    if arguments.operation == "add":
        result = add(arguments.left, arguments.right)
    elif arguments.operation == "subtract":
        result = subtract(arguments.left, arguments.right)
    elif arguments.operation == "multiply":
        result = multiply(arguments.left, arguments.right)
    elif arguments.operation == "power":
        result = power(arguments.left, arguments.right)
    else:
        try:
            if arguments.operation == "divide":
                result = divide(arguments.left, arguments.right)
            else:
                result = modulo(arguments.left, arguments.right)
        except ValueError as error:
            parser.error(str(error))
    record_history(
        arguments.operation,
        arguments.left,
        arguments.right,
        result,
        history_path,
    )
    print(f"{result:g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
