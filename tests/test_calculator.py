import subprocess
import sys
import unittest
from pathlib import Path

from calculator import add, divide, multiply, subtract


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

    def test_rejects_division_by_zero(self):
        with self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
            divide(8, 0)


class CalculatorCliTests(unittest.TestCase):
    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CALCULATOR), *arguments],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_add_operation_prints_result(self):
        result = self.run_cli("add", "2", "3")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "5")
        self.assertEqual(result.stderr, "")

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

    def test_rejects_non_numeric_operand(self):
        result = self.run_cli("add", "two", "3")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid float value", result.stderr)

    def test_rejects_unknown_operation(self):
        result = self.run_cli("power", "2", "3")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid choice", result.stderr)

    def test_reports_division_by_zero_without_traceback(self):
        result = self.run_cli("divide", "8", "0")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cannot divide by zero", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
