import argparse


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Perform a basic calculation.")
    parser.add_argument("operation", choices=("add", "subtract", "multiply", "divide"))
    parser.add_argument("left", type=float)
    parser.add_argument("right", type=float)
    arguments = parser.parse_args()

    if arguments.operation == "add":
        result = add(arguments.left, arguments.right)
    elif arguments.operation == "subtract":
        result = subtract(arguments.left, arguments.right)
    elif arguments.operation == "multiply":
        result = multiply(arguments.left, arguments.right)
    else:
        try:
            result = divide(arguments.left, arguments.right)
        except ValueError as error:
            parser.error(str(error))
    print(f"{result:g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
