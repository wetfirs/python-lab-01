import subprocess
import sys


def test_calc_cli() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "2+3*4"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "14.0000000000"

def test_calc_cli_error() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "1/0"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert result.stderr.strip() == "Деление на 0"

def test_convert_cli() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "convert", "100", "--from", "mm", "--to", "m"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "0.1"
