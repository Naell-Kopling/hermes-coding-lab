import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from calculator import (
    add,
    divide,
    modulo,
    multiply,
    power,
    read_history,
    record_history,
    subtract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CALCULATOR = PROJECT_ROOT / "calculator.py"


class ArithmeticTests(unittest.TestCase):
    def test_adds_two_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_subtracts_two_numbers(self):
        self.assertEqual(subtract(7, 4), 3)

    def test_multiplies_two_numbers(self):
        self.assertEqual(multiply(6, 7), 42)

    def test_divides_two_numbers(self):
        self.assertEqual(divide(8, 2), 4)

    def test_returns_remainder_of_two_numbers(self):
        self.assertEqual(modulo(7, 3), 1)

    def test_raises_number_to_power(self):
        self.assertEqual(power(2, 3), 8)

    def test_rejects_modulo_by_zero(self):
        with self.assertRaisesRegex(ValueError, "Cannot modulo by zero"):
            modulo(8, 0)

    def test_rejects_division_by_zero(self):
        with self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
            divide(8, 0)


class HistoryTests(unittest.TestCase):
    def test_reading_missing_history_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            history_path = Path(directory) / "history.txt"

            self.assertEqual(read_history(history_path), [])

    def test_records_calculation_history(self):
        with tempfile.TemporaryDirectory() as directory:
            history_path = Path(directory) / "history.txt"

            record_history("add", 2, 3, 5, history_path)

            self.assertEqual(read_history(history_path), ["add 2 3 = 5"])


class CalculatorCliTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.history_path = Path(self.temporary_directory.name) / "history.txt"

    def tearDown(self):
        self.temporary_directory.cleanup()

    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["CALCULATOR_HISTORY_FILE"] = str(self.history_path)
        return subprocess.run(
            [sys.executable, str(CALCULATOR), *arguments],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
            env=environment,
        )

    def test_add_operation_prints_result(self):
        result = self.run_cli("add", "2", "3")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "5")
        self.assertEqual(result.stderr, "")

    def test_successful_operation_is_saved_to_history(self):
        calculations = (
            (("add", "2", "3"), "add 2 3 = 5"),
            (("subtract", "7", "4"), "subtract 7 4 = 3"),
            (("multiply", "6", "7"), "multiply 6 7 = 42"),
            (("divide", "7", "2"), "divide 7 2 = 3.5"),
            (("modulo", "7", "3"), "modulo 7 3 = 1"),
        )

        for arguments, _ in calculations:
            result = self.run_cli(*arguments)
            self.assertEqual(result.returncode, 0)

        self.assertEqual(
            self.history_path.read_text(encoding="utf-8").splitlines(),
            [entry for _, entry in calculations],
        )

    def test_history_command_prints_saved_operations(self):
        self.run_cli("add", "2", "3")
        self.run_cli("multiply", "4", "5")

        result = self.run_cli("history")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.splitlines(), ["add 2 3 = 5", "multiply 4 5 = 20"])
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            self.history_path.read_text(encoding="utf-8"),
            "add 2 3 = 5\nmultiply 4 5 = 20\n",
        )

    def test_subtract_operation_prints_result(self):
        result = self.run_cli("subtract", "7", "4")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "3")
        self.assertEqual(result.stderr, "")

    def test_multiply_operation_prints_result(self):
        result = self.run_cli("multiply", "6", "7")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "42")

    def test_divide_operation_prints_result(self):
        result = self.run_cli("divide", "7", "2")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "3.5")

    def test_modulo_operation_prints_result(self):
        result = self.run_cli("modulo", "7", "3")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "1")
        self.assertEqual(result.stderr, "")

    def test_power_operation_prints_result(self):
        result = self.run_cli("power", "2", "3")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "8")
        self.assertEqual(result.stderr, "")

    def test_rejects_non_numeric_operand(self):
        result = self.run_cli("add", "two", "3")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid float value", result.stderr)

    def test_rejects_unknown_operation(self):
        result = self.run_cli("square", "2", "3")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid choice", result.stderr)

    def test_reports_modulo_by_zero_without_traceback(self):
        result = self.run_cli("modulo", "8", "0")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cannot modulo by zero", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_reports_division_by_zero_without_traceback(self):
        result = self.run_cli("divide", "8", "0")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cannot divide by zero", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(self.history_path.exists())


if __name__ == "__main__":
    unittest.main()
