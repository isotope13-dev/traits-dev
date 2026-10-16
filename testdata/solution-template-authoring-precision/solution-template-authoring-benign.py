"""Benchmark task authoring: reads a solution template only to stamp out a
derived per-task copy. The answer is substituted in and written back out, not
exfiltrated, so the solution-read rule must NOT fire here.
"""

from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent / "template"


def build_task(output_dir: Path, answer: str) -> None:
    # Generate solution
    solution_dir = output_dir / "solution"
    solution_dir.mkdir(exist_ok=True)
    solution = (TEMPLATE_DIR / "solution/solve.sh").read_text()
    solution = solution.replace("{answer}", answer)
    (solution_dir / "solve.sh").write_text(solution)
