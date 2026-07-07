import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(cmd: list[str]) -> None:
    print("\n$ " + " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the whole experiment pipeline.")
    parser.add_argument("--rows", type=int, default=1_000_000)
    parser.add_argument("--warmups", type=int, default=0)
    parser.add_argument("--runs", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--skip-generate", action="store_true")
    parser.add_argument("--skip-load", action="store_true")
    parser.add_argument("--skip-load-measurement", action="store_true")
    args = parser.parse_args()

    run([PYTHON, "scripts/wait_for_services.py"])
    if not args.skip_generate:
        generate_cmd = [PYTHON, "scripts/generate_data.py", "--rows", str(args.rows)]
        if args.seed is not None:
            generate_cmd.extend(["--seed", str(args.seed)])
        run(generate_cmd)
    run([PYTHON, "scripts/create_schema.py"])
    if not args.skip_load:
        run([PYTHON, "scripts/load_data.py"])
    run([PYTHON, "scripts/benchmark.py", "--warmups", str(args.warmups), "--runs", str(args.runs), "--rows", str(args.rows)])
    run([PYTHON, "scripts/build_charts.py"])
    if not args.skip_load_measurement:
        run([PYTHON, "scripts/measure_load_performance.py"])
    run([PYTHON, "scripts/build_readable_outputs.py"])


if __name__ == "__main__":
    main()
