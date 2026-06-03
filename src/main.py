from __future__ import annotations

import sys

from src.experiments.runner import ExperimentRunner


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    print("🚀 STARTING MACHINE LEARNING PIPELINE CRADLE 🚀\n")
    ExperimentRunner().run()

if __name__ == "__main__":
    main()
